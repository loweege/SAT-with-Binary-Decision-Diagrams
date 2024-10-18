import re
def parsing(file_path, apprx):

    def decimal_to_binary(num):
        # Convert the decimal number to binary using bin() and remove the '0b' prefix
        binary = bin(num)[2:]
        # Pad the binary string with leading zeros to ensure it's at least 5 characters long
        return binary.zfill(apprx)


    with open(file_path, 'r') as f:
        # Read the content of the file
        file_content = f.read()

        # Split the content by lines
        lines = file_content.strip().splitlines()

        # Initialize lists to store the portions of the lines
        raw_source_states = []
        raw_destination_states = []
        raw_accepting_states = []

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
            else:
                raw_accepting_states.append(line.strip())

        # Convert raw_source_states into source_states using decimal_to_binary
        source_states = []
        destination_states = []
        accepting_states = []

        supp_merge =  raw_source_states + raw_destination_states
        # Helper function to convert numbers in a portion to binary
        def convert_to_binary(numbers):

            # take the longest between the raw_source_states and the raw_destination_states
            
            
            supp = [element for element in numbers if element]


            longest_state = max(supp_merge, key=len)
            longest_state = re.split(r'[ |\[\]\s|]+', longest_state)
            longest_state = [element for element in longest_state if element]
            state_length = len(longest_state)
            #then compute the number of total element of a trsansition 

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
                            or char == '6' or char == '7' or char == '8' or char == '9'):  # Check if the character is a digit
                            binary_char = decimal_to_binary(int(char))  # Convert digit to binary
                            converted_number += binary_char
                        else:
                            converted_number += char  # Keep non-digit characters unchanged
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


        # Process source states
        for portion in raw_source_states:
            numbers = re.split(r'[ |\[\]\s|]+', portion)  # Split by space, |, [, and ]
            #numbers = portion.split()  # Split the portion by spaces
            source_states.append(convert_to_binary(numbers))

        # Process destination states
        for portion in raw_destination_states:
            numbers = re.split(r'[ |\[\]\s|]+', portion)  # Split by space, |, [, and ]
            destination_states.append(convert_to_binary(numbers))

        # Process accepting states
        for portion in raw_accepting_states:
            numbers = re.split(r'[ |\[\]\s|]+', portion)  # Split by space, |, [, and ]
            accepting_states.append(convert_to_binary(numbers))

        # Merge source_states and destination_states with '->' symbol
        transitions_raw = []
        for src, dest in zip(source_states, destination_states):
            transitions_raw.append(f"{src} -> {dest}")


        def extract_zeros_ones(input_string):
            # Remove non-relevant characters
            cleaned_string = input_string.replace('[', '').replace(']', '').replace('|', '').replace('->', '').replace(' ', '')
            
            # Keep only '0' and '1' characters and join them into a single string
            zeros_ones_string = ''.join([char for char in cleaned_string if char in ('0', '1')])
            return zeros_ones_string

        def extract_zeros_ones_from_list(input_list):
            # Process each string in the input list
            result_list = [extract_zeros_ones(s) for s in input_list]
            return result_list

        source_state = extract_zeros_ones(source_states[0])    
        transitions = extract_zeros_ones_from_list(transitions_raw)
        accepting_states = extract_zeros_ones_from_list(accepting_states)

        return source_state, transitions, accepting_states

def variable_number_calculation(file_path, approx):
    with open(file_path, 'r') as f:
        # Read the content of the file
        file_content = f.read()

        # Split the content by lines
        lines = file_content.strip().splitlines()

        def count_numbers_in_string(s):
            count = 0

            start = s.find(',') + 1
            end = s.find('->')
            filtered = s[start:end].strip()

            for char in filtered:
                if char.isdigit():  # Check if the character is a digit
                    count += 1
            return count
        
    return count_numbers_in_string(lines[0]) * 2 * approx
