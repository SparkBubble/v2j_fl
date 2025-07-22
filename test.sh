
a='_nobranch'

for i in {1..15}
do
    python main.py test_dir/wrong_code/fadd32_$i$a.v
done