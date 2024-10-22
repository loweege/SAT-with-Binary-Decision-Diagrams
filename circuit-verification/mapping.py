import re

def mapping(raw_S, inputs, outputs, raw_S2, inputs2, outputs2):

    def pre_mapping(raw_S, inputs, outputs, raw_S2, inputs2, outputs2):
        def is_xn(element):
            return bool(re.match(r"x\d+", element))

        def substitute_in_list(lst, old_value, new_value):
            return [new_value if not is_xn(item) and item == old_value else item for item in lst]
        
        def substitute_in_S(lst, old_value, new_value):
            updated_lst = []
            for expression in lst:
                if re.search(rf'^\s*{re.escape(old_value)}\s*=', expression):
                    expression = expression.replace(old_value, new_value)

                elif re.search(rf'[^=]*\(\s*.*?\b{re.escape(old_value)}\b\s*\)', expression):
                    expression = expression.replace(old_value, new_value)

                elif re.search(rf'\b{re.escape(old_value)}\b', expression):
                    expression = expression.replace(old_value, new_value)
                updated_lst.append(expression)
            return updated_lst
        

        lists = [
            ("inputs", inputs),
            ("outputs", outputs)
        ]
        sorted_lists = sorted(lists, key=lambda x: len(x[1]))

        c = 1

        for list_name, current_list in sorted_lists:
            for value in current_list:
                replacement = f"x{c}"
                
                # Substitute in all three lists
                new_raw_S = substitute_in_S(raw_S, value, replacement)
                new_inputs = substitute_in_list(inputs, value, replacement)
                new_outputs = substitute_in_list(outputs, value, replacement)
                new_raw_S2 = substitute_in_S(raw_S2, value, replacement)
                new_inputs2 = substitute_in_list(inputs2, value, replacement)
                new_outputs2 = substitute_in_list(outputs2, value, replacement)

                if (new_raw_S != raw_S or new_inputs != inputs or new_outputs != outputs or
                    new_raw_S2 != raw_S2 or new_inputs2 != inputs2 or new_outputs2 != outputs2) :
                    raw_S = new_raw_S
                    inputs = new_inputs
                    outputs = new_outputs
                    raw_S2 = new_raw_S2
                    inputs2 = new_inputs2
                    outputs2 = new_outputs2
                    c += 1

        return raw_S, inputs, outputs, c, raw_S2, inputs2, outputs2

    def mapping_refinement(raw_listS, raw_listS2, raw_list_inputs2, raw_list_outputs2, start):
        def is_xn(element):
            return bool(re.match(r"x\d+", element))

        def substitute_in_list(lst, old_value, new_value):
            return [new_value if not is_xn(item) and item == old_value else item for item in lst]
        
        def substitute_in_S(lst, old_value, new_value):
            updated_lst = []
            for expression in lst:
                if re.search(rf'^\s*{re.escape(old_value)}\s*=', expression):
                    expression = expression.replace(old_value, new_value)

                elif re.search(rf'[^=]*\(\s*.*?\b{re.escape(old_value)}\b\s*\)', expression):
                    expression = expression.replace(old_value, new_value)

                elif re.search(rf'\b{re.escape(old_value)}\b', expression):
                    expression = expression.replace(old_value, new_value)
                updated_lst.append(expression)
            return updated_lst
        
        variable_index = start 
        substituted_list = []

        for expression in raw_listS:
            left_side, right_side = expression.split(' = ')
            
            if not re.match(r'x\d+', left_side): 
                substituted_var = f"x{variable_index}"
                raw_listS = substitute_in_S(raw_listS, left_side, substituted_var)
                raw_listS2 = substitute_in_S(raw_listS2, left_side, substituted_var)
                raw_list_inputs2 = substitute_in_list(raw_list_inputs2, left_side, substituted_var)
                raw_list_outputs2 = substitute_in_list(raw_list_outputs2, left_side, substituted_var)
                variable_index += 1

            sub_elements = [] 
            matches = re.findall(r'\b\w+\(([^)]+)\)', right_side) 

            for match in matches:
                args = [arg.strip() for arg in match.split(',')]
                for arg in args:
                    if arg not in sub_elements:  
                        sub_elements.append(arg) 

            # Substitute variables in the right side
            for var in sub_elements:
                if not re.match(r'x\d+', var): 
                    substituted_var = f"x{variable_index}"
                    right_side = right_side.replace(var, substituted_var)

                    raw_listS = substitute_in_S(raw_listS, var, substituted_var)
                    raw_listS2 = substitute_in_S(raw_listS2, var, substituted_var)
                    raw_list_inputs2 = substitute_in_list(raw_list_inputs2, var, substituted_var)
                    raw_list_outputs2 = substitute_in_list(raw_list_outputs2, var, substituted_var)

                    variable_index += 1

            substituted_expression = f"{left_side} = {right_side}"
            substituted_list.append(substituted_expression)

        for expression in raw_listS2:
            print(expression)
            left_side, right_side = expression.split(' = ')
            
            if not re.match(r'x\d+', left_side): 
                substituted_var = f"x{variable_index}"
                raw_listS2 = substitute_in_S(raw_listS2, left_side, substituted_var)
                raw_list_inputs2 = substitute_in_list(raw_list_inputs2, left_side, substituted_var)
                raw_list_outputs2 = substitute_in_list(raw_list_outputs2, left_side, substituted_var)
                variable_index += 1

            sub_elements = [] 
            matches = re.findall(r'\b\w+\(([^)]+)\)', right_side) 

            for match in matches:
                args = [arg.strip() for arg in match.split(',')]
                for arg in args:
                    if arg not in sub_elements:  
                        sub_elements.append(arg) 

            # Substitute variables in the right side
            for var in sub_elements:
                if not re.match(r'x\d+', var): 
                    substituted_var = f"x{variable_index}"
                    right_side = right_side.replace(var, substituted_var)

                    raw_listS2 = substitute_in_S(raw_listS2, var, substituted_var)
                    raw_list_inputs2 = substitute_in_list(raw_list_inputs2, var, substituted_var)
                    raw_list_outputs2 = substitute_in_list(raw_list_outputs2, var, substituted_var)

                    variable_index += 1

            substituted_expression = f"{left_side} = {right_side}"
            substituted_list.append(substituted_expression)

        return raw_listS, raw_listS2, raw_list_inputs2, raw_list_outputs2
    
    updated_raw_S, updated_inputs, updated_outputs, start, updated_raw_s2, updated_inputs2, updated_outputs2 = pre_mapping(raw_S, inputs, outputs, raw_S2, inputs2, outputs2)
    updated_raw_S, updated_raw_s2, updated_inputs2, updated_outputs2 = mapping_refinement(updated_raw_S ,updated_raw_s2, updated_inputs2, updated_outputs2, start)

    return updated_raw_S, updated_inputs, updated_outputs, updated_raw_s2, updated_inputs2, updated_outputs2

def reordering(S, inputsS):
    new_list = []
    def subroutine1(equations, ins):
        n = -1
        while len(new_list) != n:
            #print(len(new_list), len(equations))
            #514 - 652
            n = len(new_list)
            for eq in equations:
                rhs = eq.split('=')[1].strip()
                lhs = eq.split('=')[0].strip()
                lhs = re.findall(r'\d+', lhs)
                lhs = lhs[0]

                rights = re.findall(r'\d+', rhs)
                
                if all(right in ins or right in new_list for right in rights):
                    if lhs not in new_list: 
                        new_list.append(lhs)

    ins = [re.findall(r'\d+', item)[0] for item in inputsS]
    subroutine1(S, ins)

    new_S = []
    for l in new_list:
        for eq in S:
            rhs = eq.split('=')[1].strip()
            lhs = eq.split('=')[0].strip()
            lhs = re.findall(r'\d+', lhs)
            lhs = lhs[0]

            if l == lhs:
                new_S.append(eq)
                print(eq)
                break

    return new_S