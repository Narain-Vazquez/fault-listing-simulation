def fault_calculation(user_input):

    file = open(user_input, 'r')
    lines = file.readlines()

    gate_type_IO = {}
    gate_type = {}
    fault_list_inputs = []
    fault_list_outputs = []
    fault_list_gates = {}

    for formatted_line in lines:
    
        formatted_line = formatted_line.strip()

        if not formatted_line.startswith("#"):
            
            formatted_line = formatted_line.strip()

            # I/O
            location_input = formatted_line.find('INPUT')
            location_output = formatted_line.find('OUTPUT')

            # AND
            location_and = formatted_line.find('AND')
            location_nand = formatted_line.find('NAND')

            # OR
            location_or = formatted_line.find('OR')
            location_nor = formatted_line.find('NOR')
            location_xor = formatted_line.find('XOR')

            # Other
            location_buff = formatted_line.find('BUFF')
            location_not = formatted_line.find('NOT')

            location_equal = formatted_line.find('=')
            location_finder = formatted_line.find(')')

        ##################################################################
            
            if location_input != -1:
                node = formatted_line[location_input + 6:-1].strip()
                node_f1 = node + '-0'
                node_f2 = node + '-1'
                gate_type_IO[node] = 'INPUT'
                if node_f1 not in fault_list_inputs:
                    fault_list_inputs.append(node_f1)
                if node_f2 not in fault_list_inputs:
                    fault_list_inputs.append(node_f2)

        ##################################################################
            
            elif location_output != -1:
                node = formatted_line[location_output + 7:-1].strip()
                node_f1 = node + '-out-0'
                node_f2 = node + '-out-1'
                gate_type_IO[node] = 'OUTPUT'
                if node_f1 not in fault_list_outputs:
                    fault_list_outputs.append(node_f1)
                if node_f2 not in fault_list_outputs:
                    fault_list_outputs.append(node_f2)

        ##################################################################
            
            elif location_and != -1 and location_nand == -1:
                gate_output = formatted_line[:location_equal].strip()
                inputs = formatted_line[location_and + 4:-1].split(',')

                gate_type[gate_output] = 'AND'
                if gate_output not in fault_list_gates:
                    fault_list_gates[gate_output] = []

                gate_output_0 = gate_output + '-0'
                gate_output_1 = gate_output + '-1'
                if gate_output_0 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_0)
                if gate_output_1 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_1)

                for input_node in inputs:
                    cleaned = input_node.strip()
                    cleaned_0 = cleaned + f'-{gate_output}-0'
                    cleaned_1 = cleaned + f'-{gate_output}-1'
                    if cleaned_0 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_0)
                    if cleaned_1 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_1)

        ##################################################################
            
            elif location_nand != -1:
                gate_output = formatted_line[:location_equal].strip()
                inputs = formatted_line[location_nand + 5:-1].split(',')

                gate_type[gate_output] = 'NAND'
                if gate_output not in fault_list_gates:
                    fault_list_gates[gate_output] = []
                
                gate_output_0 = gate_output + '-0'
                gate_output_1 = gate_output + '-1'
                if gate_output_0 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_0)
                if gate_output_1 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_1)
                
                for input_node in inputs:
                    cleaned = input_node.strip()
                    cleaned_0 = cleaned + f'-{gate_output}-0'
                    cleaned_1 = cleaned + f'-{gate_output}-1'
                    if cleaned_0 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_0)
                    if cleaned_1 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_1)
                    
        ##################################################################
            
            elif location_or != -1 and location_nor == -1 and location_xor == -1:
                gate_output = formatted_line[:location_equal].strip()
                inputs = formatted_line[location_or + 3:-1].split(',')

                gate_type[gate_output] = 'OR'
                if gate_output not in fault_list_gates:
                    fault_list_gates[gate_output] = []

                gate_output_0 = gate_output + '-0'
                gate_output_1 = gate_output + '-1'
                if gate_output_0 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_0)
                if gate_output_1 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_1)

                for input_node in inputs:
                    cleaned = input_node.strip()
                    cleaned_0 = cleaned + f'-{gate_output}-0'
                    cleaned_1 = cleaned + f'-{gate_output}-1'
                    if cleaned_0 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_0)
                    if cleaned_1 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_1)
                    
        ##################################################################

            elif location_nor != -1:
                gate_output = formatted_line[:location_equal].strip()
                inputs = formatted_line[location_nor + 4:-1].split(',')

                gate_type[gate_output] = 'NOR'
                if gate_output not in fault_list_gates:
                    fault_list_gates[gate_output] = []

                gate_output_0 = gate_output + '-0'
                gate_output_1 = gate_output + '-1'
                if gate_output_0 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_0)
                if gate_output_1 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_1)

                for input_node in inputs:
                    cleaned = input_node.strip()
                    cleaned_0 = cleaned + f'-{gate_output}-0'
                    cleaned_1 = cleaned + f'-{gate_output}-1'
                    if cleaned_0 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_0)
                    if cleaned_1 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_1)
        
        ##################################################################

            elif location_xor != -1:
                gate_output = formatted_line[:location_equal].strip()
                inputs = formatted_line[location_xor + 4:-1].split(',')

                gate_type[gate_output] = 'XOR'
                if gate_output not in fault_list_gates:
                    fault_list_gates[gate_output] = []
                
                gate_output_0 = gate_output + '-0'
                gate_output_1 = gate_output + '-1'
                if gate_output_0 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_0)
                if gate_output_1 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_1)
                
                for input_node in inputs:
                    cleaned = input_node.strip()
                    cleaned_0 = cleaned + f'-{gate_output}-0'
                    cleaned_1 = cleaned + f'-{gate_output}-1'
                    if cleaned_0 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_0)
                    if cleaned_1 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_1)

        ##################################################################
            
            elif location_not != -1:
                gate_output = formatted_line[:location_equal].strip()
                inputs = formatted_line[location_not + 4:-1].split(',')

                gate_type[gate_output] = 'NOT'
                if gate_output not in fault_list_gates:
                    fault_list_gates[gate_output] = []
            
                gate_output_0 = gate_output + '-0'
                gate_output_1 = gate_output + '-1'
                if gate_output_0 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_0)
                if gate_output_1 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_1)
            
                for input_node in inputs:
                    cleaned = input_node.strip()
                    cleaned_0 = cleaned + f'-{gate_output}-0'
                    cleaned_1 = cleaned + f'-{gate_output}-1'
                    if cleaned_0 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_0)
                    if cleaned_1 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_1)

        ##################################################################
            
            elif location_buff != -1:
                gate_output = formatted_line[:location_equal].strip()
                inputs = formatted_line[location_buff + 5:-1].split(',')

                gate_type[gate_output] = 'BUFF'
                if gate_output not in fault_list_gates:
                    fault_list_gates[gate_output] = []
            
                gate_output_0 = gate_output + '-0'
                gate_output_1 = gate_output + '-1'
                
                if gate_output_0 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_0)
                if gate_output_1 not in fault_list_gates[gate_output]:
                    fault_list_gates[gate_output].append(gate_output_1)
            
                for input_node in inputs:
                    cleaned = input_node.strip()
                    cleaned_0 = cleaned + f'-{gate_output}-0'
                    cleaned_1 = cleaned + f'-{gate_output}-1'
                    if cleaned_0 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_0)
                    if cleaned_1 not in fault_list_gates[gate_output]:
                        fault_list_gates[gate_output].append(cleaned_1)

    sorted_gate_outputs = sorted(fault_list_gates.keys())

    total_faults = 0

    for gate_output in sorted_gate_outputs:
        total_faults += len(fault_list_gates[gate_output])

    total_faults += len(fault_list_inputs)
    total_faults += len(fault_list_outputs)
    
    return {
        'total_faults': total_faults,
        'fault_list_inputs': fault_list_inputs,
        'fault_list_outputs': fault_list_outputs,
        'fault_list_gates': fault_list_gates,
        'gate_type': gate_type,
        'gate_type_IO': gate_type_IO
    }
    