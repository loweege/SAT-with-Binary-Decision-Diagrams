import re
def parsing(file_path, apprx):

    def decimal_to_binary(num):
        binary = bin(num)[2:]
        return binary.zfill(apprx)

    with open(file_path, 'r') as f:
        file_content = f.read()
        lines = file_content.strip().splitlines()

        raw_source_states = []
        raw_destination_states = []
        raw_accepting_states = []

        for line in lines:
            if '->' in line:  
                start = line.find(',') + 1
                end = line.find('->')
                raw_source_states.append(line[start:end].strip())
                raw_destination_states.append(line[end + 2:].strip())  # +2 to skip the '->' symbol
            else:
                raw_accepting_states.append(line.strip())

        source_states = []
        destination_states = []
        accepting_states = []

        supp_merge =  raw_source_states + raw_destination_states

        def convert_to_binary(numbers):
            supp = [element for element in numbers if element]
            longest_state = max(supp_merge, key=len)
            longest_state = re.split(r'[ |\[\]\s|]+', longest_state)
            longest_state = [element for element in longest_state if element]
            state_length = len(longest_state)

            binary_numbers = []
            for number in numbers:
                converted_number = ""
                if number == '255':
                    binary_char = '1100'
                    converted_number += binary_char
                elif number == '(ERR)':
                    converted_number = '1' * state_length * 4
                    binary_numbers.append(converted_number)
                    continue
                else:
                    for char in number:
                        if (char == '0' or char == '1' or char == '2' or char == '3' or char == '4' or char == '5'
                            or char == '6' or char == '7' or char == '8' or char == '9'):  
                            binary_char = decimal_to_binary(int(char)) 
                            converted_number += binary_char
                        else:
                            converted_number += char 
                binary_numbers.append(converted_number)
            if (file_path != 'finite-state-automata/finite-state-automata/fischer.3.1.c.ba' and 
                file_path != 'finite-state-automata/finite-state-automata/fischer.3.2.c.ba' and
                file_path != 'finite-state-automata/finite-state-automata/fischer.3.c.ba' and
                file_path != 'finite-state-automata/finite-state-automata/mcs.1.2.c.ba'
                ):
                return " ".join(binary_numbers)
            else:
                if len(supp) == state_length:
                    return " ".join(binary_numbers)
                else:
                    pip = " ".join(binary_numbers)
                    pip += "1011 " * (state_length - len(supp))
                    return pip

        for portion in raw_source_states:
            numbers = re.split(r'[ |\[\]\s|]+', portion) 
            source_states.append(convert_to_binary(numbers))

        for portion in raw_destination_states:
            numbers = re.split(r'[ |\[\]\s|]+', portion)
            destination_states.append(convert_to_binary(numbers))

        for portion in raw_accepting_states:
            numbers = re.split(r'[ |\[\]\s|]+', portion)
            accepting_states.append(convert_to_binary(numbers))

        transitions_raw = []
        for src, dest in zip(source_states, destination_states):
            transitions_raw.append(f"{src} -> {dest}")

        def extract_zeros_ones(input_string):
            cleaned_string = input_string.replace('[', '').replace(']', '').replace('|', '').replace('->', '').replace(' ', '')
            zeros_ones_string = ''.join([char for char in cleaned_string if char in ('0', '1')])
            return zeros_ones_string

        def extract_zeros_ones_from_list(input_list):
            result_list = [extract_zeros_ones(s) for s in input_list]
            return result_list

        source_state = extract_zeros_ones(source_states[0])    
        transitions = extract_zeros_ones_from_list(transitions_raw)
        accepting_states = extract_zeros_ones_from_list(accepting_states)

        return source_state, transitions, accepting_states

def variable_number_calculation(file_path, approx):
    with open(file_path, 'r') as f:
        file_content = f.read()
        lines = file_content.strip().splitlines()

        def count_numbers_in_string(s):
            count = 0
            start = s.find(',') + 1
            end = s.find('->')
            filtered = s[start:end].strip()

            for char in filtered:
                if char.isdigit(): 
                    count += 1
            return count
        
    return count_numbers_in_string(lines[0]) * 2 * approx
