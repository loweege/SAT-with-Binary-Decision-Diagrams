from oxidd.bdd import BDDManager
from util import *

manager = BDDManager(100_000_000, 1_000_000, 1)
file_path = "ex3/finite-state-automata/phils.2.c.ba"

approx = 4 

#initialize the variables needed [from 0 to num_variables-1]
num_variables = variable_number_calculation(file_path, approx)
x = [manager.new_var() for i in range(num_variables)]

source_state, transitions, accepting_states = parsing(file_path, approx)


'''------------------------TRANSITIONS DIAGRAMMIZATION PROCESSING------------------------'''
if transitions[0][0] == '1' and transitions[0][0] == '1':
    phi = x[0].__and__(x[1])        
elif transitions[0][0] == '0' and transitions[0][0] == '1':
    phi = (x[0].__invert__()).__and__(x[1])        
elif transitions[0][0] == '1' and transitions[0][0] == '0':
    phi = x[0].__and__(x[1].__invert__())        
elif transitions[0][0] == '0' and transitions[0][0] == '0':
    phi = (x[0].__invert__()).__and__(x[1].__invert__())        

for i in range(2, len(transitions[0])):
    if transitions[0][i] == '0':
        phi = phi.__and__(x[i].__invert__()) 
    else:
        phi = phi.__and__(x[i])


if transitions[1][0] == '1' and transitions[1][0] == '1':
    phi2 = x[0].__and__(x[1])        
elif transitions[1][0] == '0' and transitions[1][0] == '1':
    phi2 = (x[0].__invert__()).__and__(x[1])        
elif transitions[1][0] == '1' and transitions[1][0] == '0':
    phi2 = x[0].__and__(x[1].__invert__())        
elif transitions[1][0] == '0' and transitions[1][0] == '0':
    phi2 = (x[0].__invert__()).__and__(x[1].__invert__())        

for i in range(2, len(transitions[0])):
    if transitions[1][i] == '0':
        phi2 = phi2.__and__(x[i].__invert__()) 
    else:
        phi2 = phi2.__and__(x[i])

gamma = phi.__or__(phi2)
n = len(transitions)

for j in range(2, len(transitions)):

    if transitions[j][0] == '1' and transitions[j][0] == '1':
        alpha = x[0].__and__(x[1])        
    elif transitions[j][0] == '0' and transitions[j][0] == '1':
        alpha = (x[0].__invert__()).__and__(x[1])        
    elif transitions[j][0] == '1' and transitions[j][0] == '0':
        alpha = x[0].__and__(x[1].__invert__())        
    elif transitions[j][0] == '0' and transitions[j][0] == '0':
        alpha = (x[0].__invert__()).__and__(x[1].__invert__())        

    for i in range(2, len(transitions[0])):
        if transitions[j][i] == '0':
            alpha = alpha.__and__(x[i].__invert__()) 
        else:
            alpha = alpha.__and__(x[i])
    
    gamma = gamma.__or__(alpha)
    del alpha
'''------------------------TRANSITIONS DIAGRAMMIZATION CONCLUDED------------------------'''


'''TESTS DIFFERENT ORDERS'''
'''FIX PATHS FOR 255 ENCODING'''
'''ADD NFA_HARD TO STANDARD ENCODING'''

'''Just the BDDs of the transitions below'''

'bakery.1.c.ba'
#nodes -> 48715
#paths -> 2697.0

'bakery.2.c.ba'
#nodes -> 35802
#paths -> 2085.0

'phils.1.1.c.ba'
#nodes -> 5174
#paths -> 464.0

'phils.2.c.ba'
#nodes -> 33275
#paths -> 2350.0




'fischer.2.c.ba'
#nodes -> 313858
#paths -> 1.2074869735768798e+24