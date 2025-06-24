import re
from collections import defaultdict, deque
from jinja2 import Template

from convert.v2j_yacc import parser

class wire:
    def __init__(self, name, lb, rb):
        self.name:str = name
        self.highBit:int = lb
        self.lowBit:int = rb

class VerilogParser:
    def __init__(self, code_path):
        with open(code_path, 'r', encoding='utf-8') as f:
            self.code = f.read()
        self.body = ''
        self.input_ports:list[tuple[str, int, int]] = []
        self.output_ports:list[tuple[str, int, int]] = []
        self.module_name = ''
        self.assignments:list[tuple[wire, int, int, str]] = []
        self.variables:list[wire] = []
        self.variables_dict:dict[str, wire] = {}
        self._preprocess()
        self._parse_module()
        self._parse_body()
        self._topological_sort()

    # 预处理
    def _preprocess(self):
        # 移除单行注释
        self.code = re.sub(r'//.*?\n', '', self.code)
        # 移除多行注释
        self.code = re.sub(r'/\*.*?\*/\n', '', self.code, flags=re.DOTALL)
        # 合并跨行语句
        self.code = re.sub(r'\s+', ' ', self.code).replace('; ', ';\n')
        # 移除所有空格
        self.code = self.code.replace(' ', '')
    
    
    def _parse_var(self, var_str):
        if not var_str:
            return None, None, None
        
        match = re.match(r'(\w+)(?:\[(\d+)(?::(\d+))?\])?', var_str)
        if match:
            var = match.group(1) or None
            lb = match.group(2) or None
            rb = match.group(3) or lb or None
            return var, lb, rb
        else:
            return None, None, None


    def _parse_ports(self, port_str):
        # 匹配端口定义
        port_pattern = r'\b(input|output)\b(?:reg|wire)?(?:\[(\d+):(\d+)\])?(\w+)'
        for match in re.finditer(port_pattern, port_str):
            direction = match.group(1)
            lb = int(match.group(2)) if match.group(2) else 0
            rb = int(match.group(3)) if match.group(3) else 0
            name = match.group(4)
            if direction == 'input':
                self.input_ports.append((name, lb, rb))
            else:
                self.output_ports.append((name, lb, rb))
            portvar = wire(name, lb, rb)
            self.variables_dict[name] = portvar
            
        
    def _parse_module(self):
        # 解析模块主体
        module_pattern = r'module(\w+)\(([^)]*)\);\n(.*?)endmodule'
        match = re.search(module_pattern, self.code, re.DOTALL)
        if match:
            self.module_name = match.group(1)
            self._parse_ports(match.group(2))
            self.body = match.group(3)

    def _parse_body(self):
        # 解析所有 wire 声明 及（可能带有赋值）
        wire_pattern = r'wire(?:\[(\d+)\:(\d+)\])?(.*?)(?:=(.*?))?;'
        for lb, rb, name, expr in re.findall(wire_pattern, self.body, re.DOTALL):
            lb = 0 if not lb else int(lb)
            rb = 0 if not rb else int(rb)

            wirevar = wire(name, lb, rb)
            self.variables.append(wirevar)
            self.variables_dict[name] = wirevar
            if expr :
                self.assignments.append((wirevar, lb, rb, expr))

        # 解析所有 assign 语句
        assign_pattern = r'assign(.*?)=(.*?);'
        for ls, expr in re.findall(assign_pattern, self.body, re.DOTALL):
            name, lb, rb = self._parse_var(ls.strip())
            if not name or (name not in self.variables_dict):
                raise ValueError("Undefined variable '{}' in assignment statement.".format(name))
            
            var = self.variables_dict[name]

            if not lb:
                lb, rb = var.highBit, var.lowBit
            else:
                lb = int(lb)
                rb = int(rb) if rb else lb

            expr = re.sub(r'\s+', ' ', expr.strip())
            self.assignments.append((var, lb, rb, expr))

    def _topological_sort(self):
        # 邻接表
        graph = defaultdict(list)
        in_degree = defaultdict(int)

        # 根据赋值语句构建有向图
        for var, lb, rb, expr in self.assignments:
            match = re.findall(r'\b(\w+)\b', expr)
            for dep_var in match:
                if dep_var in self.variables_dict:
                    graph[dep_var].append(var.name)
                    in_degree[var.name] += 1
        
        queue = deque([node for node in graph if in_degree[node] == 0])
        sorted_nodes = []

        while queue:
            node = queue.popleft()
            sorted_nodes.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # 检查是否有循环依赖
        if len(sorted_nodes) != len(graph):
            raise ValueError("The verilog code has a cycle.")

        # 按照拓扑顺序重新组织赋值语句
        self.sorted_assignments = sorted(self.assignments, key=lambda x: sorted_nodes.index(x[0].name))
        self.sorted_variables = sorted(self.variables, key=lambda x: sorted_nodes.index(x.name))

    def log(self, log_path):
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('module_name: {}\n'.format(self.module_name))

            f.write('\nports:\n')
            for port in self.input_ports:
                port_str = 'input ' + port[0]
                if port[1] :
                    port_str += '[{}:{}]'.format(port[1], port[2])
                f.write('\t{}\n'.format(port_str))
            for port in self.output_ports:
                port_str = 'output ' + port[0]
                if port[1] :
                    port_str += '[{}:{}]'.format(port[1], port[2])
                f.write('\t{}\n'.format(port_str))

            f.write('\nvariables:\n')
            for var in self.sorted_variables:
                var_str = var.name
                if var.highBit != 0:
                    var_str += '[{}:{}]'.format(var.highBit, var.lowBit)
                f.write('\t{}\n'.format(var_str))
            
            
            f.write('\nassignments(sorted topologically):\n')
            for assign in self.sorted_assignments:
                assign_str = '{}'.format(assign[0].name)
                if assign[1] != -1:
                    if assign[0].highBit != assign[1] or assign[0].lowBit != assign[2]:
                        if assign[1] == assign[2]:
                            assign_str += '[{}]'.format(assign[1])
                        else:
                            assign_str += '[{}:{}]'.format(assign[1], assign[2])
                assign_str += ' = {}'.format(assign[3])
                f.write('\t{}\n'.format(assign_str))


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