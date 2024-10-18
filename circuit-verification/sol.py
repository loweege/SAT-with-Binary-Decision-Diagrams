from oxidd.bdd import BDDManager
from mapping import mapping 
import re

'''

check the order ot the inputs 

implement the multithreading stuff


'''

def read_file(file_path):
    inputs = []
    outputs = []
    S = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            if line.startswith('INPUT('):
                # Extract the element inside the parentheses
                element = line[len('INPUT('):-1]
                inputs.append(element)
            elif line.startswith('OUTPUT('):
                # Extract the element inside the parentheses
                element = line[len('OUTPUT('):-1]
                outputs.append(element)
            else:
                # Logic expressions are added to the S list
                S.append(line)

    return inputs, outputs, S

# Example usage:
file_path = 'circuit-verification/circuit-bench/circuit01.bench'  
inputs, outputs, raw_S = read_file(file_path)

S, inputs, outputs = mapping(raw_S, inputs, outputs)
print('lessgo')
print(S)

#circuit1 ok
#circuit5 ok
#circuit20 not ok (too much time)


'''def compare_last_two_elements(list1, list2):
    str1 = list1[-1]
    str2 = list2[-1]
    
    num1 = int(str1[1:])
    num2 = int(str2[1:])
    
    return max(num1, num2)'''

def find_max_x_number(expressions):
    max_num = 0
    pattern = r'x(\d+)'

    for expr in expressions:
        numbers = re.findall(pattern, expr)
        max_num = max(max_num, *map(int, numbers))
    
    return max_num

manager = BDDManager(100_000_000, 1_000_000, 1)
num_variables = find_max_x_number(S)
x = [manager.new_var() for i in range(num_variables)]




'''read the operator right after the equal
if it is NAND 
read the opereator at the left of the equal

you should do a nand operation between all the operatpr 
for example if it is NAND(x29, x23, x4)
    than it should be executed supp = x29.__nand__(x3)
    for element in NAND(x29, x23, x4) except the first one you do 
        supp = supp.__nand__(element)
    the operator we have read before that was on the left of the equal is now = supp
    del supp'''


'''
Notes 

compute the first element of the middle nodes --> 

take the first argument and create a variable with the manager
same thing for the second and so on for all the ariety pf the operator.


than you (depending on the operator, lets say is nand) do  name_of_the_gate = x1.__nand__(x2)

then you apply a logical and among all the name_of_the_gates

Than you have the BDD for the first circuit


same thing for the second circuit

Then you have to finish the formula


['x2', 'x1', 'x13', 'x14', 'x7', 'x1', 'x13', 'x18', 'x19']
['x1', 'x2', 'x3', 'x4']
['x2', 'x6', 'x7', 'x8', 'x9', 'x10']

'''