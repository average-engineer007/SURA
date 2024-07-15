import gurobipy as gp
from gurobipy import GRB
import time

model = gp.Model("neural_network")


# b1 = model.addVar(vtype=GRB.BINARY, name="b1")
# b2 = model.addVar(vtype=GRB.BINARY, name="b2")
t=model.addVar(name='t', lb=-GRB.INFINITY, ub=GRB.INFINITY)
l= model.addVar(name='l', lb=-GRB.INFINITY, ub=GRB.INFINITY)
# model.addConstr(t >= 14,"b1")
# model.addConstr(l == 7.6,"b2")
# model.addConstr(l == 8)
# model.addGenConstrOr(b1, [b2], name="implication")
z = model.addVar(vtype=GRB.BINARY, name="z")
model.addConstr(t==15)
model.addConstr(l==0)
# Add constraints to define z based on t > 14
model.addGenConstrIndicator(z, True, t >= 14.01, name="z_t_greater_14")
model.addGenConstrIndicator(z, True, l >= 0.01, name="l_positive_if_z")
a = model.addVar(vtype=GRB.BINARY, name="a")

# Create binary variable for not a
not_a = model.addVar(vtype=GRB.BINARY, name="not_a")
# Add constraints for not a: not_a = 1 when a = 0, not_a = 0 when a = 1
model.addConstr(a==1)
model.addConstr(not_a==1)
model.addConstr(a + not_a == 1, "not_a_constraint")

# Add the implication constraint: if z == 1 (i.e., t > 14) then l > 0
# model.addConstr((z == 1) >> (l >= 0.01), name="l_positive_if_z")

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