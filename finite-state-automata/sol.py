from oxidd.bdd import BDDManager
from util import *

manager = BDDManager(100_000_000, 1_000_000, 8)
file_path = 'finite-state-automata/finite-state-automata/phils.2.c.ba'

approx = 4 

#initialize the variables needed [from 0 to num_variables-1]
#num_variables = variable_number_calculation(file_path, approx)
num_variables = 104

x = [manager.new_var() for i in range(num_variables)]
y = [manager.new_var() for i in range(int(num_variables/2))]

source_state, transitions, accepting_states = parsing(file_path, approx)

def transitions_optimisation(transitions):
    reordered = []
    
    for transition in transitions:
        numbers = len(transition)
        
        mid = numbers // 2
        first_half = transition[:mid]
        second_half = transition[mid:]
        
        reordered_transition = []
        for i in range(mid):
            reordered_transition.append(first_half[i])
            reordered_transition.append(second_half[i])
        reordered.append(''.join(reordered_transition))

    return reordered



#transitions = transitions_optimisation(transitions)




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


'''------------------------ACCEPTING STATES DIAGRAMMIZATION PROCESSING------------------------'''
def compute_gamma(list, x):
    def compute_phi(row):
        # Compute the first condition for the row
        if row[0] == '1' and row[1] == '1':
            phi = x[0].__and__(x[1])
        elif row[0] == '0' and row[1] == '1':
            phi = (x[0].__invert__()).__and__(x[1])
        elif row[0] == '1' and row[1] == '0':
            phi = x[0].__and__(x[1].__invert__())
        elif row[0] == '0' and row[1] == '0':
            phi = (x[0].__invert__()).__and__(x[1].__invert__())
        
        # Loop through the rest of the elements in the row
        for i in range(2, len(row)):
            if row[i] == '0':
                phi = phi.__and__(x[i].__invert__())
            else:
                phi = phi.__and__(x[i])
        return phi

    # Compute the first two phi values
    phi = compute_phi(list[0])
    phi2 = compute_phi(list[1])

    # Compute initial gamma as the OR of the first two phi values
    gamma = phi.__or__(phi2)

    # Compute the remaining phi values and OR them with gamma
    for j in range(2, len(list)):
        alpha = compute_phi(list[j])
        gamma = gamma.__or__(alpha)
    
    return gamma
'''------------------------ACCEPTING STATES DIAGRAMMIZATION CONCLUDED-------------------------'''

gamma1 = compute_gamma(accepting_states, y)
'''
(A) the variable ordering of the shared BDD

(B) the total number of nodes of the shared BDD

(C) the number satisfying assignments and BDD nodes for representing the characteristic function of
    (i) the initial state,
    (ii) the transition relation, and
    (iii) the accepting states.

'''

'''
THINGS TO WRITE IN THE REPORT

1) Encoding (with ERR and how has been exploited only four bits)
2) The difference between the order of the feature. Heuristic and not Heuristic

'''



'bakery.1.c.ba NON HEURISTIC'
#nodes -> 48715
#paths -> 2697.0
'bakery.1.c.ba HEURISTIC'
#nodes -> 11641
#paths -> 2697.0
'ACCEPTING STATES'
#nodes -> 1210
#paths -> 196.0


'bakery.2.c.ba NON HEURISTIC'
#nodes -> 35802
#paths -> 2085.0
'bakery.2.c.ba HEURISTIC'
#nodes -> 8094
#paths -> 2085.0
'ACCEPTING STATES'
#nodes -> 937
#paths -> 204.0


'fischer.2.c.ba NON HEURISTIC'
#nodes -> 313858
#paths -> 65458.0
'fischer.2.c.ba HEURISTIC'
#nodes -> 29393
#paths -> 67590.0
'ACCEPTING STATES'
#nodes -> 2542
#paths -> 6866


'fischer.3.1.c.ba NON HEURISTIC'
#nodes -> 13708
#paths -> 1401.0
'fischer.3.1.c.ba HEURISTIC'
#nodes -> 6760
#paths -> 1401.0
'ACCEPTING STATES'
#nodes -> 252
#paths -> 29.0


'fischer.3.2.c.ba NON HEURISTIC'
#nodes -> 25826
#paths -> 3856.0
'fischer.3.2.c.ba HEURISTIC'
#nodes -> 8632
#paths -> 3856.0
'ACCEPTING STATES'
#nodes -> 870
#paths -> 431.0


'fischer.3.c.ba NON HEURISTIC'
#nodes -> 13737
#paths -> 1400.0
'fischer.3.c.ba HEURISTIC'
#nodes -> 6760
#paths -> 1400.0
'ACCEPTING STATES'
#nodes -> 252
#paths -> 29.0


'mcs.1.2.c.ba NON HEURISTIC'
#nodes -> 314625
#paths -> 21509.0
'mcs.1.2.c.ba HEURISTIC'
#nodes -> 21551
#paths -> 21509.0
'ACCEPTING STATES'
#nodes -> 2261
#paths -> 1843.0


'NFA_hard_1.ba NON HEURISTIC'
#nodes -> 237553
#paths -> 25452.0
'NFA_hard_1.ba HEURISTIC'
#nodes -> 17539
#paths -> 25452.0
'ACCEPTING STATES'
#nodes -> 1076
#paths -> 2850.0


'phils.1.1.c.ba NON HEURISTIC'
#nodes -> 5174
#paths -> 464.0
'phils.1.1.c.ba HEURISTIC'
#nodes -> 2228
#paths -> 464.0
'ACCEPTING STATES'
#nodes -> 230
#paths -> 81.0


'phils.2.c.ba NON HEURISTIC'
#nodes -> 33275
#paths -> 2350.0
'phils.2.c.ba HEURISTIC'
#nodes -> 11350
#paths -> 2350.0
'ACCEPTING STATES'
#nodes -> 1073
#paths -> 295.0