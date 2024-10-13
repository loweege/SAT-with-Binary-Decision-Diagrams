import os
import re
from oxidd.bdd import BDDManager
import z3

'''
TO DO LIST:
0.1) implement apply
0.2) implement formula_to_bdd properly
1) implement the othe part of the formula
2) check if it works with a small sample.
3) complete the exercise
'''



def decimal_to_binary(num):
    # Convert the decimal number to binary using bin() and remove the '0b' prefix
    binary = bin(num)[2:]
    # Pad the binary string with leading zeros to ensure it's at least 5 characters long
    return binary.zfill(5)

file_path = "ex3/finite-state-automata/bakery.1.c.ba"
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
    #print(final_states_raw)

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


'''def make_bdd(level_function, formula, manager, variables):
    # Recursive function to construct π-BDD from formula
    if formula is False:
        return manager.false()
    elif formula is True:
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
        # Instead of using `~left_bdd | right_bdd`, combine using |=
        return ~left_bdd | right_bdd
    


    elif formula[0] == 'and':  # AND operation (ψ ∧ ψ')
        result_bdd = manager.true()

        left_bdd = make_bdd(level_function, formula[1], manager, variables)
        right_bdd = make_bdd(level_function, formula[2], manager, variables)
        result_bdd &= left_bdd
        result_bdd &= right_bdd
        return result_bdd
    elif formula[0] == 'or':  # OR operation (ψ ∨ ψ')
        result_bdd = manager.false()  # Start with false, since it's an OR clause
        
        left_bdd = make_bdd(level_function, formula[1], manager, variables)
        right_bdd = make_bdd(level_function, formula[2], manager, variables)
        result_bdd |= left_bdd
        result_bdd |= right_bdd  # Use |= to combine
        return result_bdd
    else:
        raise ValueError("Unsupported formula format")
'''


import z3

# Define variables
x = z3.Int('x')
y = z3.Int('y')

# Create constraints
c1 = z3.And(x >= 1, x <= 10)
c2 = z3.And(y >= 1, y <= 10)
c3 = z3.Distinct(x, y)

# Create a goal and add constraints
g = z3.Goal()
g.add(c1, c2, c3)

# List available tactics (optional)
#print(z3.Tactic.list())

# Apply tseitin-cnf tactic and print result
t = z3.Tactic('tseitin-cnf')
print(t(g))



from oxidd.bdd import BDDManager

def make_bdd(level_func, phi, manager, variables):
    print(f"Processing formula: {phi}")  # Debug statement

    # Base cases
    if phi == False:
        return manager.false()
    if phi == True:
        return manager.true()

    # If φ is a variable, return it with its respective 0/1 branches
    if isinstance(phi, int):
        var_index = abs(phi) - 1  # Variables are indexed starting from 1
        if phi > 0:
            return variables[var_index]  # Positive literal (xi)
        else:
            return ~variables[var_index]  # Negative literal (¬xi)

    # Handle negation
    if isinstance(phi, tuple) and phi[0] == 'not':
        return ~make_bdd(level_func, phi[1], manager, variables)

    # Handle binary/n-ary operators
    if isinstance(phi, tuple):
        op = phi[0]
        operands = phi[1:]

        if len(operands) > 2:
            combined_bdd = make_bdd(level_func, (op, operands[0], operands[1]), manager, variables)
            for i in range(2, len(operands)):
                combined_bdd = apply(op, combined_bdd, make_bdd(level_func, operands[i], manager, variables))
            return combined_bdd
        elif len(operands) == 2:
            left = make_bdd(level_func, operands[0], manager, variables)
            right = make_bdd(level_func, operands[1], manager, variables)
            return apply(op, left, right)

    raise ValueError(f"Unsupported formula structure: {phi}")

# Apply function remains the same
def apply(op, left_bdd, right_bdd):
    print(f"Applying operator: {op} to BDDs")  # Debug statement
    if op == 'and':
        return left_bdd & right_bdd
    elif op == 'or':
        return left_bdd | right_bdd
    elif op == 'implies':
        return ~left_bdd | right_bdd
    else:
        raise ValueError(f"Unknown operator: {op}")








#ussume that if a bdd is less then another it means that same bdd is higher
def apply(op, bdd1, bdd2):
    op = 'and'
    #.node_count() considers also the root nodes and the terminal nodes
    if bdd1.node_count() == 0 and bdd2.node_count() == 0:
        #return bdd1 op bdd2 but for now let's say:
        return bdd1 & bdd2
    if bdd1.__lt__(bdd2):
        eps0 = apply(op, bdd1.cofactor_false(), bdd2)
        eps1 = apply(op, bdd1.cofactor_true(), bdd2)
        return eps0 & eps1
    if bdd1.__gt__(bdd2):
        eps0 = apply(op, bdd1, bdd2.cofactor_false())
        eps1 = apply(op, bdd1, bdd2.cofactor_true())
        return eps0 & eps1
    if ((not bdd1.__lt__(bdd2)) and (not bdd1.__gt__(bdd2))):
        eps0 = apply(op, bdd1.cofactor_false(), bdd2.cofactor_false())
        eps1 = apply(op, bdd1.cofactor_true(), bdd2.cofactor_true())
        return eps0 & eps1





# Example usage
level_function = None  # No specific level function is needed here
num_variables = 100

