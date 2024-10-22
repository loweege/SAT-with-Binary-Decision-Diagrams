import re
from oxidd.bdd import BDDManager
from mapping import mapping, reordering
manager = BDDManager(100_000_000, 1_000_000, 8)
aiuto = []

def read_file(file_path):
    inputs = []
    outputs = []
    S = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  
            if line.startswith('INPUT('):
                element = line[len('INPUT('):-1]
                inputs.append(element)
            elif line.startswith('OUTPUT('):
                element = line[len('OUTPUT('):-1]
                outputs.append(element)
            else:
                S.append(line)

    return inputs, outputs, S

file_path1 = 'circuit-verification/circuit-bench/circuit14.bench'
inputs, outputs, raw_S = read_file(file_path1)
file_path2 = 'circuit-verification/circuit-bench/circuit14_opt.bench'  
inputs2, outputs2, raw_S2 = read_file(file_path2)

S, inputsS, outputsS, T, inputsT, outputsT = mapping(raw_S, inputs, outputs, raw_S2, inputs2, outputs2)
S = reordering(S, inputsS)
T = reordering(T, inputsT)

x = [manager.new_var() for i in range(100000)]
phis = [manager.new_var() for i in range(100000)]
psys = [manager.new_var() for i in range(100000)]

phis_used = []
psys_used = []

