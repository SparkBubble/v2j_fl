# 在指定目录下将 Verilog 文件转换为 Java ，并生成 Java 项目
# 项目名为 Verilog 文件名，请注意重名问题
# 以标准 io 文件为基准，生成单元测试



# * 以下参数需要根据实际情况修改
verilog_file_path = 'generator/test/fadd32_13.v'  # 输入Verilog文件路径

verilog_io_path = 'generator/testdata/fadd32.io10000'  # 输入Verilog IO文件路径
ports_resort = [1, 2, 0, 3, 4] # 模块上数第 i 个端口位于IO文件第左数 p[i] 列
samp_rate = 0.10  # IO测试采样率（0~1之间，数值越大越准确，但是测试时间与其成正比）


# ? 以下参数一般无需修改
java_project_parentDir = 'java_prjs'  # 生成的Java项目放到哪个目录下
output_dir = 'output'  # 输出放到哪个目录下

java_tools_dir = 'java_tools'  # 生成工具目录
java_package_name =  'module'  # Java包名

parser_detail = True  # 是否使用详细语法分析器





# ! 以下代码无需修改

from convert.converter import Verilog2JavaConverter as V2JStd
from convert.converter_detail import Verilog2JavaConverter as V2JDtl
import os, shutil, sys
import subprocess

def generate_project(project_name:str):
    if not os.path.exists(java_project_parentDir):
        os.mkdir(java_project_parentDir)
    pwd = os.getcwd()
    os.chdir(java_project_parentDir)
    if os.path.exists(project_name):
        print(f'Project {project_name} already exists, maybe you want to delete it first.')
        os.chdir(pwd)
        return os.path.join(java_project_parentDir, project_name)
    # 创建maven项目
    print(f'Creating maven project {project_name}...')
    print('------------------------------------------------')
    subprocess.run(['mvn', 
                    'archetype:generate', 
                    '-DarchetypeArtifactId=maven-archetype-quickstart', 
                    '-DartifactId=' + project_name, 
                    '-DgroupId=' + java_package_name, 
                    '-DinteractiveMode=false'])
    print('------------------------------------------------')
    print(f'Maven project {project_name} created.\n\n')
    os.chdir(pwd)
    return os.path.join(java_project_parentDir, project_name)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] :
        verilog_file_path = args[0]
    # 生成项目
    project_name = os.path.basename(verilog_file_path).split('.')[0]
    project_path = generate_project(project_name)
    
    # 删除原有文件
    try:
        os.remove(os.path.join(project_path, 'pom.xml'))
        os.remove(os.path.join(project_path, 'src', 'test', 'java', java_package_name, 'AppTest.java'))
        os.remove(os.path.join(project_path, 'src', 'main', 'java', java_package_name, 'App.java'))
    except:
        pass

    # 生成模块和单元测试
    print(f'载入Verilog文件 ———— {verilog_file_path}')
    if parser_detail:
        converter = V2JDtl(verilog_file_path)
    else:
        converter = V2JStd(verilog_file_path)
    print(f'解析Verilog文件 ———— {verilog_file_path}\n')
    # converter.parser_log('parser.log')

    print(f'生成模块Java代码...')
    dir = os.path.join(project_path, 'src', 'main', 'java', java_package_name)
    converter.toJava(dir, java_package_name)
    print(f'模块Java代码生成至 {dir}\n')

    print(f'生成单元测试...')
    dir = os.path.join(project_path, 'src', 'test', 'java', java_package_name)
    converter.genTest(dir, verilog_io_path, ports_resort, samp_rate)
    print(f'单元测试生成至 {dir}\n')
    
    # 生成wire.java
    print(f'生成wire.java...')
    shutil.copy(os.path.join(java_tools_dir, 'wire.java'), os.path.join(project_path, 'src', 'main', 'java', java_package_name))

    # 生成testall.java
    print(f'生成testall.java...')
    with open(os.path.join(java_tools_dir, 'testall.java'), 'r', encoding='utf-8') as f:
        code = f.read()
        code = code.replace("path_to_test_io", os.path.abspath(verilog_io_path))
        with open(os.path.join(project_path, 'src', 'main', 'java', java_package_name, 'testall.java'), 'w', encoding='utf-8') as f:
            f.write(code)

    # # 生成pom.xml
    # print(f'生成pom.xml...\n')
    # with open(os.path.join(java_tools_dir, 'pom.xml'), 'r', encoding='utf-8') as f:
    #     code = f.read()
    #     code = code.replace("the_package_name_of_this_project", java_package_name)
    #     code = code.replace("the_project_name_of_this_project", os.path.basename(project_path))
    #     with open(os.path.join(project_path, 'pom.xml'), 'w', encoding='utf-8') as f:
    #         f.write(code)

    # 复制gzoltar包
    print(f'复制gzoltar包...')
    if not os.path.exists(os.path.join(project_path, 'lib')):
        os.mkdir(os.path.join(project_path, 'lib'))
    shutil.copy(os.path.join(java_tools_dir, 'gzoltarcli.jar'), os.path.join(project_path, 'lib'))
    shutil.copy(os.path.join(java_tools_dir, 'gzoltaragent.jar'), os.path.join(project_path, 'lib'))

    # 复制其他依赖
    print(f'复制其他依赖...')
    if not os.path.exists(os.path.join(project_path, 'lib')):
        os.mkdir(os.path.join(project_path, 'lib'))
    shutil.copy(os.path.join(java_tools_dir, 'junit.jar'), os.path.join(project_path, 'lib'))
    shutil.copy(os.path.join(java_tools_dir, 'hamcrest-core.jar'), os.path.join(project_path, 'lib'))

    # 复制执行脚本
    print(f'复制执行脚本...')
    shutil.copy(os.path.join(java_tools_dir, 'run.sh'), os.path.join(project_path))
    os.chmod(os.path.join(project_path, 'run.sh'), 0o777)

    print(f'\n项目生成完毕！')

    # 运行测试
    print(f'\n运行测试...')
    print('---------------------------------------------')
    subprocess.run(['bash', './run.sh'], cwd=project_path)
    print('---------------------------------------------')
    print(f'测试结束！')

    # 获取结果
    print(f'\n获取结果...')
    result_file = os.path.join(project_path, 'build', 'sfl', 'txt', 'ochiai.ranking.csv')
    if os.path.exists(result_file):
        with open(result_file, 'r', encoding='utf-8') as f:
            result = f.read()
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            with open(os.path.join(output_dir, f'{project_name}.csv'), 'w', encoding='utf-8') as f:
                f.write(result)
    else:
        print(f'结果文件不存在！')
    print(f'结果已保存至{os.path.join(output_dir, f"{project_name}.csv")}')
