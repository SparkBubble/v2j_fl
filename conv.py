# example for converting Verilog to Java


# 单值语法分析器
from convert.converter import Verilog2JavaConverter as v2j_simple

# 全值语法分析器
from convert.converter_detail import Verilog2JavaConverter as v2j_full

# converter_class = v2j_simple
converter_class = v2j_full

converter = converter_class('generator/test/fadd32_1.v')
converter.toJava('.')