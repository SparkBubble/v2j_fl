import re
from collections import defaultdict, deque
from convert.wire import wire

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
        self._get_graph()
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
    
    def _get_graph(self):
        # 邻接表
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)

        # 根据赋值语句构建有向图
        for var, lb, rb, expr in self.assignments:
            match = re.findall(r'\b(\w+)\b', expr)
            for dep_var in match:
                if dep_var in self.variables_dict:
                    self.graph[dep_var].append(var.name)
                    self.in_degree[var.name] += 1


    def _topological_sort(self):
        queue = deque([node for node in self.graph if self.in_degree[node] == 0])
        sorted_nodes = []

        while queue:
            node = queue.popleft()
            sorted_nodes.append(node)
            for neighbor in self.graph[node]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # 检查是否有循环依赖
        if len(sorted_nodes) != len(self.graph):
            raise ValueError("The verilog code has a cycle.")

        # 按照拓扑顺序重新组织赋值语句
        self.sorted_assignments = sorted(self.assignments, key=lambda x: sorted_nodes.index(x[0].name))
        self.sorted_variables = sorted(self.variables, key=lambda x: sorted_nodes.index(x.name))

    def calculate_distance(self, start_name: str, end_name: str) -> int | None:
        if start_name not in self.variables_dict or end_name not in self.variables_dict:
            raise ValueError("One or both of the specified variables are not defined.")

        queue = deque([(start_name, 0)])
        visited = set()

        while queue:
            node, distance = queue.popleft()
            if node == end_name:
                return -distance
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph[node]:
                    if neighbor not in visited:
                        queue.append((neighbor, distance + 1))

        queue = deque([(end_name, 0)])
        visited = set()

        while queue:
            node, distance = queue.popleft()
            if node == start_name:
                return distance
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph[node]:
                    if neighbor not in visited:
                        queue.append((neighbor, distance + 1))

        return None  # 如果没有找到路径，返回None

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
