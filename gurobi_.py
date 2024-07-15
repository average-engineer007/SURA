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

file_path = 'weight_biases_128_nodes.txt'
# file_path = 'output.txt'

n, l, weights, biases = parse_file(file_path)

# Create a new model
model = gp.Model("neural_network")

# Create variables
vars = []
for i in range(len(l)):
    temp = []
    for j in range(l[i]):
        temp.append(model.addVar(name=f'v_{i+1}_{j+1}', lb=-GRB.INFINITY, ub=GRB.INFINITY))
    vars.append(temp)

# Add constraints
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
            
            # ReLU implementation using binary variable
            # z = model.addVar(vtype=GRB.BINARY, name=f'z_{i+1}_{j+1}')
            # M = 1000  # A large constant, adjust if needed
            
            # model.addConstr(current >= a_w)
            # model.addConstr(current <= a_w + M * z)
            # model.addConstr(current >= 0)
            # model.addConstr(current <= M * (1 - z))
            pre_relu = model.addVar(name=f'pre_relu_{i+1}_{j+1}', lb=-GRB.INFINITY, ub=GRB.INFINITY)
            model.addConstr(pre_relu == a_w)
            model.addGenConstrMax(current, [pre_relu, 0])

# Add constraints for input layer
for i in range(l[0]):
    model.addConstr(vars[0][i] >= 0)
    model.addConstr(vars[0][i] <= 1)

# Add the final constraint
t = gp.LinExpr([1 for _ in range(28)], [vars[0][28*i+14] for i in range(28)])
# model.addConstr((t >= 14) >> (vars[3][1] >= 0))
M = 1000  # A large constant
b = model.addVar(vtype=GRB.BINARY, name="b")
model.addConstr(t - 14 <= M * b)
model.addConstr(vars[3][1] >= -M * (1 - b)) 

# b1 = model.addVar(vtype=GRB.BINARY, name="b1")
# b2 = model.addVar(vtype=GRB.BINARY, name="b2")
# model.addConstr(t >= 14,"b1")
# model.addConstr(vars[3][1] >= 0,"b2")
# model.addGenConstrOr(b1, [b2], name="implication")


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