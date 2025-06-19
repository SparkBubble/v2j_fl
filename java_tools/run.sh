SCRIPT_DIR=$(cd `dirname ${BASH_SOURCE[0]}` && pwd)

# Prepare runtime dependencies

LIB_DIR="$SCRIPT_DIR/lib"
mkdir -p "$LIB_DIR" 
[ -d "$LIB_DIR" ] 

JUNIT_JAR="$LIB_DIR/junit.jar"
if [ ! -s "$JUNIT_JAR" ]; then
  wget "https://repo1.maven.org/maven2/junit/junit/4.12/junit-4.12.jar" -O "$JUNIT_JAR" 
fi
[ -s "$JUNIT_JAR" ] 

HAMCREST_JAR="$LIB_DIR/hamcrest-core.jar"
if [ ! -s "$HAMCREST_JAR" ]; then
  wget -np -nv "https://repo1.maven.org/maven2/org/hamcrest/hamcrest-core/1.3/hamcrest-core-1.3.jar" -O "$HAMCREST_JAR" 
fi
[ -s "$HAMCREST_JAR" ] 

GZOLTAR_CLI_JAR="$LIB_DIR/gzoltarcli.jar"
if [ ! -s "$GZOLTAR_CLI_JAR" ]; then
  cp "$SCRIPT_DIR/gzoltarcli.jar" "$GZOLTAR_CLI_JAR" 
fi
[ -s "$GZOLTAR_CLI_JAR" ] 

GZOLTAR_AGENT_RT_JAR="$LIB_DIR/gzoltaragent.jar"
if [ ! -s "$GZOLTAR_AGENT_RT_JAR" ]; then
  cp "$SCRIPT_DIR/gzoltaragent.jar" "$GZOLTAR_AGENT_RT_JAR" 
fi
[ -s "$GZOLTAR_AGENT_RT_JAR" ] 


BUILD_DIR="$SCRIPT_DIR/build"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR" 



# Compile source and test files

SRC_DIR="$SCRIPT_DIR/src/main/java"
TEST_DIR="$SCRIPT_DIR/src/test/java"

javac -d "$BUILD_DIR" "$SRC_DIR/module/wire.java" 
javac -d "$BUILD_DIR" -cp "$BUILD_DIR" "$SRC_DIR/module/FADD.java" 
javac -cp $JUNIT_JAR:$BUILD_DIR "$TEST_DIR/module/FADDTest.java" -d "$BUILD_DIR" 


# Collect list of unit test cases to run

UNIT_TESTS_FILE="$BUILD_DIR/tests.txt"


java -cp $BUILD_DIR:$JUNIT_JAR:$HAMCREST_JAR:$GZOLTAR_CLI_JAR \
  com.gzoltar.cli.Main listTestMethods $BUILD_DIR \
    --outputFile "$UNIT_TESTS_FILE" \
    --includes "module.FADDTest#*" 
[ -s "$UNIT_TESTS_FILE" ] 

# collect coverage data

SER_FILE="$BUILD_DIR/gzoltar.ser"

echo "Perform offline instrumentation ..."

# Backup original classes
BUILD_BACKUP_DIR="$SCRIPT_DIR/.build"
mv "$BUILD_DIR" "$BUILD_BACKUP_DIR" 
mkdir -p "$BUILD_DIR"

# Perform offline instrumentation
java -cp $BUILD_BACKUP_DIR:$GZOLTAR_AGENT_RT_JAR:$GZOLTAR_CLI_JAR \
  com.gzoltar.cli.Main instrument \
    --outputDirectory "$BUILD_DIR" \
    $BUILD_BACKUP_DIR 

echo "Run each unit test case in isolation ..."

# Run each unit test case in isolation
java -cp $BUILD_DIR:$JUNIT_JAR:$HAMCREST_JAR:$GZOLTAR_AGENT_RT_JAR:$GZOLTAR_CLI_JAR \
  -Dgzoltar-agent.destfile=$SER_FILE \
  -Dgzoltar-agent.output="file" \
  com.gzoltar.cli.Main runTestMethods \
    --testMethods "$UNIT_TESTS_FILE" \
    --offline \
    --collectCoverage 

# Restore original classes
cp -R $BUILD_BACKUP_DIR/* "$BUILD_DIR" 
rm -rf "$BUILD_BACKUP_DIR"

[ -s "$SER_FILE" ] 

echo "Generate coverage report ..."

SPECTRA_FILE="$BUILD_DIR/sfl/txt/spectra.csv"
MATRIX_FILE="$BUILD_DIR/sfl/txt/matrix.txt"
TESTS_FILE="$BUILD_DIR/sfl/txt/tests.csv"

java -cp $BUILD_DIR:$JUNIT_JAR:$HAMCREST_JAR:$GZOLTAR_CLI_JAR \
  com.gzoltar.cli.Main faultLocalizationReport \
    --buildLocation "$BUILD_DIR" \
    --excludes "module.wire:module.*Test" \
    --granularity "line" \
    --inclPublicMethods \
    --inclStaticConstructors \
    --inclDeprecatedMethods \
    --dataFile "$SER_FILE" \
    --outputDirectory "$BUILD_DIR" \
    --family "sfl" \
    --formula "ochiai" \
    --metric "entropy" \
    --formatter "txt" 

[ -s "$SPECTRA_FILE" ] 
[ -s "$MATRIX_FILE" ] 
[ -s "$TESTS_FILE" ] 

echo "DONE!"
exit 0