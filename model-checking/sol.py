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

num_variables, num_clauses, variable_order, clauses = parse_dimacs(file_path='model-checking/conf-dimacs/example2.dimacs')

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






def selective_configuration(num_clauses, variable_order, clauses):
    E = [] 
    assignment = {} 

    relevant_variables = set()
    for clause in clauses:
        for literal in clause:
            relevant_variables.add(abs(literal))  


    def is_global_satisfiable(feature):
        for clause in clauses:
            if feature in clause or -feature in clause:
                clause_satisfied = False
                for literal in clause:
                    var = abs(literal)
                    if literal > 0 and assignment.get(var, -1) == 1:  # Positive literal must be 1
                        clause_satisfied = True
                        break 
                    elif literal < 0 and assignment.get(var, -1) == 0:  # Negative literal must be 0
                        clause_satisfied = True
                        break 
                if not clause_satisfied:  
                    return False
        return True


    for feature in variable_order:
        if feature not in relevant_variables:
            continue  


        assignment[feature] = 1  
        E.append((feature, 1))

        if is_global_satisfiable(feature):
            break  

        assignment[feature] = 0  # Deselect the feature (set to 0)
        E[-1] = (feature, 0)  # Update the decision in the list

        if is_global_satisfiable(feature):
            break  # Stop early if the CNF is satisfied

    return len(E), E  # Return the number of decisions made and the decisions themselves

 
print(selective_configuration(num_clauses=num_clauses, variable_order=variable_order, clauses=clauses))


'''

a clause 

if the len of the literals SCANNED (everyone both in FE and E) is len(clause) - 1 AND the CF[idx] corresponding is still 0
activate the missing variable
'''

def element_scanned_in_a_clause(clause, E, FE):
    counter = 0
    for literal in clause:
        for el in E:
            if abs(el) == abs(literal):
                counter += 1
        for el in FE:
            if abs(el) == abs(literal):
                counter += 1
    return counter


def selective_configuration(num_clauses, variable_order):

    CF = [0] * num_clauses
    E = []
    FE = []
    is_in_FE = True
    occurred = False
    flag = False
    activation_protocol = False 

    for feature in variable_order:
        occurred = False
        is_in_FE = True
        flag = True
        activation_protocol = False 

        for clause_idx in range(len(clauses)):
            for literal_idx in range(len(clauses[clause_idx])):
                if clauses[clause_idx][literal_idx] == feature:
                    if CF[clause_idx] == 0 and flag:

                        '''if (element_scanned_in_a_clause(clauses[clause_idx], E, FE) == (len(clauses[clause_idx]) - 1) and
                            CF[clause_idx] == 0):   
                            activation_protocol = True'''

                        flag = False
                        is_in_FE = False
                        CF[clause_idx] = 1
                        if not occurred:
                            occurred = True

                elif clauses[clause_idx][literal_idx] == -feature:
                    if CF[clause_idx] == 0 and flag:

                        if (element_scanned_in_a_clause(clauses[clause_idx], E, FE) == (len(clauses[clause_idx]) - 1) and
                            CF[clause_idx] == 0):   
                            activation_protocol = True

                        flag = False
                        is_in_FE = False
                        if not occurred:
                            occurred = True

        if is_in_FE:
            FE.append(feature)
        else:
            if activation_protocol:
                E.append(-(feature))
            else:
                E.append(feature)
    return E, FE

def deselective_configuration(num_clauses, variable_order):
    pass

E, FE = selective_configuration(num_clauses=num_clauses, variable_order=variable_order)






















def permissive_configuration(num_clauses, variable_order):

    E = []
    CF = [0] * num_clauses
    FE = []
    is_in_FE = True
    occurred = False
    flag = False

    for feature in variable_order:
        occurred = False
        is_in_FE = True
        first_occurrence = 0  
        flag = True

        for clause_idx in range(len(clauses)):
            for literal_idx in range(len(clauses[clause_idx])):
                if abs(clauses[clause_idx][literal_idx]) == feature:

                    if CF[clause_idx] == 0 and flag:
                        flag = False
                        is_in_FE = False
                        CF[clause_idx] = 1
                        if not occurred:
                            first_occurrence = clauses[clause_idx][literal_idx]
                            occurred = True
        if is_in_FE:
            FE.append(feature)
        else:
            if first_occurrence > 0:
                E.append(feature)
            else:
                E.append(-feature)
    return E, FE

E, FE = permissive_configuration(num_clauses=num_clauses, variable_order=variable_order)

if E[0] > 0 and E[1] > 0:
    limited_variables = variables[abs(E[0])-1].__and__(variables[abs(E[1])-1])
elif E[0] > 0 and E[1] < 0:
    limited_variables = variables[abs(E[0])-1].__and__((variables[abs(E[1])-1]).__invert__())
elif E[0] < 0 and E[1] > 0:
    limited_variables = (variables[abs(E[0])-1].__invert__()).__and__(variables[abs(E[1])-1])
else:
    limited_variables = (variables[abs(E[0])-1].__invert__()).__and__((variables[abs(E[1])-1]).__invert__())

for i in range(2, len(E)):
    if E[i] > 0:
        limited_variables = limited_variables.__and__(variables[abs(E[i])-1])
    else:
        limited_variables = limited_variables.__and__((variables[abs(E[i])-1]).__invert__())

restricted_bdd = cnf_bdd.__and__(limited_variables)


print('OSTIA')


'''
RESULTS

(A) the total number of valid configurations

buildroot: 1.979294126137951e+158

busybox: inf

embtoolkit: memory out of bound

toybox: 1.4499179090096947e+17

uClinux: inf

'''