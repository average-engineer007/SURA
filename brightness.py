import gurobipy as gp
from gurobipy import GRB
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


# parse the text file and extract weights and biases
file_path = 'weight_biases_4_nodes.txt'

n, l, weights, biases = parse_file(file_path)

model = gp.Model("neural_network")

# function to encode the neural network
def encode_neural_network(x, y, ans_var, k):
    vars = []
    for i in range(len(l)):
        temp = []
        if i==0:
            vars.append(x)
        elif i==len(l)-1:
            vars.append(y)
        else:
            for j in range(l[i]):
                temp.append(model.addVar(name=f'v_{k}_{i+1}_{j+1}', lb=-GRB.INFINITY, ub=GRB.INFINITY))
            vars.append(temp)

    for i in range(len(l)):
        for j in range(l[i]):
            if i == len(l) - 1:
                current = vars[i][j]
                w = weights[i][j]
                prev_layer_vars = vars[i-1]
                a_w = gp.LinExpr(w, prev_layer_vars) + biases[i][j]
                model.addConstr(current == a_w)
            elif i != 0:
                current = vars[i][j]
                w = weights[i][j]
                prev_layer_vars = vars[i-1]
                a_w = gp.LinExpr(w, prev_layer_vars) + biases[i][j]
                pre_relu = model.addVar(name=f'pre_relu_{k}_{i+1}_{j+1}', lb=-GRB.INFINITY, ub=GRB.INFINITY)
                model.addConstr(pre_relu == a_w)
                model.addGenConstrMax(current, [pre_relu, 0])
    max_var = model.addVar(name=f"max_{k}", lb=-GRB.INFINITY)

    is_max = [model.addVar(vtype=GRB.BINARY, name=f'is_max_{k}_{i}') for i in range(len(y))]

    model.addConstr(sum(is_max) == 1)

    for i in range(len(y)):
        model.addConstr(max_var >= y[i])
        model.addConstr(max_var <= y[i] + (1 - is_max[i]) * 1e6)  
    for i in range(len(y)):
        model.addConstr(ans_var >= i - (1 - is_max[i]) * 1e6)  
        model.addConstr(ans_var <= i + (1 - is_max[i]) * 1e6)  


# define the input and output variables and call the encoding function 
x1=[]
for i in range(l[0]):
    x1.append(model.addVar(name=f'x1_{i+1}', lb=0, ub=1))
y1=[]
for i in range(l[len(l)-1]):
    y1.append(model.addVar(name=f'y1_{i+1}', lb=-GRB.INFINITY, ub=GRB.INFINITY))
x2=[]
for i in range(l[0]):
    x2.append(model.addVar(name=f'x2_{i+1}', lb=0, ub=1))
y2=[]
for i in range(l[len(l)-1]):
    y2.append(model.addVar(name=f'y2_{i+1}', lb=-GRB.INFINITY, ub=GRB.INFINITY))


ans_1 = model.addVar(name="ans_1", vtype=GRB.INTEGER)
ans_2 = model.addVar(name="ans_2", vtype=GRB.INTEGER)
encode_neural_network(x1,y1,ans_1,1)
encode_neural_network(x2,y2,ans_2,2)


# define the encoding of the property

for i in range(len(x1)):
    model.addConstr(x2[i] == x1[i] + 0.0005)
M = 1e6

not_equal = model.addVar(vtype=GRB.BINARY, name="not_equal")

model.addConstr(ans_1 - ans_2 >= 1 - M * not_equal)
model.addConstr(ans_1 - ans_2 <= -1 + M * (1 - not_equal))


model.addConstr(not_equal == 1)


# Set the objective (minimizing a dummy variable to find any feasible solution)
dummy = model.addVar(name="dummy")
model.setObjective(dummy, GRB.MINIMIZE)

# Solve the model
start_time = time.time()
model.optimize()

# Check the results
if model.Status == GRB.OPTIMAL:
    print("Found solution")
    with open('answers.txt', 'w') as f:
        for v in model.getVars():
            f.write(f"{v.VarName} = {v.X}\n")
else:
    print("No valid solution found")

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Time taken: {elapsed_time} seconds")