from buddy import BuDDy

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

def diagramization(manager, clauses):
    cnf_bdd = 1
    for clause in clauses:
        clause_bdd = 0
        for literal in clause:
            if literal > 0:
                var_bdd = manager.var2bdd(literal)
            elif literal < 0:
                var_bdd = manager.neg(manager.var2bdd(abs(literal)))
            clause_bdd = manager.apply_or(clause_bdd, var_bdd)
        cnf_bdd = manager.apply_and(cnf_bdd, clause_bdd)

    return cnf_bdd 

def selecting_literal_when_choice(manager, clauses):
    bdd = diagramization(manager, clauses)  
    permissive_features = []
    while bdd != manager.true:
        current_node = bdd 
        branch_0 = manager.low(current_node)
        branch_1 = manager.high(current_node)

        if (manager.satcount_ln(branch_0) > 0 and manager.satcount_ln(branch_1) > 0) or branch_0 == manager.false:
            current_node = branch_1
            permissive_features.append(manager.var(bdd))  
        else:
            current_node = branch_0
            permissive_features.append(-manager.var(bdd))  
        bdd = current_node

    return len(permissive_features)
     

def deselecting_literal_when_choice(manager, clauses):
    bdd = diagramization(manager, clauses)
    permissive_features = []

    while bdd != manager.true:
        current_node = bdd
        branch_0 = manager.low(current_node)
        branch_1 = manager.high(current_node)

        if (manager.satcount_ln(branch_0) > 0 and manager.satcount_ln(branch_1) > 0) or branch_1 == manager.false:
            current_node = branch_0
            permissive_features.append(-manager.var(bdd))
        else:
            current_node = branch_1
            permissive_features.append(manager.var(bdd))
        bdd = current_node

    return len(permissive_features)

def selecting_features_if_more_configurations(manager, clauses):
    bdd = diagramization(manager, clauses)  
    permissive_features = []

    while bdd != manager.true:
        current_node = bdd
        branch_0 = manager.low(current_node)
        branch_1 = manager.high(current_node)

        if branch_1 != manager.false:
            count_true = manager.satcount_ln(branch_1)
        else:
            count_true = 0

        if branch_0 != manager.false:
            count_false = manager.satcount_ln(branch_0)
        else:
            count_false = 0

        if count_true >= count_false:
            permissive_features.append(manager.var(current_node))  
            current_node = branch_1
        else:
            permissive_features.append(-manager.var(current_node))  
            current_node = branch_0
        bdd = current_node

    return len(permissive_features)


def deselecting_features_if_more_configurations(manager, clauses):
    bdd = diagramization(manager, clauses)  
    permissive_features = []
   
    while bdd != manager.true:
        current_node = bdd
        branch_0 = manager.low(current_node)
        branch_1 = manager.high(current_node)

        if branch_1 != manager.false:
            count_true = manager.satcount_ln(branch_1)
        else:
            count_true = 0

        if branch_0 != manager.false:
            count_false = manager.satcount_ln(branch_0)
        else:
            count_false = 0

        if count_false >= count_true:
            permissive_features.append(-manager.var(current_node))  
            current_node = branch_0
        else:
            permissive_features.append(manager.var(current_node))  
            current_node = branch_1
        bdd = current_node

    return len(permissive_features)


def most_permissive_configuration(manager, clauses, variable_order):
    bdd = diagramization(manager, clauses)
    permissive_features = []

    while bdd != manager.true:
        current_node = bdd
        branch_0 = manager.low(current_node)
        branch_1 = manager.high(current_node)
        count_false = manager.satcount_ln(branch_0)
        count_true = manager.satcount_ln(branch_1)
        var = manager.var(current_node)
        
        if count_true > count_false:
            permissive_features.append(var)  
            bdd = branch_1
        elif count_true < count_false:
            permissive_features.append(-var)  
            bdd = branch_0
        else:
            index_var = variable_order.index(var)
            index_branch_0 = variable_order.index(manager.var(branch_0))
            index_branch_1 = variable_order.index(manager.var(branch_1))
            sum_indexes_0 = index_var + index_branch_0
            sum_indexes_1 = index_var + index_branch_1

            if sum_indexes_1 < sum_indexes_0:
                permissive_features.append(var)  
                bdd = branch_1
            else:
                permissive_features.append(-var)  
                bdd = branch_0

    return len(permissive_features), permissive_features

file_path = './model-checking/conf-dimacs/buildroot.dimacs'
num_variables, num_clauses, variable_order, clauses = parse_dimacs(file_path)

manager = BuDDy(variable_order, "buddy.windows")
cnf = diagramization(manager, clauses)
flag = True
if flag:
    valid_configurations = manager.satcount_ln(cnf)
    print("Selecting whenever there is a choice: ", selecting_literal_when_choice(manager, clauses))
    print("Deselecting whenever there is a choice: ", deselecting_literal_when_choice(manager, clauses))
    print("Selecting a feature iff this decision would cover more valid configurations than with deselecting the feature: ", selecting_features_if_more_configurations(manager, clauses))
    print("Deselecting a feature iff this decision would cover more valid configurations than with selecting the feature: ", deselecting_features_if_more_configurations(manager, clauses))
    print(f"Number of valid configurations: {valid_configurations}")

    print("Most permissive configuration: ", most_permissive_configuration(manager, clauses, variable_order))

manager.__exit__()

