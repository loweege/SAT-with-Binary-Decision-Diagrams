import re
from oxidd.bdd import BDDManager
from mapping import mapping, reordering
from util import read_file
manager = BDDManager(100_000_000, 1_000_000, 8)

n = '01'
file_path2 = f'circuit-verification/circuit-bench/circuit{n}_opt.bench'
file_path1 = f'circuit-verification/circuit-bench/circuit{n}.bench'

inputs1, outputs1, raw_S1, output_numbers1 = read_file(file_path1)
inputs2, outputs2, raw_S2, output_numbers2 = read_file(file_path2)

S, inputsS, outputsS, T, inputsT, outputsT = mapping(raw_S1, inputs1, outputs1, raw_S2, inputs2, outputs2)
S = reordering(S, inputsS)
T = reordering(T, inputsT)

x = [manager.new_var() for i in range(100000)]
phis = [manager.new_var() for i in range(100000)]
psys = [manager.new_var() for i in range(100000)]

def gate_diagrammization(circuit, pattern, alphas):
    for gate in circuit:
        left_side, right_side = gate.split(' = ')
        i_left = re.findall(pattern, left_side)
        is_right = re.findall(pattern, right_side)
        ins = [re.findall(r'\d+', item)[0] for item in inputsT]

        if right_side.startswith("NAND"):
            if ((is_right[-2]) in ins) and ((is_right[-1]) in ins):
                supp = x[int(is_right[-2])].__and__(x[int(is_right[-1])])
            elif ((is_right[-2]) in ins) and ((is_right[-1]) not in ins):
                supp = x[int(is_right[-2])].__and__(alphas[int(is_right[-1])])
            elif ((is_right[-2]) not in ins) and ((is_right[-1]) in ins):
                supp = alphas[int(is_right[-2])].__and__(x[int(is_right[-1])])
            else:
                supp = alphas[int(is_right[-2])].__and__(alphas[int(is_right[-1])])

            if len(is_right) > 2:
                for variable in is_right[:-2]:
                    if variable in ins:
                        supp = supp.__and__(x[int(variable)])
                    else:
                        supp = supp.__and__(alphas[int(variable)])

            supp = supp.__invert__()
            alphas[int(i_left[0])] = supp
            x[int(i_left[0])].equiv(supp)  
            del supp

        elif right_side.startswith("AND"):
            if ((is_right[-2]) in ins) and ((is_right[-1]) in ins):
                supp = x[int(is_right[-2])].__and__(x[int(is_right[-1])])
            elif ((is_right[-2]) in ins) and ((is_right[-1]) not in ins):
                supp = x[int(is_right[-2])].__and__(alphas[int(is_right[-1])])
            elif ((is_right[-2]) not in ins) and ((is_right[-1]) in ins):
                supp = alphas[int(is_right[-2])].__and__(x[int(is_right[-1])])
            else:
                supp = alphas[int(is_right[-2])].__and__(alphas[int(is_right[-1])])

            if len(is_right) > 2:
                for variable in is_right[:-2]:
                    if variable in ins:
                        supp = supp.__and__(x[int(variable)])
                    else:
                        supp = supp.__and__(alphas[int(variable)])

            alphas[int(i_left[0])] = supp
            x[int(i_left[0])].equiv(supp)
            del supp

        elif right_side.startswith("NOT"):
            if is_right[0] in ins:
                supp = (x[int(is_right[0])].__invert__())
            else:
                supp = alphas[int(is_right[0])].__invert__()
            alphas[int(i_left[0])] = supp

            x[int(i_left[0])].equiv(supp)
            del supp

        elif right_side.startswith("OR"):
            if ((is_right[-2]) in ins) and ((is_right[-1]) in ins):
                supp = x[int(is_right[-2])].__or__(x[int(is_right[-1])])
            elif ((is_right[-2]) in ins) and ((is_right[-1]) not in ins):
                supp = x[int(is_right[-2])].__or__(alphas[int(is_right[-1])])
            elif ((is_right[-2]) not in ins) and ((is_right[-1]) in ins):
                supp = alphas[int(is_right[-2])].__or__(x[int(is_right[-1])])
            else:
                supp = alphas[int(is_right[-2])].__or__(alphas[int(is_right[-1])])

            if len(is_right) > 2:
                for variable in is_right[:-2]:
                    if variable in ins:
                        supp = supp.__or__(x[int(variable)])    
                    else:
                        supp = supp.__or__(alphas[int(variable)])

            alphas[int(i_left[0])] = supp
            x[int(i_left[0])].equiv(supp)
            del supp

        elif right_side.startswith("NOR"):
            if ((is_right[-2]) in ins) and ((is_right[-1]) in ins):
                supp = x[int(is_right[-2])].__or__(x[int(is_right[-1])])
            elif ((is_right[-2]) in ins) and ((is_right[-1]) not in ins):
                supp = x[int(is_right[-2])].__or__(alphas[int(is_right[-1])])
            elif ((is_right[-2]) not in ins) and ((is_right[-1]) in ins):
                supp = alphas[int(is_right[-2])].__or__(x[int(is_right[-1])])
            else:
                supp = alphas[int(is_right[-2])].__or__(alphas[int(is_right[-1])])

            if len(is_right) > 2:
                for variable in is_right[:-2]:
                    if variable in ins:
                        supp = supp.__or__(x[int(variable)])    
                    else:
                        supp = supp.__or__(alphas[int(variable)])

            supp = supp.__invert__()
            alphas[int(i_left[0])] = supp
            x[int(i_left[0])].equiv(supp)
            del supp

        else:
            raise ValueError(f"Unsupported operation: {right_side}")

def ultimate_function(circuit1, circuit2, outputs1, outputs2):
    pattern = r'x(\d+)'

    gate_diagrammization(circuit1, pattern, phis)
    gate_diagrammization(circuit2, pattern, psys)

    outputs1 = str(outputs1)
    indeces1 = re.findall(pattern, outputs1)
    outputs2 = str(outputs2)
    indeces2 = re.findall(pattern, outputs2)

    lefties = []
    for gate in circuit1:
        left_side, right_side = gate.split(' = ')
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

    return gamma

gamma = ultimate_function(S, T, outputsS, outputsT)
print('----------------------------Are-the-two-circuits-equivalent?------------------------------------')
print(gamma.valid())
