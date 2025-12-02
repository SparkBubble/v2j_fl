from convert.parser import VerilogParser
from verilog_covered.tools import Fault_Locate_Analyzer_Factory
from collections import defaultdict

# wrong_vars = {
#     2 : ['resultant_sign'],
#     5 : ['exp_diff'],
#     10 : ['is_nan'],
#     11 : ['resultant_sign'],
#     12 : ['need_swap'],
#     13 : ['round_up'],
#     14 : ['mant_ext_a'],
#     16 : ['mant_a'],
#     17 : ['exp_ext_a', 'exp_ext_b'],
#     18 : ['result_sign_nan'],
#     19 : ['exp_diff'],
#     20 : ['result_mant_nan']
# }

faulty_vars="rounded_exp round_up round_up round_up round_up round_up smaller_sticky need_swap real_shift_norm normalized_exp normalized_mantissa exp_ext_a result_sign_opposite result_sign_inf result_mant_nan"
wrong_vars = defaultdict(list)
for i, var in enumerate(faulty_vars.split()):
    wrong_vars[i+1].append(var)

def dist_factor(x, d, zero=4, e=2):
    """
    采用非线性的e次函数，距离为0的时候比例为1，距离为zero的时候比例为0
    """
    return x * (1 - (d / zero) ** e) if d >= 0 and d < zero else 0 

# for i in [2, 5, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20]:
#     dir = f"ljq_wrongcode/output/fadd32_{i}"
#     parser = VerilogParser(f"{dir}/fadd32_{i}.v")

for i in range(1, 16):
    dir = f"test_dir/output/fadd32_{i}_nobranch"
    parser = VerilogParser(f"{dir}/fadd32_{i}_nobranch.v")
    
    wrong_var = wrong_vars[i]
    locate_var_file = f"{dir}/wrong_var_names.txt"
    locate_vars = []
    with open(locate_var_file, 'r') as f:
        locate_vars = f.read().splitlines()
    dists = {}
    for wvar in wrong_var:
        dists[wvar] = {}
    for lvar in locate_vars:
        if dists.get(lvar) is None:
            dists[lvar] = {}
        for wvar in wrong_var:
            dis = parser.calculate_distance(wvar, lvar)
            dis = dis if dis is not None else float('inf')
            dists[wvar][lvar] = dis
            dists[lvar][wvar] = -dis

    analyzer = Fault_Locate_Analyzer_Factory().create(dists, vars_limit=10, dist_factor=dist_factor, type=4)

    locate_vars_with_weight = []
    for ith, lvar in enumerate(locate_vars):
        locate_vars_with_weight.append((lvar, 10 - ith))
        
    
    score = -1e9
    for wvar in wrong_var:
        score = max(score, analyzer.analyse(wvar, locate_vars_with_weight))
    
    print(f"score of {i} is {score}")