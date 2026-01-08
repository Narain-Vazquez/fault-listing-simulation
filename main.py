import levelization
import listing_faults
import imply
import pprint

while True:
    # Request user input for file and action choice
    user_input = input('Enter file name: ')
    print('Enter character for what you want to do')
    print('A - Fault listing')
    print('B - Circ sim')
    print('C - Fault sim')
    print('Q - Exit')
    user_input2 = input('Enter choice: ')
    if user_input2 == 'Q':
        print("Exiting the program.")
        break

    # Perform node levelization and fault calculation
    level_data = levelization.node_levelization(user_input)
    fault_data = listing_faults.fault_calculation(user_input)

    '''
    'total_faults': total_faults,
            'fault_list_inputs': fault_list_inputs,
            'fault_list_outputs': fault_list_outputs,
            'fault_list_gates': fault_list_gates,
            'gate_type': gate_type,
            'gate_type_IO': gate_type_IO
    '''
    faults_detected_inputs = []
    faults_detected_outputs = []
    faults_detected_gates = []

    #print(level_data['circuit_inputs'])

    input_circuit_evaluate = {}

    #*******************************************************************************************************************************************

    if user_input2 == 'A' or user_input2 == 'a':
        
        
        # i generated the print out with chatgpt
        print("========== Fault Listing ==========\n")

        print("Stuck-at Faults for Inputs\n")
        for fault in fault_data['fault_list_inputs']:
            print(f"  {fault}")

        print("\nStuck-at Faults for Outputs\n")
        for fault in fault_data['fault_list_outputs']:
            print(f"  {fault}")

        print("\nStuck-at Faults for Internal Nodes (Gates)\n")
        sorted_gate_outputs = sorted(fault_data['fault_list_gates'].keys())
        for gate_output in sorted_gate_outputs:
            print(f"\n  Gate: {gate_output} ({fault_data['gate_type'][gate_output]})")
            for fault in fault_data['fault_list_gates'][gate_output]:
                print(f"    {fault}")
        
        pprint.pprint(fault_data['fault_list_inputs'])
        pprint.pprint(fault_data['fault_list_outputs'])
        pprint.pprint(fault_data['fault_list_gates'])
        print(f"Total number of faults: {fault_data['total_faults']}")

    #*******************************************************************************************************************************************

    elif user_input2 == 'B' or user_input2 == 'b':
        print('Enter character for input of the TV')
        print('A - All-0 vector')
        print('B - All-1 vector')
        
        user_input3 = input('Enter choice: ')
        if(user_input3 == 'A' or user_input3 == 'a'):
            kak = 0
        elif user_input3 == 'B' or user_input3 == 'b':
            kak = 1
            
        for node in level_data['circuit_inputs']:
        
            #kak = input(f'Enter input value for {node}: ')
            input_circuit_evaluate[node] = int(kak)
            
        output_values = imply.evaluate_circuit(input_circuit_evaluate, level_data['circuit_gates'], level_data['node_prerequiste'])

        for node, val in output_values.items():
            print(f'{node}: {val}')
        
    #pprint.pprint(level_data['node_prerequiste'])
    #pprint.pprint(fault_data['gate_type'])
    #pprint.pprint(fault_data['gate_type_IO'])
    #pprint.pprint(fault_data['fault_list_gates'])

    #*******************************************************************************************************************************************

    elif user_input2 == 'C' or user_input2 == 'c':
        
        print('Enter your TV for each input')
        
        for node in level_data['circuit_inputs']:
            
            kak = input(f'Enter input value for {node}: ')
            input_circuit_evaluate[node] = int(kak)

        print('Choices')
        print('A - find specific fault')
        print('B - give all faults found')
        user_input4 = input('Enter choice: ')
        
        if(user_input4 == 'A' or user_input4 == 'a'):
            print("========== Fault Listing ==========\n")

            print("Stuck-at Faults for Inputs\n")
            for fault in fault_data['fault_list_inputs']:
                print(f"  {fault}")

            print("\nStuck-at Faults for Outputs\n")
            for fault in fault_data['fault_list_outputs']:
                print(f"  {fault}")

            print("\nStuck-at Faults for Internal Nodes (Gates)\n")
            sorted_gate_outputs = sorted(fault_data['fault_list_gates'].keys())
            for gate_output in sorted_gate_outputs:
                print(f"\n  Gate: {gate_output} ({fault_data['gate_type'][gate_output]})")
                for fault in fault_data['fault_list_gates'][gate_output]:
                    print(f"    {fault}")
                    
            print('\nAbove is all the faults')
            user_input5 = input('Enter fault you want to detect: ')

        output_values = imply.evaluate_circuit(input_circuit_evaluate, level_data['circuit_gates'], level_data['node_prerequiste'])
        
        '''
        for node, val in output_values.items():
            print(f'{node}: {val}')
        '''
        
        #print('XXXXXXXXXXXX')

        for node, value in output_values.items():
            if node in fault_data['gate_type_IO']:
                #print(f'{node}: {value}')
                #print(fault_data['gate_type_IO'][node])
                if fault_data['gate_type_IO'][node] == 'INPUT':
                    
                    for fault in fault_data['fault_list_inputs']:
                        
                        if fault.split('-')[0] == node.strip('\''):
                            
                            if (value == 1 and int(fault[-1]) != value):
                                faults_detected_inputs.append(fault)
                            elif (value == 0 and int(fault[-1]) != value):
                                faults_detected_inputs.append(fault)

                elif fault_data['gate_type_IO'][node] == 'OUTPUT':
                    
                    for fault in fault_data['fault_list_outputs']:
                        
                        if fault.split('-')[0] == node.strip('\''):
                            
                            if (value == 1 and int(fault[-1]) != value):
                                faults_detected_outputs.append(fault)
                            elif (value == 0 and int(fault[-1]) != value):
                                faults_detected_outputs.append(fault)
            
            if node in fault_data['gate_type']:

                if fault_data['gate_type'][node] == 'AND':
                    #print(f'{node}: {value} (AND)')
                    for fault, val in fault_data['fault_list_gates'].items():
                        
                        if fault.strip() == node.strip():
                            
                            if value == 1:
                                for fault_within_gate in val:
                                    #print(fault_within_gate)
                                    if int(fault_within_gate[-1]) == 0:
                                        faults_detected_gates.append(fault_within_gate)
                            
                            elif value == 0:
                                for prerequisite in level_data['node_prerequiste'][node]:
                                    #print(prerequisite)
                                    if output_values[prerequisite] == 0:
                                        #print('*********')
                                        #print(prerequisite)
                                        #print(output_values[prerequisite])
                                        for fault_within_gate in val:
                                            #print('$$$$$$$')
                                            #print(fault_within_gate)
                                            #print(output_values[fault_within_gate.split('-')[0]])
                                            #print(fault_within_gate[-1])
                                            if fault_within_gate.split('-')[0] == prerequisite and int(fault_within_gate[-1]) == 1 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate)
                                            if fault_within_gate.split('-')[0] == fault and int(fault_within_gate[-1]) == 1 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate) # + ' (collapsed by dominance)')
                                            if fault_within_gate.split('-')[0] != prerequisite and fault_within_gate.split('-')[0] != fault and output_values[fault_within_gate.split('-')[0]] != 0:
                                                if(int(fault_within_gate[-1]) == 0 and fault_within_gate not in faults_detected_gates):
                                                    faults_detected_gates.append(fault_within_gate)
                    #print('%%%%%%%%%%%%%%')

                ###########################################################################################################################################################

                elif fault_data['gate_type'][node] == 'NAND':
                    #print(f'{node}: {value} (NAND)')
                    for fault, val in fault_data['fault_list_gates'].items():
                        
                        if fault.strip() == node.strip():
                            
                            if value == 0:
                                for fault_within_gate in val:
                                    #print(fault_within_gate)
                                    #print(fault_within_gate.split('-')[0])
                                    #print('HHHHHHHHHHH')
                                    if int(fault_within_gate[-1]) == 0 and fault_within_gate.split('-')[0] != fault and fault_within_gate not in faults_detected_gates:
                                        #print('GGGGGGG')
                                        #print(fault_within_gate)
                                        faults_detected_gates.append(fault_within_gate)
                                    
                                    elif fault_within_gate.split('-')[0] == fault and fault_within_gate not in faults_detected_gates:
                                        if ( int(fault_within_gate[-1]) == 1):
                                            #print('LLLLLLLLLL')
                                            #print(fault_within_gate)
                                            faults_detected_gates.append(fault_within_gate)        
                                        
                            elif value == 1:
                                for prerequisite in level_data['node_prerequiste'][node]:
                                    if output_values[prerequisite] == 0:
                                        for fault_within_gate in val:
                                            if fault_within_gate.split('-')[0] == prerequisite and int(fault_within_gate[-1]) == 1 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate)
                                            if fault_within_gate.split('-')[0] == fault and int(fault_within_gate[-1]) == 0 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate) # + ' (collapsed by dominance)')
                                            if fault_within_gate.split('-')[0] != prerequisite and fault_within_gate.split('-')[0] != fault and output_values[fault_within_gate.split('-')[0]] != 0:
                                                if(int(fault_within_gate[-1]) == 0 and fault_within_gate not in faults_detected_gates):
                                                    faults_detected_gates.append(fault_within_gate)

                ###########################################################################################################################################################
                
                elif fault_data['gate_type'][node] == 'OR':
                    #print(f'{node}: {value} (OR)')
                    for fault, val in fault_data['fault_list_gates'].items():
                        if fault.strip() == node.strip():
                            if value == 0:
                                for fault_within_gate in val:
                                    if int(fault_within_gate[-1]) == 1:
                                        faults_detected_gates.append(fault_within_gate)
                                        
                            elif value == 1:
                                for prerequisite in level_data['node_prerequiste'][node]:
                                    if output_values[prerequisite] == 1:
                                        for fault_within_gate in val:
                                            if fault_within_gate.split('-')[0] == prerequisite and int(fault_within_gate[-1]) == 0 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate)
                                            if fault_within_gate.split('-')[0] == fault and int(fault_within_gate[-1]) == 0 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate) # + ' (collapsed by dominance)')
                                            if fault_within_gate.split('-')[0] != prerequisite and fault_within_gate.split('-')[0] != fault and output_values[fault_within_gate.split('-')[0]] != 1:
                                                if(int(fault_within_gate[-1]) == 1 and fault_within_gate not in faults_detected_gates):
                                                    faults_detected_gates.append(fault_within_gate)

                ###########################################################################################################################################################
                
                elif fault_data['gate_type'][node] == 'NOR':
                    #print(f'{node}: {value} (NOR)')
                    for fault, val in fault_data['fault_list_gates'].items():
                        if fault.strip() == node.strip():
                            if value == 1:
                                for fault_within_gate in val:
                                    if int(fault_within_gate[-1]) == 1 and fault_within_gate.split('-')[0] != fault and fault_within_gate not in faults_detected_gates:
                                        faults_detected_gates.append(fault_within_gate)
                                    
                                    elif fault_within_gate.split('-')[0] == fault and fault_within_gate not in faults_detected_gates:
                                        if ( int(fault_within_gate[-1]) == 0):
                                            faults_detected_gates.append(fault_within_gate) 
                                        
                            elif value == 0:
                                for prerequisite in level_data['node_prerequiste'][node]:
                                    if output_values[prerequisite] == 1:
                                        #print(prerequisite)
                                        for fault_within_gate in val:
                                            if fault_within_gate.split('-')[0] == prerequisite and int(fault_within_gate[-1]) == 0 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate)
                                            if fault_within_gate.split('-')[0] == fault and int(fault_within_gate[-1]) == 1 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate) # + ' (collapsed by dominance)')
                                            if fault_within_gate.split('-')[0] != prerequisite and fault_within_gate.split('-')[0] != fault and output_values[fault_within_gate.split('-')[0]] != 1:
                                                if(int(fault_within_gate[-1]) == 1 and fault_within_gate not in faults_detected_gates):
                                                    faults_detected_gates.append(fault_within_gate)
                                            
                                            
                ###########################################################################################################################################################
                
                elif fault_data['gate_type'][node] == 'XOR':
                    #print(f'{node}: {value} (XOR)')
                    for fault, val in fault_data['fault_list_gates'].items():
                        if fault.strip() == node.strip():
                            
                            if value == 0:
                                for prerequisite in level_data['node_prerequiste'][node]:
                                    if output_values[prerequisite] == 0:
                                        for fault_within_gate in val:
                                            if int(fault_within_gate[-1]) == 1 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate)
                                            '''
                                            if fault_within_gate.split('-')[0] == fault and int(fault_within_gate[-1]) == 0 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate) # + ' (collapsed by dominance)')
                                            '''
                                    if output_values[prerequisite] == 1:
                                        for fault_within_gate in val:
                                            if fault_within_gate.split('-')[0] == prerequisite and int(fault_within_gate[-1]) == 0 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate)
                                            
                                            if fault_within_gate.split('-')[0] == fault and int(fault_within_gate[-1]) == 1 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate) # + ' (collapsed by dominance)')        '''
                                                
                            elif value == 1:
                                for prerequisite in level_data['node_prerequiste'][node]:
                                    if output_values[prerequisite] == 1:
                                        for fault_within_gate in val:    
                                            if fault_within_gate.split('-')[0] == fault and int(fault_within_gate[-1]) == 0 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate) # + ' (collapsed by dominance)')        '''
                                            
                                            if fault_within_gate.split('-')[0] == prerequisite and int(fault_within_gate[-1]) == 0 and fault_within_gate not in faults_detected_gates:
                                                faults_detected_gates.append(fault_within_gate) # + ' (collapsed by dominance)')        '''
                                        
                                            if fault_within_gate.split('-')[0] != prerequisite and fault_within_gate.split('-')[0] != fault and int(fault_within_gate[-1]) == 1 and fault_within_gate not in faults_detected_gates:
                                                    faults_detected_gates.append(fault_within_gate)
                            
                            
                            '''
                            I dont think i can implement fault dominance for the XOR GATE, atleast not to my know because the the each output value for the XOR gate
                            details showing about the input, to be honest im not sure but this is my implementation
                            '''

                ###########################################################################################################################################################
                
                elif fault_data['gate_type'][node] == 'NOT':
                    #print(f'{node}: {value} (NOT)')
                    for fault, val in fault_data['fault_list_gates'].items():
                        if fault.strip() == node.strip():
                            
                            if value == 1:
                                for fault_within_gate in val:
                                    if int(fault_within_gate[-1]) == 1 and fault_within_gate.split('-')[0] != fault and fault_within_gate not in faults_detected_gates:
                                        faults_detected_gates.append(fault_within_gate)
                                    elif fault_within_gate.split('-')[0] == fault and fault_within_gate not in faults_detected_gates:
                                        if ( int(fault_within_gate[-1]) == 0):
                                            faults_detected_gates.append(fault_within_gate) 
                            elif value == 0:
                                for fault_within_gate in val:
                                    if int(fault_within_gate[-1]) == 0 and fault_within_gate.split('-')[0] != fault and fault_within_gate not in faults_detected_gates:
                                        faults_detected_gates.append(fault_within_gate)
                                    elif fault_within_gate.split('-')[0] == fault and fault_within_gate not in faults_detected_gates:
                                        if ( int(fault_within_gate[-1]) == 1):
                                            faults_detected_gates.append(fault_within_gate) 

                ###########################################################################################################################################################
                
                elif fault_data['gate_type'][node] == 'BUFF':
                    #print(f'{node}: {value} (BUFF))')
                    for fault, val in fault_data['fault_list_gates'].items():
                        if fault.strip() == node.strip():
                            
                            if value == 1:
                                for fault_within_gate in val:
                                    if int(fault_within_gate[-1]) == 0 and fault_within_gate.split('-')[0] != fault and fault_within_gate not in faults_detected_gates:
                                        faults_detected_gates.append(fault_within_gate) # + 'yoyoyoyoy')
                                    elif fault_within_gate.split('-')[0] == fault and fault_within_gate not in faults_detected_gates:
                                        if ( int(fault_within_gate[-1]) == 0):
                                            faults_detected_gates.append(fault_within_gate) # + 'yoyoyoyoy') 
                            elif value == 0:
                                for fault_within_gate in val:
                                    if int(fault_within_gate[-1]) == 1 and fault_within_gate.split('-')[0] != fault and fault_within_gate not in faults_detected_gates:
                                        faults_detected_gates.append(fault_within_gate) # + 'yoyoyoyoy')
                                    elif fault_within_gate.split('-')[0] == fault and fault_within_gate not in faults_detected_gates:
                                        if ( int(fault_within_gate[-1]) == 1):
                                            faults_detected_gates.append(fault_within_gate) # + 'yoyoyoyoy') 

                #print('###################')
        
        if(user_input4 == 'A' or user_input4 == 'a'):
            
            print('Output of each node in circuit\n')
            for node, val in output_values.items():
                    print(f'{node}: {val}')
                    
            print('\n')
            #pprint.pprint(faults_detected_gates)
            #pprint.pprint(faults_detected_inputs)
            if user_input5 in faults_detected_gates:
                print(f"Fault {user_input5} DETECTED in gates.")
            elif user_input5 in faults_detected_inputs:
                print(f"Fault {user_input5} DETECTED in inputs.")
            elif user_input5 in faults_detected_outputs:
                print(f"Fault {user_input5} DETECTED in outputs.")
            else:
                print(f"Fault {user_input5} NOT detected.")
                
        elif(user_input4 == 'B' or user_input4 == 'b'):
            faults_detected = faults_detected_gates + faults_detected_inputs + faults_detected_outputs
            
            print('Choices')
            print('A - if you want a list of all faults and see if detected or not')
            print('B  - If you only want to see the fualts detected')
            user_input6 = input('Enter Choice: ')  
            
            if(user_input6 == 'A' or user_input6 == 'a'):    
                print('Fault List of Detected/Not Detected')  
                for fault in fault_data['fault_list_inputs']:
                    if fault in faults_detected:
                        print(f"  {fault}: Detected")
                    else:
                        print(f"  {fault}: Not Detected")
                        
            elif (user_input6 == 'B' or user_input6 == 'b'):
                print("\nFaults Detected in Gates:")
                for fault in faults_detected_gates:
                    print(f"  {fault}")

                print("\nFaults Detected in Inputs:")
                for fault in faults_detected_inputs:
                    print(f"  {fault}")

                print("\nFaults Detected in Outputs:")
                for fault in faults_detected_outputs:
                    print(f"  {fault}")
            
            total_faults = len(fault_data['fault_list_inputs']) + len(fault_data['fault_list_outputs']) + sum(len(v) for v in fault_data['fault_list_gates'].values())
            detected_faults = len(faults_detected_gates) + len(faults_detected_inputs) + len(faults_detected_outputs)
            detection_percentage = (detected_faults / total_faults) * 100
            
            print(f"\nTotal faults: {total_faults}")
            print(f"Detected faults: {detected_faults}")
            print(f"Detection percentage: {detection_percentage}%")
        

