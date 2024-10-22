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

num_variables, num_clauses, variable_order, clauses = parse_dimacs(file_path='model-checking/conf-dimacs/example3.dimacs')

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

print('betis')




'''
#cmon = cnf_bdd.cofactor_false().__or__(cnf_bdd.cofactor_true())
cmon = cnf_bdd.pick_cube_dd_set(variables[1])
cmon = cmon.pick_cube_dd_set(variables[2])
'''



'''limited_variables = variables[1].__and__(variables[2].__invert__())
restricted_bdd = cnf_bdd.__and__(limited_variables)'''


'''limited_variables = variables[1].__and__(variables[2].__invert__())
limited_variables = limited_variables.__and__(variables[0])
restricted_bdd = cnf_bdd.__and__(limited_variables)'''

limited_variables = variables[0].__and__(variables[1])
restricted_bdd = cnf_bdd.__and__(limited_variables)

s1 = variables[1].__or__(variables[2])
c1 = s1.__or__(variables[4])

c2 = (variables[2]).__or__(variables[4].__invert__())

form = c1.__and__(c2)




set_of_literals_1 = variables[1].__and__(variables[2])

set_of_literals_2 = variables[1].__and__(variables[2].__invert__())

g = form.pick_cube_dd_set(variables[1].__and__(variables[2]))



cmon = cnf_bdd.pick_cube_dd_set(set_of_literals_1)

cmon = cmon.pick_cube_dd_set(variables[1])
cmon = cmon.pick_cube_dd_set(variables[2])
cmon = cmon.pick_cube_dd_set(variables[3])
cmon = cmon.pick_cube_dd_set(variables[4])



cmon = cmon.cofactor_true().__and__(cmon)
cmon = cmon.cofactor_true().__and__(cmon)

supp = cmon.cofactor_false().__or__(cmon.cofactor_true())
cmon = cmon.__and__(supp)

supp = cmon.cofactor_false().__or__(cmon.cofactor_true())
cmon = cmon.__and__(supp)

cnf_bdd = cnf_bdd.cofactor_false()

first_branch = cnf_bdd.cofactor_false()
first_branch = first_branch.cofactor_true()

second_branch = cnf_bdd.cofactor_false()
second_branch = second_branch.cofactor_true()
second_branch = second_branch.cofactor_true()

final = first_branch.__and__(second_branch)

cnf_bdd = cnf_bdd.cofactor_false()
cnf_bdd = cnf_bdd.cofactor_false()
cnf_bdd = cnf_bdd.cofactor_false()





cnf_bdd = cnf_bdd.cofactor_false().__and__(cnf_bdd.cofactor_true())

E = []
CF = [0] * num_clauses
FE = []
clauses_indeces = []
is_in_FE = True
for feature in variable_order:
    is_in_FE = True
    #if it is in none of the clauses
    for clause_idx in range(len(clauses)):
        for literal_idx in range(len(clauses[clause_idx])):
            if abs(clauses[clause_idx][literal_idx]) == feature:
                if CF[clause_idx] == 0:
                    is_in_FE = False
                    CF[clause_idx] = 1
    if is_in_FE:
        FE.append(feature)
        cnf_bdd = cnf_bdd.cofactor_true()
    else:
        E.append(feature)
        if clauses[clause_idx][literal_idx] > 0:
            cnf_bdd = cnf_bdd.cofactor_true()
        else:
            cnf_bdd = cnf_bdd.cofactor_false()

print('help')

'''
toybox sample
-56 55 0
-342 0
56 -55 0
-139 0
-343 0
24 -55 0
-140 0
-344 0
-141 0
'''