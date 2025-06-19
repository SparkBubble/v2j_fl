# 0 到 15 循环
for i in {0..15}
do
    # 运行15 个 fadd32 模块的定位测试
    python main.py generator/test/fadd32_$i.v
done