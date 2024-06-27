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


file_path = 'output.txt'

n, l, weights, biases = parse_file(file_path)

vars = []
s = Solver()

for i in range(len(l)):
    temp = []
    for j in range(l[i]):
        temp.append(Real(f'v_{i+1}_{j+1}'))
    vars.append(temp)

z=[]
for i in range(len(l)):
    for j in range(l[i]):
        if i == len(l) - 1:
            current = vars[i][j]
            w = weights[i][j]
            prev_layer_vars = vars[i-1]
            a_w = [w[k] * prev_layer_vars[k] for k in range(l[i-1])]
            a_w.append(biases[i][j])
            z.append(Real(f'z_{j+1}'))
            s.add(current == ((math.e)**Sum(a_w)))
            # s.add(current == Sum(a_w))
        elif i != 0:
            current = vars[i][j]
            w = weights[i][j]
            prev_layer_vars = vars[i-1]
            a_w = [w[k] * prev_layer_vars[k] for k in range(l[i-1])]
            a_w.append(biases[i][j])
            s.add(Or(current == Sum(a_w), current == 0))
            s.add(current >= 0)
            s.add(current >= Sum(a_w))
sum=Real('sum')
n=len(l)-1
s.add(sum==Sum(vars[n]))
# # # final=[ (vars[n][i]/sum) for i in range (l[n]) ] 
for j in range(l[n]):                   
    s.add(z[j]==vars[n][j]/19.923)




# image_array=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 226, 27, 212, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 218, 226, 0, 0, 0, 0, 0, 75, 33, 225, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 175, 14, 143, 0, 0, 0, 0, 199, 7, 127, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 84, 94, 0, 0, 0, 0, 0, 120, 3, 210, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 118, 0, 0, 0, 0, 0, 94, 2, 210, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 230, 17, 119, 0, 0, 0, 0, 0, 11, 12, 218, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 34, 108, 249, 0, 0, 0, 0, 2, 50, 253, 249, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 118, 3, 87, 222, 0, 0, 0, 2, 16, 65, 187, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 239, 82, 2, 1, 87, 95, 61, 1, 2, 143, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 253, 166, 83, 50, 50, 33, 2, 179, 252, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 163, 2, 233, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 129, 2, 233, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 249, 52, 46, 247, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 232, 3, 122, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 157, 3, 205, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 107, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 209, 2, 61, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 192, 3, 113, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 118, 22, 243, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 118, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# input = [x / 255 for x in image_array]
# for i in range(l[0]):
#     s.add(And(vars[0][i]<=1,vars[0][i]>=0))


l=[]
for i in range(28):
    l.append(vars[0][28*i+14])
s.add(And(Sum(l)>=14,vars[3][1]<0))


start_time = time.time()
if s.check() == sat:
    model = s.model()
    # print(model)
    print("Found solution")
    with open('answers.txt', 'w') as f:
        for d in model.decls():
            f.write(f"{d.name()} = {model[d]}\n")
else:
    print("No valid solution found")

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Time taken: {elapsed_time} seconds")