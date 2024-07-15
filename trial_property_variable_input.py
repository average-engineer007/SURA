from z3 import *
import time

def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    data = {}
    for line in lines:
        key, value = line.strip().split('=')
        data[key] = eval(value)
    
    n = data['n']
    l = data['l']
    weights = data['weights']
    biases = data['biases']
    
    return n, l, weights, biases


file_path = 'weight_biases_5_nodes.txt'

n, l, weights, biases = parse_file(file_path)

vars = []
s = Solver()

for i in range(len(l)):
    temp = []
    for j in range(l[i]):
        temp.append(Real(f'v_{i+1}_{j+1}'))
    vars.append(temp)

for i in range(len(l)):
    for j in range(l[i]):
        if i == len(l) - 1:
            current = vars[i][j]
            w = weights[i][j]
            prev_layer_vars = vars[i-1]
            a_w = [w[k] * prev_layer_vars[k] for k in range(l[i-1])]
            a_w.append(biases[i][j])
            s.add(current == Sum(a_w))
        elif i != 0:
            current = vars[i][j]
            w = weights[i][j]
            prev_layer_vars = vars[i-1]
            a_w = [w[k] * prev_layer_vars[k] for k in range(l[i-1])]
            a_w.append(biases[i][j])
            # Encoding 1
            s.add(Or(current == Sum(a_w), current == 0))
            s.add(current >= 0)
            s.add(current >= Sum(a_w))

            # Encoding 2
            # s.add(Implies(Sum(a_w)>0,current==Sum(a_w)))
            # s.add(Implies(Sum(a_w)<=0,current==0))

            # Encoding 3
            # s.add(current==If(Sum(a_w)>0,Sum(a_w),0))


# adding this makes the code run for infinity
for i in range(l[0]):
    s.add(And(vars[0][i]<=1,vars[0][i]>=0))


t=[]
for i in range(28):
    t.append(vars[0][28*i+14])
s.add(Not(Implies(Sum(t)>=14,vars[3][1]<0)))



start_time = time.time()
if s.check() == sat:
    print("Found solution")
    model = s.model()
    # print(model)
    with open('answers.txt', 'w') as f:
        for d in model.decls():
            f.write(f"{d.name()} = {model[d]}\n")
else:
    print("No valid solution found")

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Time taken: {elapsed_time} seconds")