# 在指定目录下将 Verilog 文件转换为 Java ，并生成 Java 项目
# 项目名为 Verilog 文件名，请注意重名问题
# 以标准 io 文件为基准，生成单元测试



# * 以下参数需要根据实际情况修改
verilog_file_path = 'test_dir/wrong_code/fadd32_3_nobranch.v'  # 输入Verilog文件路径

verilog_io_path = 'generator/testdata/fadd32.io10000'  # 输入Verilog IO文件路径
ports_resort = [1, 2, 0, 3, 4] # 模块上数第 i 个端口位于IO文件第左数 p[i] 列
samp_rate = 0.1  # IO测试采样率（0~1之间，数值越大越准确，但是测试时间与其成正比）

max_ranking = 10  # 输出排名最高的 max_ranking 个变量

java_project_parentDir = 'test_dir/prjs'  # 生成的Java项目放到哪个目录下
output_dir = 'test_dir/output'  # 输出放到哪个目录下

# ? 以下参数一般无需修改

java_tools_dir = 'java_tools'  # 生成工具目录
java_package_name =  'module'  # Java包名

parser_detail = True  # 是否使用详细语法分析器



# ! 以下代码无需修改

from convert.converter import Verilog2JavaConverter as V2JStd
from convert.converter_detail import Verilog2JavaConverter as V2JDtl
import os, shutil, sys
import subprocess
import re

def generate_project(project_name:str):
    if not os.path.exists(java_project_parentDir):
        os.mkdir(java_project_parentDir)
    pwd = os.getcwd()
    os.chdir(java_project_parentDir)
    if os.path.exists(project_name):
        print(f'项目 {project_name} 于 {os.path.join(java_project_parentDir, project_name)} 已存在，也许您想要先删除它.')
        # 询问是否删除
        while True:
            choice = input('是否删除它? ([y]/n) ')
            if choice.lower() == 'y' or choice.lower() == '':
                shutil.rmtree(project_name)
                break
            elif choice.lower() == 'n':
                os.chdir(pwd)
                return os.path.join(java_project_parentDir, project_name)
    # 创建maven项目
    print(f'创建 maven 项目 {project_name}...')
    print('------------------------------------------------')
    subprocess.run(['mvn', 
                    'archetype:generate', 
                    '-DarchetypeArtifactId=maven-archetype-quickstart', 
                    '-DartifactId=' + project_name, 
                    '-DgroupId=' + java_package_name, 
                    '-DinteractiveMode=false'])
    print('------------------------------------------------')
    print(f'Maven 项目 {project_name} 创建完毕。\n\n')
    os.chdir(pwd)



def generate_result(project_path:str):
    project_name = os.path.basename(project_path)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if os.path.exists(os.path.join(output_dir, project_name)):
        shutil.rmtree(os.path.join(output_dir, project_name))
    os.mkdir(os.path.join(output_dir, project_name))
    print(f'\n获取结果...')
    shutil.copy(verilog_file_path, os.path.join(output_dir, project_name))

    result_file = os.path.join(project_path, 'build', 'sfl', 'txt', 'ochiai.ranking.csv')
    ranking_lines = []
    if os.path.exists(result_file):
        with open(result_file, 'r', encoding='utf-8') as f:
            ranking_lines = f.readlines()
            with open(os.path.join(output_dir, project_name, f'java_ranking.csv'), 'w', encoding='utf-8') as f:
                f.writelines(ranking_lines)
    else:
        print(f'结果文件不存在！')
    print(f'结果已保存至{os.path.join(output_dir, project_name)}')
    
    java_lines = []
    with open(os.path.join(project_path, 'src', 'main', 'java', java_package_name, java_file_name), 'r', encoding='utf-8') as f:
        java_lines = f.readlines()
        with open(os.path.join(output_dir, project_name, java_file_name), 'w', encoding='utf-8') as f:
            f.writelines(java_lines)
            
    verilog_ranking = []
    wrong_var_names = []
    pattern = re.compile(r'module\$(\w+)#(\w+)\(\):(\d+);(\d+\.\d+)')
    for line in ranking_lines[:max_ranking+1]:
        match = pattern.match(line)
        if match:
            class_name, func_name, line_num, score = match.groups()
            if func_name != 'compute':
                continue
            line_num = int(line_num) - 1
            i = j = line_num
            while java_lines[i+1].strip() != '':
                i += 1
            while java_lines[j-1].strip() != '':
                j -= 1

            var_name = java_lines[i].strip().split('.')[0]
            wrong_var_names.append(var_name)
            verilog_ranking.append(f'module: {class_name}\n')
            verilog_ranking.append(f'    var: {var_name}\n')
            verilog_ranking.append(f'    line: {line_num+1}\n')
            verilog_ranking.append(f'    score: {score}\n')
            verilog_ranking.append(f'------------\n')
            for k in range(j, i+1):
                verilog_ranking.append(f'{k+1}{"(this) " if k == line_num else "       "}: {java_lines[k][5:].replace(".notZero()", "")}')
            verilog_ranking.append(f'------------\n\n')
    with open(os.path.join(output_dir, project_name, f'verilog_ranking.txt'), 'w', encoding='utf-8') as f:
        f.writelines(verilog_ranking)
    with open(os.path.join(output_dir, project_name, f'wrong_var_names.txt'), 'w', encoding='utf-8') as f:
        f.writelines([f'{name}\n' for name in wrong_var_names])



if __name__ == '__main__':
    args = sys.argv[1:]
    if args and len(args) > 0 :
        verilog_file_path = args[0]
    if args and len(args) > 1 :
        output_dir = args[1]


    # 生成项目
    project_name = os.path.basename(verilog_file_path).split('.')[0]
    project_path = os.path.join(java_project_parentDir, project_name)

    generate_project(project_name)
    
    # 删除原有文件
    try:
        os.remove(os.path.join(project_path, 'pom.xml'))
        os.remove(os.path.join(project_path, 'src', 'test', 'java', java_package_name, 'AppTest.java'))
        os.remove(os.path.join(project_path, 'src', 'main', 'java', java_package_name, 'App.java'))
    except:
        pass

    # 载入Verilog文件
    print(f'载入Verilog文件 ———— {verilog_file_path}')
    if parser_detail:
        converter = V2JDtl(verilog_file_path)
    else:
        converter = V2JStd(verilog_file_path)
    print(f'解析Verilog文件 ———— {verilog_file_path}\n')
    # converter.parser_log('parser.log')

    # 生成模块和单元测试
    print(f'生成模块Java代码...')
    dir = os.path.join(project_path, 'src', 'main', 'java', java_package_name)
    java_file_name = converter.toJava(dir, java_package_name)
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
    generate_result(project_path)
