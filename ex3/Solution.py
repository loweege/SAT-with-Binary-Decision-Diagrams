import os
import re
from oxidd.bdd import BDDManager

'''
TO DO LIST:

1) implement the othe part of the formula
2) check if it works with a small sample.
3) complete the exercise
'''

def decimal_to_binary(num):
    # Convert the decimal number to binary using bin() and remove the '0b' prefix
    binary = bin(num)[2:]
    # Pad the binary string with leading zeros to ensure it's at least 5 characters long
    return binary.zfill(5)

file_path = "finite-state-automata/bakery.1.c.ba"
with open(file_path, 'r') as f:
    # Read the content of the file
    file_content = f.read()

    # Split the content by lines
    lines = file_content.strip().splitlines()

    # Initialize lists to store the portions of the lines
    raw_source_states = []
    raw_destination_states = []

    # Iterate over each line
    for line in lines:
        if '->' in line:  # Check if the line contains '->'
            # Find the position of the first comma and '->'
            start = line.find(',') + 1
            end = line.find('->')
            # Extract the portion between the first comma and '->' for source states
            raw_source_states.append(line[start:end].strip())
            # Extract the portion after '->' for destination states
            raw_destination_states.append(line[end + 2:].strip())  # +2 to skip the '->' symbol

    # Convert raw_source_states into source_states using decimal_to_binary
    source_states = []
    destination_states = []

    # Helper function to convert numbers in a portion to binary
    def convert_to_binary(numbers):
        binary_numbers = []
        for number in numbers:
            converted_number = ""
            for char in number:
                if char.isdigit():  # Check if the character is a digit
                    binary_char = decimal_to_binary(int(char))  # Convert digit to binary
                    converted_number += binary_char
                else:
                    converted_number += char  # Keep non-digit characters unchanged
            binary_numbers.append(converted_number)
        return " ".join(binary_numbers)

    # Process source states
    for portion in raw_source_states:
        numbers = portion.split()  # Split the portion by spaces
        source_states.append(convert_to_binary(numbers))

    # Process destination states
    for portion in raw_destination_states:
        numbers = portion.split()  # Split the portion by spaces
        destination_states.append(convert_to_binary(numbers))

    # Merge source_states and destination_states with '->' symbol
    final_states_raw = []
    for src, dest in zip(source_states, destination_states):
        final_states_raw.append(f"{src} -> {dest}")

    # Print the final states list
    print(final_states_raw)

def extract_zeros_ones_from_list(input_list):
    def extract_zeros_ones(input_string):
        # Remove non-relevant characters
        cleaned_string = input_string.replace('[', '').replace(']', '').replace('|', '').replace('->', '').replace(' ', '')
        
        # Keep only '0' and '1' characters and join them into a single string
        zeros_ones_string = ''.join([char for char in cleaned_string if char in ('0', '1')])
        
        return zeros_ones_string

    # Process each string in the input list
    result_list = [extract_zeros_ones(s) for s in input_list]
    
    return result_list

final_states = extract_zeros_ones_from_list(final_states_raw)

def create_formula_from_strings(strings):
    def create_formula_from_string(s):
        variables = []
        for i, bit in enumerate(s):
            # Each variable is xi where i is the position + 1
            var = i + 1
            if bit == '0':
                # Append negated variable (represented as -xi)
                variables.append(-var)  # -var means not xi
            elif bit == '1':
                # Append positive variable (xi)
                variables.append(var)
        
        # Create 'and' clause for all variables before 'implies'
        and_clause = ('and', *variables)  # Unpack the list of variables into 'and'
        
        # Create final formula with implies
        formula = ('implies', and_clause, True)  # Example implies with another condition
        return formula

    final_formula = [create_formula_from_string(s) for s in strings]
    return final_formula

final_formulas = create_formula_from_strings(final_states)

def flatten_formulas(formula_list):
    # Create a new formula that is an AND operation of all formulas in the list
    if not formula_list:
        return True  # Return True if the list is empty (no formulas to combine)

    combined_formula = ('or', *formula_list)
    
    # Return the final combined formula
    return combined_formula

final_formula = flatten_formulas(final_formulas)

def contains_number(s):
    # Define the regex pattern for a valid integer (positive or negative)
    pattern = r'^-?\d+$'
    return bool(re.match(pattern, s))

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
        return ~make_bdd(level_function, formula[1], manager, variables)
    elif formula[0] == 'implies':  # Implication (ψ → ψ')
        left_bdd = make_bdd(level_function, formula[1], manager, variables)
        right_bdd = make_bdd(level_function, formula[2], manager, variables)
        return ~left_bdd | right_bdd  # Use the equivalence p → q = ¬p ∨ q
    elif formula[0] == 'and':  # AND operation (ψ ∧ ψ')
        left_bdd = make_bdd(level_function, formula[1], manager, variables)
        right_bdd = make_bdd(level_function, formula[2], manager, variables)
        return left_bdd & right_bdd
    elif formula[0] == 'or':  # OR operation (ψ ∨ ψ')
        left_bdd = make_bdd(level_function, formula[1], manager, variables)
        right_bdd = make_bdd(level_function, formula[2], manager, variables)
        return left_bdd | right_bdd
    else:
        raise ValueError("Unsupported formula format")








# Example usage

level_function = 1
num_variables = 100

manager = BDDManager(100_000_000, 1_000_000, 1)
variables = [manager.new_var() for i in range(1, num_variables + 1)]  # Same variable initialization as in your code

# Constructing the BDD for a propositional formula
# Example formula in Python structure: ('implies', ('or', 1, -2), ('not', 3))
formula = ('implies', ('or', 1, -2), ('not', 3))  # This is just an example structure

prova = ('or', ('implies', ('and', 1,2,3), True), ('implies', ('and', 1,2,3), True))

bdd = make_bdd(level_function, final_formula, manager, variables)


"""


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
    print()"""