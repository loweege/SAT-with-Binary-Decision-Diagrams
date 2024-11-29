from z3 import *
import random

num_matches = 32
num_days = 32
num_fields = 3
num_priorities = 6

M_d = [Int(f"M_d_{i}") for i in range(num_matches)] 
M_start = [Int(f"M_s_{i}") for i in range(num_matches)] 
M_end = [Int(f"M_e_{i}") for i in range(num_matches)] 
M_p = [Int(f"M_p_{i}") for i in range(num_matches)]  
M_f = [Int(f"M_f_{i}") for i in range(num_matches)] 
M_duration = [Int(f"M_dur_{i}") for i in range(num_matches)]  

solver = Optimize()

'''Change seed to have a different set sample'''
seed = '2IMF25'
random.seed(seed)
for i in range(num_matches):
    variation = random.randint(-20, 20)
    solver.add(M_duration[i] == 110 + variation)

'''Generation of priorities'''
for _ in range(num_matches):
    if _ < 16:
        M_p[_] = 1
    elif _ >= 16 and _ < 24:
        M_p[_] = 2
    elif _ >= 24 and _ < 28:
        M_p[_] = 3
    elif _ >= 28 and _ < 30:
        M_p[_] = 4
    elif _ >= 30 and _ < 31:
        M_p[_] = 5         
    else:
        M_p[_] = 6

for i in range(num_matches):
    solver.add(M_end[i] == M_start[i] + M_duration[i])
    solver.add(M_start[i] >= 14*60) 
    solver.add(M_end[i] <= 24*60) 

for i in range(num_matches):
    for j in range(i+1, num_matches):
        and_condition = And(M_d[i] == M_d[j], M_f[i] == M_f[j])
        or_condition = Or(M_start[j] > M_end[i], M_end[j] < M_start[i])
        solver.add(Implies(and_condition, or_condition))

for i in range(num_matches):
    for j in range(num_matches):
        if i != j:
            solver.add(Implies(M_p[i] < M_p[j], M_d[i] < M_d[j]))

for i in range(num_matches):
    solver.add(And(M_f[i] >= 1, M_f[i] <= num_fields))

for i in range(num_days):
    solver.add(And(M_d[i] >= 0, M_d[i] <= num_days))

max_day = Int("max_day")
solver.add(max_day >= 6)
for i in range(num_matches):
    solver.add(M_d[i] <= max_day)
solver.minimize(max_day)

if solver.check() == sat:
    model = solver.model()
    min_days = model[max_day].as_long()
    print(f"Minimum number of days needed: {min_days + 1}")
    for i in range(num_matches):
        print(f"Match {i + 1}: Day {model[M_d[i]]}, Start {model[M_start[i]]}, "
              f"End {model[M_end[i]]}, Field {model[M_f[i]]}, Priority {M_p[i]}")
else:
    print("No solution found.")