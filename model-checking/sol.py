from oxidd.bdd import BDDManager

def parse_dimacs(file_path):
    num_variables = None
    num_clauses = None
    variable_order = []
    clauses = []

    with open(file_path, 'r') as f:
        for line in f:
            tokens = line.strip().split()

            if not tokens or tokens[0] == 'c':
                if tokens[1] == 'vo':
                    variable_order = list(map(int, tokens[2:]))
                continue

            if tokens[0] == 'p' and tokens[1] == 'cnf':
                num_variables = int(tokens[2])
                num_clauses = int(tokens[3])
            else:
                clause = list(map(int, tokens[:-1]))  
                clauses.append(clause)

    return num_variables, num_clauses, variable_order, clauses

num_variables, num_clauses, variable_order, clauses = parse_dimacs(file_path='model-checking/conf-dimacs/busybox.dimacs')

manager = BDDManager(100_000_000, 1_000_000, 8)
variables = [manager.new_var() for i in range(num_variables)]

if len(clauses[0]) == 1:
    if clauses[0][0] > 0:
        first_clause = variables[abs(clauses[0][0])-1]
    else:
        first_clause = variables[abs(clauses[0][0])-1].__invert__() 
else:
    if ((clauses[0][0]) > 0 and (clauses[0][1]) > 0):
        first_clause = (variables[abs(clauses[0][0])-1]).__or__(variables[abs(clauses[0][1])-1])
    elif ((clauses[0][0]) > 0 and (clauses[0][1]) < 0):
        first_clause = (variables[abs(clauses[0][0])-1]).__or__((variables[abs(clauses[0][1])-1].__invert__()))
    elif ((clauses[0][0]) < 0 and (clauses[0][1]) > 0):
        first_clause = ((variables[abs(clauses[0][0])-1].__invert__())).__or__(variables[abs(clauses[0][1])-1])
    else:
        first_clause = ((variables[abs(clauses[0][0])-1].__invert__())).__or__((variables[abs(clauses[0][1])-1].__invert__()))
if len(clauses[0]) > 2:
    for i in range(2, len(clauses[0])):
        if (clauses[0][i]) > 0:
            first_clause = first_clause.__or__(variables[abs(clauses[0][i])-1])
        else:
            first_clause = first_clause.__or__(variables[abs(clauses[0][i])-1].__invert__())

if len(clauses[1]) == 1:
    if clauses[1][0] > 0:
        second_clause = variables[abs(clauses[1][0])-1]
    else:
        second_clause = variables[abs(clauses[1][0])-1].__invert__() 
else:
    if ((clauses[1][0]) > 0 and (clauses[1][1]) > 0):
        second_clause = (variables[abs(clauses[1][0])-1]).__or__(variables[abs(clauses[1][1])-1])
    elif ((clauses[1][0]) > 0 and (clauses[1][1]) < 0):
        second_clause = (variables[abs(clauses[1][0])-1]).__or__((variables[abs(clauses[1][1])-1].__invert__()))
    elif ((clauses[1][0]) < 0 and (clauses[1][1]) > 0):
        second_clause = ((variables[abs(clauses[1][0])-1].__invert__())).__or__(variables[abs(clauses[1][1])-1])
    else:
        second_clause = ((variables[abs(clauses[1][0])-1].__invert__())).__or__((variables[abs(clauses[1][1])-1].__invert__()))
if len(clauses[1]) > 2:
    for i in range(2, len(clauses[1])):
        if (clauses[1][i]) > 0:
            second_clause = second_clause.__or__(variables[abs(clauses[1][i])-1])
        else:
            second_clause = second_clause.__or__(variables[abs(clauses[1][i])-1].__invert__())  

cnf_bdd = first_clause.__and__(second_clause)

if len(clauses) > 2:
    for clause in clauses[2:]:
        if len(clause) == 1:
            if clause[0] > 0:
                clause_f = variables[abs(clause[0])-1]
            else:
                clause_f = variables[abs(clause[0])-1].__invert__() 
        else:
            if ((clause[0]) > 0 and (clause[1]) > 0):
                clause_f = (variables[abs(clause[0])-1]).__or__(variables[abs(clause[1])-1])
            elif ((clause[0]) > 0 and (clause[1]) < 0):
                clause_f = (variables[abs(clause[0])-1]).__or__((variables[abs(clause[1])-1].__invert__()))
            elif ((clause[0]) < 0 and (clause[1]) > 0):
                clause_f = ((variables[abs(clause[0])-1].__invert__())).__or__(variables[abs(clause[1])-1])
            else:
                clause_f = ((variables[abs(clause[0])-1].__invert__())).__or__((variables[abs(clause[1])-1].__invert__()))
        if len(clause) > 2:
            for i in range(2, len(clause)):
                if (clause[i]) > 0:
                    clause_f = clause_f.__or__(variables[abs(clause[i])-1])
                else:
                    clause_f = clause_f.__or__(variables[abs(clause[i])-1].__invert__())  
        
        cnf_bdd = cnf_bdd.__and__(clause_f)   

print('diocane')

'''
permessive configuration process

take all the feature in the right order.

for each of the feature check if it is contained in one of the clauses.
if not select it (insert into F/E set)
otherwise, select it (insert into E set [permessive configuration]) check if the new bdd is satisfiable, if yes go on
if not go back (remove from E set [permessive configuration] the feature) and deselect the feature you are considering.

'''



'''
RESULTS

(A) the total number of valid configurations

buildroot: 1.979294126137951e+158

busybox: 

embtoolkit: 

toybox: 

uClinux: 

'''