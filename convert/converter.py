import re
from collections import defaultdict, deque
from jinja2 import Template

from convert.v2j_yacc import parser
from convert.parser import VerilogParser


class Verilog2JavaConverter:
    def __init__(self, verilog_file_path):
        self.parser = VerilogParser(verilog_file_path)
        self.assignments_javacode = []

    def parser_log(self, log_path:str):
        self.parser.log(log_path)

    def _translate_assignment(self):
        for var, lb, rb, expr in self.parser.sorted_assignments:
            try:
                verilog_code = f'{var.name}'
                if lb != var.highBit or rb != var.lowBit:
                    if lb == rb:
                        verilog_code += f'[{lb}]'
                    else:
                        verilog_code += f'[{lb}:{rb}]'
                verilog_code += f' = {expr}'
                javacode = parser.parse(verilog_code)
                self.assignments_javacode.append(javacode)
            except Exception as e:
                print(f'Error in assignment statement: {expr}')
                raise e

    def toJava(self, dir_path:str, package_name:str='module') -> str:
        """
        将 Verilog 代码转换为 Java 代码
        
        Parameters
        ----------
            dir_path : 输出位置(父目录)，文件名自动设置为模块名
            package_name : 包名
        """
        if len(self.assignments_javacode) == 0:
            self._translate_assignment()
        with open(f'{dir_path}/{self.parser.module_name}.java', 'w', encoding='utf-8') as f:
            template = '''package {{ package_name }};
import java.math.BigInteger;

public class {{ module_name }} {
    // inputs{% for port in ports.input %}
    private wire {{ port.name }} = new wire({{ port.highBit }}, {{ port.lowBit }});{% endfor %}

    // outputs{% for port in ports.output %}
    private wire {{ port.name }} = new wire({{ port.highBit }}, {{ port.lowBit }});{% endfor %}

    public void loadInput({% for port in ports.input %}BigInteger {{ port.name }}{% if not loop.last %}, {% endif %}{% endfor %}) {
        // load inputs{% for port in ports.input %}
        this.{{ port.name }}.set({{ port.name }});{% endfor %}
    }

    // getters{% for port in ports.output %}
    public BigInteger get_{{ port.name }}() {
        return this.{{ port.name }}.get();
    }{% endfor %}

    public void compute() {
        // declare variables{% for var in sorted_variables %}
        wire {{ var.name }} = new wire({{ var.highBit }}, {{ var.lowBit }});{% endfor %}

        // assignments{% for assign in assignments_javacode %}
        {{ assign }}{% endfor %}
    }

}

'''
            context = {
                'package_name': package_name,
                'module_name': self.parser.module_name,
                'ports': {
                    'input': [{'name': port[0], 'highBit': port[1], 'lowBit': port[2]} for port in self.parser.input_ports],
                    'output': [{'name': port[0], 'highBit': port[1], 'lowBit': port[2]} for port in self.parser.output_ports]
                },
                'sorted_variables': self.parser.sorted_variables,
                'assignments_javacode': self.assignments_javacode
            }
            f.write(Template(template).render(context))
        return f'{self.parser.module_name}.java'

    def genTest(self, dir_path:str, testio_path:str, resort_index:list[int]|None = None, samp_rate:float=0.01, package_name:str='module'):
        """
        生成对应的单元测试
        
        Parameters
        ----------
        dir_path : 输出目录
        
        testio_path : 标准io文件路径
            文件每行对应一组测试数据，每组数据由端口输入输出值组成，value 为十六进制字符串，每行数量必须与端口数量一致。
            
            标准io文件格式：
        ```
        value0 value1 value2 value3 value4 value5 ... \\n
        value0 value1 value2 value3 value4 value5 ... \\n
        ...
        ```
            
        
        resort_index : 重新排序端口索引
        ```
            若为 None ，则默认按 verilog 模块端口定义顺序读取io文件。

            否则，按 resort_index 指定的顺序读取io文件。

            例如 resort_index = [1, 3, 0, 2] ，表示
            第 0 个端口对应 io 文件的第 1 列，
            第 1 个端口对应 io 文件的第 3 列，
            第 2 个端口对应 io 文件的第 0 列，
            第 3 个端口对应 io 文件的第 2 列
        ```
        
        package_name : 包名
        """
        
        if len(self.assignments_javacode) == 0:
            self._translate_assignment()
        
        if resort_index:
            if len(resort_index) != len(self.parser.input_ports) + len(self.parser.output_ports):
                raise ValueError("resort_index length should be equal to the number of ports.")
        
        template = '''package {{ package_name }};
import java.math.BigInteger;
import org.junit.Test;
import static org.junit.Assert.*;

public class {{ module_name }}Test {
    private {{ module_name }} module = new {{ module_name }}();

{% for test in tests %}
    @Test
    public void test{{ loop.index }}() {
        {% for port in ports.input %}
        BigInteger {{ port.name }} = new BigInteger("{{ test.input[port.name] }}", 16);{% endfor %}
        {% for port in ports.output %}
        BigInteger {{ port.name }} = new BigInteger("{{ test.output[port.name] }}", 16);{% endfor %}

        module.loadInput({% for port in ports.input %}{{ port.name }}{% if not loop.last %}, {% endif %}{% endfor %});
        module.compute();
        {% for port in ports.output %}
        assertTrue({{ port.name }}.equals(module.get_{{ port.name }}()));{% endfor %}
    }
{% endfor %}
}

'''
        tests = []
        try:
            with open(testio_path, 'r', encoding='utf-8') as fio:
                lines = fio.readlines()
                import time, random
                random.seed(time.time())
                samp_line = random.sample(lines, int(len(lines) * samp_rate))
                for line in samp_line:
                    values = line.strip().split()
                    input_values = {}
                    output_values = {}
                    index = 0
                    for port in self.parser.input_ports:
                        value_str = values[resort_index[index]] if resort_index else values[index]
                        input_values[port[0]] = value_str
                        index += 1
                    for port in self.parser.output_ports:
                        value_str = values[resort_index[index]] if resort_index else values[index]
                        output_values[port[0]] = value_str
                        index += 1
                    tests.append({'input': input_values, 'output': output_values})
        except Exception as e:
            print(f'Error in testio file: {testio_path}')
            raise e

        context = {
            'package_name': package_name,
            'module_name': self.parser.module_name,
            'ports': {
                'input': [{'name': port[0], 'highBit': port[1], 'lowBit': port[2]} for port in self.parser.input_ports],
                'output': [{'name': port[0], 'highBit': port[1], 'lowBit': port[2]} for port in self.parser.output_ports]
            },
            'tests': tests
        }
        with open(f'{dir_path}/{self.parser.module_name}Test.java', 'w', encoding='utf-8') as f:
            f.write(Template(template).render(context))