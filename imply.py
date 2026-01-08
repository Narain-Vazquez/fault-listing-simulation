
import levelization
import pprint

'''
user_input = input('Enter file name ')

level_data = levelization.node_levelization(user_input)

print(level_data['circuit_inputs'])

input_circuit_evaluate = {}

for node in level_data['circuit_inputs']:
    kak = input(f'Enter input value for {node}: ')
    input_circuit_evaluate[node] = int(kak)
'''

def evaluate_circuit(inputs, circuit_gates, node_prerequiste):
    node_values = {}

    for node, value in inputs.items():
        node_values[node] = value

    unevaluated_gates = circuit_gates.copy()

    while unevaluated_gates:
        remaining_gates = []

        for gate in unevaluated_gates:
            output_node, gate_expression = gate.split("=", 1)
            output_node = output_node.strip()
            #print(output_node)
            
            gate_type, input_nodes = gate_expression.split("[", 1)
            gate_type = gate_type.strip()
            #print(gate_type)
            
            input_nodes = node_prerequiste[output_node]
            #print(input_nodes)
            
            if all(node in node_values for node in input_nodes):
                
                if gate_type == 'AND':
                    result = 1
                    for node in input_nodes:
                        result &= node_values[node]
                elif gate_type == 'NAND':
                    result = 1
                    for node in input_nodes:
                        result &= node_values[node]
                    result = 1 - result
                elif gate_type == 'OR':
                    result = 0
                    for node in input_nodes:
                        result |= node_values[node]
                elif gate_type == 'NOR':
                    result = 0
                    for node in input_nodes:
                        result |= node_values[node]
                    result = 1 - result
                elif gate_type == 'XOR':
                    result = 0
                    for node in input_nodes:
                        result ^= node_values[node]
                elif gate_type == 'NOT':
                    input_node = input_nodes[0]
                    result = 1 - node_values[input_node]
                elif gate_type == 'BUFF':
                    #print(input_nodes[0])
                    input_node = input_nodes[0]
                    result = node_values[input_node]

                node_values[output_node] = result
            else:
                remaining_gates.append(gate)

        if len(remaining_gates) == len(unevaluated_gates):
            print("Unable to evaluate all gates due to unresolved dependencies.")
            break

        unevaluated_gates = remaining_gates

    return node_values



#output_values = evaluate_circuit(input_circuit_evaluate, level_data['circuit_gates'],level_data['node_prerequiste'])

#print(level_data['circuit_outputs'])

'''
for node, value in output_values.items():
    #print(node)
    if(node in level_data['circuit_outputs']):
        print(f'{node}: {value}')
'''

    #########################################################################################
    