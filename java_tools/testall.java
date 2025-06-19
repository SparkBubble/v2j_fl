package module;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.math.BigInteger;

/**
 * Hello world!
 *
 */
public class testall 
{
    public static void main(String[] args) {
        FADD fadd = new FADD();
        String filename = "path_to_test_io";

        try {
            BufferedReader br = new BufferedReader(new FileReader(filename));
            String line = br.readLine();

            int right_count = 0;
            int wrong_count = 0;
            while (line!= null) {
                String[] parts = line.split(" ");
                BigInteger rm = new BigInteger(parts[0], 16);
                BigInteger a = new BigInteger(parts[1], 16);
                BigInteger b = new BigInteger(parts[2], 16);
                BigInteger result = new BigInteger(parts[3], 16);
                BigInteger fflags = new BigInteger(parts[4], 16);
                fadd.loadInput(a, b, rm);
                fadd.compute();
                if (!fadd.get_io_result().equals(result) ||!fadd.get_io_fflags().equals(fflags)) {
                    System.out.println("Error: " + line);
                    System.out.println("Expected: " + result.toString(16) + " " + fflags.toString(16));
                    System.out.println("Got: " + fadd.get_io_result().toString(16) + " " + fadd.get_io_fflags().toString(16));
                    wrong_count++;
                } else {
                    right_count++;
                }
                line = br.readLine();
            }
            br.close();
            System.out.println("Right count: " + right_count);
            System.out.println("Wrong count: " + wrong_count);
            System.out.println("Accuracy: " + (float)right_count/(right_count+wrong_count) * 100 + "%");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