manager = BDDManager(100_000_000, 1_000_000, 1)
variables = [manager.new_var() for i in range(1, num_variables + 1)]  # Same variable initialization as in your code

# Constructing the BDD for a propositional formula
# Example formula in Python structure: ('implies', ('or', 1, -2), ('not', 3))
formula = ('implies', ('or', 1, -2), -3)  # This is just an example structure
ts_formuka = ('and',('and', 1, ('or', -1, -2, 3)), ('and', ('or', 1, -3), ('or', 1, 2)), ('and', ('or', -2, 4, -5), ('or', 2, -4)), ('and', ('or', 2, 5), ('or', 3, 6), ('or', -3, -6)))

tested_formula = ('and',('or', 2,3,5), ('or', -3,-5)) #THIS WORKS against all possibilities

tested_formula_shape2 = ('and',('or', ('or', 2, 3), 5), ('or', -3,-5)) #THIS WORKS against all possibilities


f = ('or', ('implies', ('and', -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20), ('implies', ('and', -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20), True)), ('implies', ('and', -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20), ('implies', ('and', -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20), True)))

diocane = ('and', ('or', 1,2,-3), ('or', -1, 3))
diocane_binary = ('and', ('or', 1, ('or', 2, -3)), ('or', -1, 3))


# Create the BDD from the formula
bdd = make_bdd(level_function, diocane_binary, manager, variables)

'''
result using the first implementation on final formula --> 1.2676506002282294e+30
'''









manager2 = BDDManager(100_000_000, 1_000_000, 1)
x1 = manager2.new_var()
x1.node_count()
x2 = manager2.new_var()
x2.node_count()
x3 = manager2.new_var()
x3.node_count()
x4 = manager2.new_var()
x4.node_count()
x5 = manager2.new_var()
x5.node_count()


'''... add 100 features'''

tested_formula_shape2 = ('and',('or', ('or', 2, 3), 5), ('or', -3,-5)) #THIS WORKS against all possibilities

# 
orcond = x2.__or__(x3)
orcond2 = orcond.__or__(x5)
#check the one below 
orcond3 = -x3.__or__(-x5)

trye = orcond2.__and__(orcond3)  



r = x1.__and__(x2)


'''


# Cache to store computed results of (op, A, B) to avoid recomputation
cache = {}

# Modified apply function with variable ordering checks
def apply(op, left_bdd, right_bdd, manager):
    # Terminal cases: return terminal if encountered
    if left_bdd.is_terminal() and right_bdd.is_terminal():
        if op == 'and':
            return manager.true() if left_bdd.is_true() and right_bdd.is_true() else manager.false()
        elif op == 'or':
            return manager.false() if left_bdd.is_false() and right_bdd.is_false() else manager.true()
        elif op == 'implies':
            return manager.true() if not left_bdd.is_true() or right_bdd.is_true() else manager.false()
        else:
            raise ValueError(f"Unknown operator: {op}")

    # Check if result is cached
    if (op, left_bdd, right_bdd) in cache:
        return cache[(op, left_bdd, right_bdd)]

    # Determine variable ordering cases
    left_var = left_bdd.var() if not left_bdd.is_terminal() else float('inf')
    right_var = right_bdd.var() if not right_bdd.is_terminal() else float('inf')

    if left_var == right_var:
        # A.var == B.var, apply recursively on both branches
        lo_bdd = apply(op, left_bdd.lo(), right_bdd.lo(), manager)
        hi_bdd = apply(op, left_bdd.hi(), right_bdd.hi(), manager)
        result = manager.ite(left_bdd.var(), lo_bdd, hi_bdd)  # ITE (if-then-else) for BDDs
    elif left_var < right_var:
        # A.var < B.var, apply recursively with B as the same on both branches
        lo_bdd = apply(op, left_bdd.lo(), right_bdd, manager)
        hi_bdd = apply(op, left_bdd.hi(), right_bdd, manager)
        result = manager.ite(left_bdd.var(), lo_bdd, hi_bdd)
    else:
        # A.var > B.var, apply recursively with A as the same on both branches
        lo_bdd = apply(op, left_bdd, right_bdd.lo(), manager)
        hi_bdd = apply(op, left_bdd, right_bdd.hi(), manager)
        result = manager.ite(right_bdd.var(), lo_bdd, hi_bdd)

    # Cache the result before returning it
    cache[(op, left_bdd, right_bdd)] = result
    return result

# Example usage for 'and', 'or', and 'implies'
def make_bdd(level_func, phi, manager, variables):
    if phi == False:
        return manager.false()
    if phi == True:
        return manager.true()

    if isinstance(phi, int):
        var_index = abs(phi) - 1
        if phi > 0:
            return variables[var_index]
        else:
            return ~variables[var_index]

    if isinstance(phi, tuple):
        op = phi[0]
        operands = phi[1:]

        if len(operands) == 2:
            left = make_bdd(level_func, operands[0], manager, variables)
            right = make_bdd(level_func, operands[1], manager, variables)
            return apply(op, left, right, manager)

    raise ValueError(f"Unsupported formula structure: {phi}")

# Initialize the BDD manager and variables
manager = BDDManager(100_000_000, 1_000_000, 1)
num_variables = 100
variables = [manager.new_var() for i in range(1, num_variables + 1)]

# Sample formula: (A.var == B.var case example)
formula = ('implies', ('or', 1, -2), ('not', 3))
bdd = make_bdd(None, formula, manager, variables)
'''