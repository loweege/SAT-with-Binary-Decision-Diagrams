import os
from oxidd.bdd import BDDManager



def make_bdd(level_function, formula, manager, variables):
    # Recursive function to construct π-BDD from formula
    if formula == False:
        return manager.false()
    elif formula == True:
        return manager.true()
    elif isinstance(formula, int):  # If formula is a literal (e.g., xi)
        var_index = abs(formula) - 1
        if formula > 0:
            return variables[var_index]  # Positive literal (xi)
        else:
            return ~variables[var_index]  # Negative literal (¬xi)
    elif formula[0] == 'not':  # If formula is a negation (¬ψ)
        return make_bdd(level_function, formula[1], manager, variables)
    elif formula[0] in ['and', 'or']:  # Binary operation (ψ ◦ ψ')
        left_bdd = make_bdd(level_function, formula[1], manager, variables)
        right_bdd = make_bdd(level_function, formula[2], manager, variables)
        if formula[0] == 'and':
            return left_bdd & right_bdd
        else:
            return left_bdd | right_bdd
    else:
        raise ValueError("Unsupported formula format")



def cnf_to_bdd_with_proper_initialization(clauses, num_variables):
    manager = BDDManager(100_000_000, 1_000_000, 1)

    # Create a variable for each feature
    variables = [manager.new_var() for i in range(1, num_variables + 1)]

    bdd_formula = manager.true()

    # Track variables that have been set to true or false
    initialized_variables = set()

    for clause in clauses:
        clause_bdd = manager.false()  # Start with false since it's an OR clause

        # Check the first literal of the clause
        first_literal = clause[0]
        var_index = abs(first_literal) - 1  # Variable index is 1-based in DIMACS

        # If the variable hasn't been initialized, set it to True
        if var_index not in initialized_variables:
            if first_literal > 0:
                bdd_formula &= variables[var_index]  # Set positive literal to True
            else:
                bdd_formula &= ~variables[var_index]  # Set negative literal to True
            initialized_variables.add(var_index)

        # Process the rest of the clause
        for literal in clause:
            var_index = abs(literal) - 1  # Variable index is 1-based in DIMACS
            if literal > 0:
                clause_bdd |= variables[var_index]
            else:
                clause_bdd |= ~variables[var_index]

        # AND this clause with the current BDD formula
        bdd_formula &= clause_bdd

    return bdd_formula

def cnf_to_bdd_with_initialization(clauses, num_variables):
    manager = BDDManager(100_000_000, 1_000_000, 1)

    # Create a variable for each feature
    variables = [manager.new_var() for i in range(1, num_variables + 1)]

    bdd_formula = manager.true()

    # Set to track variables that have been set to True or False
    initialized_variables = set()

    for clause in clauses:
        clause_bdd = manager.false()  # Start with false, since it's an OR clause

        # Check the first literal
        first_literal = clause[0]
        var_index = abs(first_literal) - 1  # Variable index is 1-based in DIMACS

        # If the variable hasn't been initialized, set it to True
        if var_index not in initialized_variables:
            bdd_formula &= variables[var_index]  # Set to True
            initialized_variables.add(var_index)

        # Process the clause
        for literal in clause:
            var_index = abs(literal) - 1  # Variable index is 1-based in DIMACS
            if literal > 0:
                # Positive literal (xi)
                clause_bdd |= variables[var_index]
            else:
                # Negative literal (¬xi)
                clause_bdd |= ~variables[var_index]

        # AND this clause with the current BDD formula
        bdd_formula &= clause_bdd

    return bdd_formula


def parse_dimacs(file_path):
    num_variables = None
    num_clauses = None
    variable_order = []
    clauses = []

    with open(file_path, 'r') as f:
        for line in f:
            tokens = line.strip().split()

            # Skip empty or comment lines
            if not tokens or tokens[0] == 'c':
                # Check for variable order comment lines (c vo ...)
                if tokens[1] == 'vo':
                    variable_order = list(map(int, tokens[2:]))
                continue

            # Header line (p cnf num_variables num_clauses)
            if tokens[0] == 'p' and tokens[1] == 'cnf':
                num_variables = int(tokens[2])
                num_clauses = int(tokens[3])
            else:
                # Clause lines (e.g., 2 -3 5 0)
                clause = list(map(int, tokens[:-1]))  # Drop the ending 0
                clauses.append(clause)

    return num_variables, num_clauses, variable_order, clauses

    
def cnf_to_bdd(clauses, num_variables):
    manager = BDDManager(100_000_000, 1_000_000, 1)


    # Create a variable for each feature
    variables = [manager.new_var() for i in range(1, num_variables + 1)]


    bdd_formula = manager.true()

    for clause in clauses:
        clause_bdd = manager.false()  # Start with false, since it's an OR clause
        for literal in clause:
            var_index = abs(literal) - 1  # Variable index is 1-based in DIMACS
            if literal > 0:
                # Positive literal (xi)
                clause_bdd |= variables[var_index]
            else:
                # Negative literal (¬xi)
                clause_bdd |= ~variables[var_index]

        # AND this clause with the current BDD formula
        bdd_formula &= clause_bdd
    
    return bdd_formula


def count_valid_configurations(bdd, num_variables):
    # Return the number of satisfying assignments
    return bdd.sat_count_float(num_variables)







if __name__ == '__main__':

    paths = {
    "example": "Exercise1/example.dimacs",
    "buildroot": "Exercise1/conf-dimacs/buildroot.dimacs",
    "busybox": "Exercise1/conf-dimacs/busybox.dimacs",
    "embtoolkit": "Exercise1/conf-dimacs/embtoolkit.dimacs",
    "toybox": "Exercise1/conf-dimacs/toybox.dimacs",
    "uClinux": "Exercise1/conf-dimacs/uClinux.dimacs"
    }

    path = paths["example"]
    num_variables, num_clauses, variable_order, clauses = parse_dimacs(path)

    #print(num_variables, num_clauses, variable_order, clauses)
    bdd_formula = cnf_to_bdd(clauses, num_variables)

    #same as reshma
    bdd_new = cnf_to_bdd_with_initialization(clauses, num_variables)

    '''
    What does it mean select a feature whenever there is a choice?
    if it means that we scan all the feature in the right order, we select 
    and after it there still is at least one satisfiable path, we implemented it.

    check x1, then x2, then x3, and so on
    '''

    '''
    for all the variables, scan all the clauses and put into a list the variables not contained 
    in none of tha clauses. Each of this variable can be set to true.

    After that, scan the clauses and set the first element to true if it is not been selected yet.
    Otherwise pick the second, otherwise pick the third and so on. 
    '''

    num_valid_configs = count_valid_configurations(bdd_formula, num_variables)
    i = 1

    supp = []
    while i <= num_variables:
        clauses.append([i])
        supp.append([i])

        bdd_formula = cnf_to_bdd(clauses, num_variables)
        #bdd_formula = bdd_formula.cofactor_true()
        num_valid_configs = count_valid_configurations(bdd_formula, num_variables)
        if num_valid_configs == 0.0:
            supp.remove([i])
            clauses.remove([i])
        i+=1

    print(i)
    print(len(supp))




    print("----------------------valid_configurations_number_below-----------------------")
    print(int(num_valid_configs))
    print()