def ultimate_function(equations1, equations2, outputs1, outputs2):
    pattern = r'x(\d+)'

    for eq in equations1:
        left_side, right_side = eq.split(' = ')
        i_left = re.findall(pattern, left_side)
        is_right = re.findall(pattern, right_side)
        ins = [re.findall(r'\d+', item)[0] for item in inputsS]

        if right_side.startswith("NAND"):
            if ((is_right[-2]) in ins) and ((is_right[-1]) in ins):
                supp = x[int(is_right[-2])].__and__(x[int(is_right[-1])])
            elif ((is_right[-2]) in ins) and ((is_right[-1]) not in ins):
                supp = x[int(is_right[-2])].__and__(phis[int(is_right[-1])])
            elif ((is_right[-2]) not in ins) and ((is_right[-1]) in ins):
                supp = phis[int(is_right[-2])].__and__(x[int(is_right[-1])])
            else:
                supp = phis[int(is_right[-2])].__and__(phis[int(is_right[-1])])

            if len(is_right) > 2:
                for variable in is_right[:-2]:
                    if variable in ins:
                        supp = supp.__and__(x[int(variable)])
                    else:
                        supp = supp.__and__(phis[int(variable)])

            supp = supp.__invert__()
            phis[int(i_left[0])] = supp
            x[int(i_left[0])].equiv(supp)
            phis_used.append(int(i_left[0]))
            del supp

        elif right_side.startswith("AND"):
            if ((is_right[-2]) in ins) and ((is_right[-1]) in ins):
                supp = x[int(is_right[-2])].__and__(x[int(is_right[-1])])
            elif ((is_right[-2]) in ins) and ((is_right[-1]) not in ins):
                supp = x[int(is_right[-2])].__and__(phis[int(is_right[-1])])
            elif ((is_right[-2]) not in ins) and ((is_right[-1]) in ins):
                supp = phis[int(is_right[-2])].__and__(x[int(is_right[-1])])
            else:
                supp = phis[int(is_right[-2])].__and__(phis[int(is_right[-1])])

            if len(is_right) > 2:
                for variable in is_right[:-2]:
                    if variable in ins:
                        supp = supp.__and__(x[int(variable)])
                    else:
                        supp = supp.__and__(phis[int(variable)])

            phis[int(i_left[0])] = supp
            x[int(i_left[0])].equiv(supp)
            phis_used.append(int(i_left[0]))
            del supp

        elif right_side.startswith("NOT"):
            if is_right[0] in ins:
                supp = (x[int(is_right[0])].__invert__())
            else:
                supp = phis[int(is_right[0])].__invert__()
            
            phis[int(i_left[0])] = supp
            x[int(i_left[0])].equiv(supp)
            phis_used.append(int(i_left[0]))
            del supp

        elif right_side.startswith("OR"):
            if ((is_right[-2]) in ins) and ((is_right[-1]) in ins):
                supp = x[int(is_right[-2])].__or__(x[int(is_right[-1])])
            elif ((is_right[-2]) in ins) and ((is_right[-1]) not in ins):
                supp = x[int(is_right[-2])].__or__(phis[int(is_right[-1])])
            elif ((is_right[-2]) not in ins) and ((is_right[-1]) in ins):
                supp = phis[int(is_right[-2])].__or__(x[int(is_right[-1])])
            else:
                supp = phis[int(is_right[-2])].__or__(phis[int(is_right[-1])])

            if len(is_right) > 2:
                for variable in is_right[:-2]:
                    if variable in ins:
                        supp = supp.__or__(x[int(variable)])    
                    else:
                        supp = supp.__or__(phis[int(variable)])    

            phis[int(i_left[0])] = supp
            x[int(i_left[0])].equiv(supp)
            phis_used.append(int(i_left[0]))
            del supp

        elif right_side.startswith("NOR"):
            if ((is_right[-2]) in ins) and ((is_right[-1]) in ins):
                supp = x[int(is_right[-2])].__or__(x[int(is_right[-1])])
            elif ((is_right[-2]) in ins) and ((is_right[-1]) not in ins):
                supp = x[int(is_right[-2])].__or__(phis[int(is_right[-1])])
            elif ((is_right[-2]) not in ins) and ((is_right[-1]) in ins):
                supp = phis[int(is_right[-2])].__or__(x[int(is_right[-1])])
            else:
                supp = phis[int(is_right[-2])].__or__(phis[int(is_right[-1])])

            if len(is_right) > 2:
                for variable in is_right[:-2]:
                    if variable in ins:
                        supp = supp.__or__(x[int(variable)])    
                    else:
                        supp = supp.__or__(phis[int(variable)])

            supp = supp.__invert__()
            phis[int(i_left[0])] = supp
            x[int(i_left[0])].equiv(supp)
            phis_used.append(int(i_left[0]))
            del supp
        else:
            raise ValueError(f"Unsupported operation: {right_side}")


    for eq in equations2:
        left_side, right_side = eq.split(' = ')
        i_left = re.findall(pattern, left_side)
        is_right = re.findall(pattern, right_side)
        ins = [re.findall(r'\d+', item)[0] for item in inputsT]

        if right_side.startswith("NAND"):
            if ((is_right[-2]) in ins) and ((is_right[-1]) in ins):
                supp = x[int(is_right[-2])].__and__(x[int(is_right[-1])])
            elif ((is_right[-2]) in ins) and ((is_right[-1]) not in ins):
                supp = x[int(is_right[-2])].__and__(psys[int(is_right[-1])])
            elif ((is_right[-2]) not in ins) and ((is_right[-1]) in ins):
                supp = psys[int(is_right[-2])].__and__(x[int(is_right[-1])])
            else:
                supp = psys[int(is_right[-2])].__and__(psys[int(is_right[-1])])

            if len(is_right) > 2:
                for variable in is_right[:-2]:
                    if variable in ins:
                        supp = supp.__and__(x[int(variable)])
                    else:
                        supp = supp.__and__(psys[int(variable)])

            supp = supp.__invert__()
            psys[int(i_left[0])] = supp
            x[int(i_left[0])].equiv(supp)  
            psys_used.append(int(i_left[0]))
            del supp

        elif right_side.startswith("AND"):
            if ((is_right[-2]) in ins) and ((is_right[-1]) in ins):
                supp = x[int(is_right[-2])].__and__(x[int(is_right[-1])])
            elif ((is_right[-2]) in ins) and ((is_right[-1]) not in ins):
                supp = x[int(is_right[-2])].__and__(psys[int(is_right[-1])])
            elif ((is_right[-2]) not in ins) and ((is_right[-1]) in ins):
                supp = psys[int(is_right[-2])].__and__(x[int(is_right[-1])])
            else:
                supp = psys[int(is_right[-2])].__and__(psys[int(is_right[-1])])

            if len(is_right) > 2:
                for variable in is_right[:-2]:
                    if variable in ins:
                        supp = supp.__and__(x[int(variable)])
                    else:
                        supp = supp.__and__(psys[int(variable)])

            psys[int(i_left[0])] = supp
            x[int(i_left[0])].equiv(supp)
            psys_used.append(int(i_left[0]))
            del supp

        elif right_side.startswith("NOT"):
            if is_right[0] in ins:
                supp = (x[int(is_right[0])].__invert__())
            else:
                supp = psys[int(is_right[0])].__invert__()
            psys[int(i_left[0])] = supp

            x[int(i_left[0])].equiv(supp)
            psys_used.append(int(i_left[0]))
            del supp

        elif right_side.startswith("OR"):
            if ((is_right[-2]) in ins) and ((is_right[-1]) in ins):
                supp = x[int(is_right[-2])].__or__(x[int(is_right[-1])])
            elif ((is_right[-2]) in ins) and ((is_right[-1]) not in ins):
                supp = x[int(is_right[-2])].__or__(psys[int(is_right[-1])])
            elif ((is_right[-2]) not in ins) and ((is_right[-1]) in ins):
                supp = psys[int(is_right[-2])].__or__(x[int(is_right[-1])])
            else:
                supp = psys[int(is_right[-2])].__or__(psys[int(is_right[-1])])

            if len(is_right) > 2:
                for variable in is_right[:-2]:
                    if variable in ins:
                        supp = supp.__or__(x[int(variable)])    
                    else:
                        supp = supp.__or__(psys[int(variable)])

            psys[int(i_left[0])] = supp
            x[int(i_left[0])].equiv(supp)
            psys_used.append(int(i_left[0]))
            del supp

        elif right_side.startswith("NOR"):
            if ((is_right[-2]) in ins) and ((is_right[-1]) in ins):
                supp = x[int(is_right[-2])].__or__(x[int(is_right[-1])])
            elif ((is_right[-2]) in ins) and ((is_right[-1]) not in ins):
                supp = x[int(is_right[-2])].__or__(psys[int(is_right[-1])])
            elif ((is_right[-2]) not in ins) and ((is_right[-1]) in ins):
                supp = psys[int(is_right[-2])].__or__(x[int(is_right[-1])])
            else:
                supp = psys[int(is_right[-2])].__or__(psys[int(is_right[-1])])

            if len(is_right) > 2:
                for variable in is_right[:-2]:
                    if variable in ins:
                        supp = supp.__or__(x[int(variable)])    
                    else:
                        supp = supp.__or__(psys[int(variable)])

            supp = supp.__invert__()
            psys[int(i_left[0])] = supp
            x[int(i_left[0])].equiv(supp)
            psys_used.append(int(i_left[0]))
            del supp

        else:
            raise ValueError(f"Unsupported operation: {right_side}")


    outputs1 = str(outputs1)
    indeces1 = re.findall(pattern, outputs1)
    outputs2 = str(outputs2)
    indeces2 = re.findall(pattern, outputs2)

    lefties = []
    for eq in equations1:
        left_side, right_side = eq.split(' = ')
        i_left = re.findall(pattern, left_side)
        lefties.append(i_left[0])

    for index in indeces1:
        if index not in lefties:
            phis[int(index)] = psys[int(index)]

    for index in indeces2:
        if index not in lefties:
            phis[int(index)] = psys[int(index)]

    supp = phis[int(indeces1[0])].equiv(psys[int(indeces2[0])])
    for j in range(len(indeces1[1:])):
        supp = supp.__and__(phis[int(indeces1[j+1])].equiv(psys[int(indeces2[j+1])]))
    gamma = supp 
    del supp


    '''ONLY FOR TESTINFG PURPOSES'''
    for j in range(len(indeces1)):
        if not phis[int(indeces1[j])].equiv(psys[int(indeces2[j])]).valid():
            print(f'Error: phis {indeces1[j]} and psys {indeces2[j]} are not equivalent.')

    return gamma

gamma = ultimate_function(S, T, outputsS, outputsT)
print(gamma.valid())
print('eureka')