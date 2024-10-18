import re

def mapping(raw_S, inputs, outputs):

    def pre_mapping(raw_S, inputs, outputs):
        # Check if an element is in the form 'x' followed by a number
        def is_xn(element):
            return bool(re.match(r"x\d+", element))

        # Function to perform substitution in a list
        def substitute_in_list(lst, old_value, new_value):
            return [new_value if not is_xn(item) and item == old_value else item for item in lst]
        
        def substitute_in_S(lst, old_value, new_value):
            updated_lst = []
            for expression in lst:
                # Check if old_value is to the left of '='
                if re.search(rf'^\s*{re.escape(old_value)}\s*=', expression):
                    # Replace old_value with new_value
                    expression = expression.replace(old_value, new_value)
                # Check if old_value is inside parentheses after an operator
                elif re.search(rf'[^=]*\(\s*.*?\b{re.escape(old_value)}\b\s*\)', expression):
                    # Replace old_value with new_value
                    expression = expression.replace(old_value, new_value)
                # Check if old_value appears anywhere as a whole word
                elif re.search(rf'\b{re.escape(old_value)}\b', expression):
                    expression = expression.replace(old_value, new_value)
                updated_lst.append(expression)
            return updated_lst
        

        # Create a list of tuples (list_name, list) and sort by length
        lists = [
            ("inputs", inputs),
            ("outputs", outputs)
        ]
        sorted_lists = sorted(lists, key=lambda x: len(x[1]))

        # Initialize substitution index
        c = 1

        # Iterate through sorted lists
        for list_name, current_list in sorted_lists:
            for value in current_list:
                replacement = f"x{c}"
                
                # Substitute in all three lists
                new_raw_S = substitute_in_S(raw_S, value, replacement)
                new_inputs = substitute_in_list(inputs, value, replacement)
                new_outputs = substitute_in_list(outputs, value, replacement)

                # If any substitution occurred, update the lists and increment the counter
                if new_raw_S != raw_S or new_inputs != inputs or new_outputs != outputs:
                    raw_S = new_raw_S
                    inputs = new_inputs
                    outputs = new_outputs
                    c += 1

        return raw_S, inputs, outputs, c

    def mapping_refinement(raw_list, start):
        def substitute_in_S(lst, old_value, new_value):
            updated_lst = []
            for expression in lst:
                # Check if old_value is to the left of '='
                if re.search(rf'^\s*{re.escape(old_value)}\s*=', expression):
                    # Replace old_value with new_value
                    expression = expression.replace(old_value, new_value)
                # Check if old_value is inside parentheses after an operator
                elif re.search(rf'[^=]*\(\s*.*?\b{re.escape(old_value)}\b\s*\)', expression):
                    # Replace old_value with new_value
                    expression = expression.replace(old_value, new_value)
                # Check if old_value appears anywhere as a whole word
                elif re.search(rf'\b{re.escape(old_value)}\b', expression):
                    expression = expression.replace(old_value, new_value)
                updated_lst.append(expression)
            return updated_lst
        
        variable_index = start  # Starting index for substitution
        substituted_list = []

        for expression in raw_list:
            left_side, right_side = expression.split(' = ')
            
            # Check the left side variable
            if not re.match(r'x\d+', left_side):  # If it's not of the form xN
                substituted_var = f"x{variable_index}"
                raw_list = substitute_in_S(raw_list, left_side, substituted_var)
                variable_index += 1

            # Find function calls and extract variables inside parentheses
            sub_elements = []  # Use a list to store elements
            matches = re.findall(r'\b\w+\(([^)]+)\)', right_side)  # Matches 'function(args)'

            for match in matches:
                # Split by commas and strip whitespace
                args = [arg.strip() for arg in match.split(',')]
                for arg in args:
                    if arg not in sub_elements:  # Avoid duplicates
                        sub_elements.append(arg)  # Add found arguments to the list

            # Substitute variables in the right side
            for var in sub_elements:
                if not re.match(r'x\d+', var):  # Check if it’s not in the form xN
                    substituted_var = f"x{variable_index}"
                    right_side = right_side.replace(var, substituted_var)
                    raw_list = substitute_in_S(raw_list, var, substituted_var)
                    variable_index += 1

            substituted_expression = f"{left_side} = {right_side}"
            substituted_list.append(substituted_expression)

        return raw_list
    
    updated_raw_S, updated_inputs, updated_outputs, start = pre_mapping(raw_S, inputs, outputs)
    updated_raw_S = mapping_refinement(updated_raw_S, start)

    return updated_raw_S, updated_inputs, updated_outputs