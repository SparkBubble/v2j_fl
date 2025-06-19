
# 项目说明

- 实现了模拟`verilog`中`wire`变量的全部运算的java类———[wire.java](./java_tools/wire.java)
- 在此基础上利用语法制导翻译将纯组合逻辑的`verilog`代码转换为`java`代码。
- 使用标准IO结果生成其`JUnit`单元测试。
- 使用开源的错误定位工具 [gzoltar](https://github.com/gzoltar/gzoltar) 对转换后的`java`代码进行错误定位。
- 以此来完成对纯组合逻辑`verilog`代码的自动化错误定位。


# 项目目录结构

```
.
├── java_tools
│   ├── wire.java            # 实现 wire 类
│   ├── testall.java         # 利用标准IO文件测试 wire 类以及语法翻译
│   ├── gzoltaragent.jar     # gzoltar的 agent 发行包 (v1.7.4)
│   ├── gzoltarcil.jar       # gzoltar的 cil 发行包 (v1.7.4)
│   └── run.sh               # 用于在生成java项目中测试运行的脚本
├── convert
│   ├── converter.py         # 用于实现转换器（标准）
│   ├── converter_detail.py  # 转换器（详细）
│   ├── v2j_yacc.py          # 语法制导翻译器（标准）
│   ├── v2j_yacc_detail.py   # 语法制导翻译器（详细）
│   └── verilog_lex.py       # 用于语法制导翻译的词法分析器
├── README.md                # 项目说明文件
├── conv.py                  # 转换java的示例程序
└── main.py                  # 主程序
```

# 运行说明

## 安装依赖

#### python 依赖

- `python3.10+`

- `ply`
- `jinja2`
- `re`

``` bash
>>> sudo apt-get install python3.10
>>> python3.10 -m pip install --upgrade pip
>>> pip install ply jinja2 re
```

#### java 依赖

- `java 8+`
- `maven`

``` bash
>>> sudo apt-get install openjdk-8-jdk maven
```

## 运行

- 修改`main.py`中相关参数
- `python3 main.py`
- 结果会以`csv`格式输出到`$output_dir`目录下