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
