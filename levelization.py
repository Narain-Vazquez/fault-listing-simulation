
def node_levelization(user_input):

  circuit_inputs = []
  circuit_outputs = []
  circuit_gates = []
  node_levels = {}
  node_prerequiste = {}
  node_dependents = {}
  
  #user_input = input("Enter the file name: ")
  
  file = open(user_input, 'r')
  lines = file.readlines()
  
  for formatted_line in lines:
  
    formatted_line = formatted_line.strip()
    if (not (formatted_line.startswith("#"))):
  
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
  
      ####################################################################
  
      if location_input != -1:
  
        node = formatted_line[location_input + 6:-1].strip()
        circuit_inputs.append(node)
  
        node_levels[node] = 0
  
        if node not in node_prerequiste:
  
          node_prerequiste[node] = []
          node_dependents[node] = []
  
    ####################################################################
  
      if location_output != -1:
  
        node = formatted_line[location_output + 7:-1].strip()
        circuit_outputs.append(node)
  
        if node not in node_prerequiste:
          node_prerequiste[node] = []
          node_dependents[node] = []
  
    ####################################################################
  
    # AND GATE FORMATTING
      if location_and != -1 and location_nand == -1:
  
        gate_output = formatted_line[:location_equal].strip()
        gate_output = gate_output.strip('=')
        inputs = formatted_line[location_and + 4:-1].split(',')
        #print(inputs)
  
        inputs_clean = []
        for input_node in inputs:
          cleaned = input_node.strip()
          #print(cleaned)
          inputs_clean.append(cleaned)
  
        circuit_gates.append(
          f'{gate_output} = AND{inputs_clean}'
        )
        #print(f'{gate_output} = AND{inputs_clean}')
        #print('XXXXXXXXXXX')

        
        if gate_output not in node_prerequiste:
          node_prerequiste[gate_output] = []
          node_dependents[gate_output] = []
  
        for node in inputs_clean:
  
          if node not in node_prerequiste[gate_output]:
            node_prerequiste[gate_output].append(node)
  
          if node not in node_prerequiste:
            node_prerequiste[node] = []
            node_dependents[node] = []
  
          if gate_output not in node_dependents[node]:
            node_dependents[node].append(gate_output)
  
      ####################################################################
  
      # NAND GATE FORMATTING
      if location_nand != -1:
  
        gate_output = formatted_line[:location_equal].strip()
        gate_output = gate_output.strip('=')
        inputs = formatted_line[location_nand + 5:-1].split(',')
  
        inputs_clean = []
        for input_node in inputs:
          cleaned = input_node.strip()
          inputs_clean.append(cleaned)
  
        circuit_gates.append(
          f'{gate_output} = NAND{inputs_clean}'
        )
  
        if gate_output not in node_prerequiste:
          node_prerequiste[gate_output] = []
          node_dependents[gate_output] = []
  
        for node in inputs_clean:
  
          if node not in node_prerequiste[gate_output]:
            node_prerequiste[gate_output].append(node)
  
          if node not in node_prerequiste:
            node_prerequiste[node] = []
            node_dependents[node] = []
  
          if gate_output not in node_dependents[node]:
            node_dependents[node].append(gate_output)
  
    ####################################################################
  
    # OR GATE FORMATTING
      if location_or != -1 and location_nor == -1 and location_xor == -1:
  
        gate_output = formatted_line[:location_equal].strip()
        gate_output = gate_output.strip('=')
        inputs = formatted_line[location_or + 3:-1].split(',')
  
        inputs_clean = []
        for input_node in inputs:
          cleaned = input_node.strip()
          inputs_clean.append(cleaned)
  
        circuit_gates.append(
          f'{gate_output} = OR{inputs_clean}'
          )
  
        if gate_output not in node_prerequiste:
          node_prerequiste[gate_output] = []
          node_dependents[gate_output] = []
  
        for node in inputs_clean:
  
          if node not in node_prerequiste[gate_output]:
            node_prerequiste[gate_output].append(node)
  
          if node not in node_prerequiste:
            node_prerequiste[node] = []
            node_dependents[node] = []
  
          if gate_output not in node_dependents[node]:
            node_dependents[node].append(gate_output)
  
      ####################################################################
  
      # NOR GATE FORMATTING
      if location_nor != -1:
  
        gate_output = formatted_line[:location_equal].strip()
        gate_output = gate_output.strip('=')
        inputs = formatted_line[location_nor + 4:-1].split(',')
  
        inputs_clean = []
        for input_node in inputs:
          cleaned = input_node.strip()
          inputs_clean.append(cleaned)
  
        circuit_gates.append(
          f'{gate_output} = NOR{inputs_clean}'
        )
  
        if gate_output not in node_prerequiste:
          node_prerequiste[gate_output] = []
          node_dependents[gate_output] = []
  
        for node in inputs_clean:
  
          if node not in node_prerequiste[gate_output]:
            node_prerequiste[gate_output].append(node)
  
          if node not in node_prerequiste:
            node_prerequiste[node] = []
            node_dependents[node] = []
  
          if gate_output not in node_dependents[node]:
            node_dependents[node].append(gate_output)
  
      ####################################################################
  
      # XOR GATE FORMATTING
      if location_xor != -1:
  
        gate_output = formatted_line[:location_equal].strip()
        gate_output = gate_output.strip('=')
        inputs = formatted_line[location_xor + 4:-1].split(',')
  
        inputs_clean = []
        for input_node in inputs:
          cleaned = input_node.strip()
          inputs_clean.append(cleaned)
  
        circuit_gates.append(
          f'{gate_output} = XOR{inputs_clean}'
        )
  
        if gate_output not in node_prerequiste:
          node_prerequiste[gate_output] = []
          node_dependents[gate_output] = []
  
        for node in inputs_clean:
  
          if node not in node_prerequiste[gate_output]:
            node_prerequiste[gate_output].append(node)
  
          if node not in node_prerequiste:
            node_prerequiste[node] = []
            node_dependents[node] = []
  
          if gate_output not in node_dependents[node]:
            node_dependents[node].append(gate_output)
  
    ####################################################################
  
    # NOT GATE FORMATTING
      if location_not != -1:
  
        gate_output = formatted_line[:location_equal].strip()
        gate_output = gate_output.strip('=')
        #gate_output = gate_output.replace("'", r"\'")
        ##print(gate_output)
        input_node = formatted_line[location_not + 4:-1].strip()
        circuit_gates.append(
          f'{gate_output} = NOT[{input_node}]'
        )
  
        if gate_output not in node_prerequiste:
          node_prerequiste[gate_output] = []
          node_dependents[gate_output] = []
  
        if input_node not in node_prerequiste:
          node_prerequiste[input_node] = []
          node_dependents[input_node] = []
  
        if gate_output not in node_dependents[input_node]:
          node_dependents[input_node].append(gate_output)
  
        node_prerequiste[gate_output].append(input_node)
  
  ####################################################################
  
  # BUFF GATE FORMATTING
      if location_buff != -1:
  
        gate_output = formatted_line[:location_equal].strip()
        gate_output = gate_output.strip('=')
        input_node = formatted_line[location_buff + 5:-1].strip(',')
        circuit_gates.append(
          f'{gate_output} = BUFF[{input_node}]'
        )
  
        if gate_output not in node_prerequiste:
          node_prerequiste[gate_output] = []
          node_dependents[gate_output] = []
  
        if input_node not in node_prerequiste:
          node_prerequiste[input_node] = []
          node_dependents[input_node] = []
  
        if gate_output not in node_dependents[input_node]:
          node_dependents[input_node].append(gate_output)
  
        node_prerequiste[gate_output].append(input_node)
  
  ####################################################################
  
  
  def calcalate_levels():
  
    cycle = True
  
    while cycle:
      cycle = False
      updated_levels = {}
  
      for node, level in node_levels.items():
        if node in node_dependents:
  
          # see which nodes depend on the current node
          for dependent in node_dependents[node]:
            # make their level currently one higher than the input current node
            #new_level = level + 1
            highest_prerequisite_level = 0
  
            # look for the other nodes attached this the current dependent node
            for prerequisite in node_prerequiste[dependent]:
              # if the input nodes have a level store that current level
              if prerequisite in node_levels:
                prerequisite_level = node_levels[prerequisite]
  
            # see if that's the highest level
              if prerequisite_level > highest_prerequisite_level:
                highest_prerequisite_level = prerequisite_level
  
              #print(node_levels.get(dependent, 0))
  
              # complete the cycle and add node to update level dict
              if highest_prerequisite_level + 1 > node_levels.get(dependent, 0):
                updated_levels[dependent] = highest_prerequisite_level + 1
                cycle = True
  
      for node, level in updated_levels.items():
        node_levels[node] = level
  
  
  ####################################################################
  
  calcalate_levels()
  
  '''
  print('Inputs: ', circuit_inputs)
  print('Outputs: ', circuit_outputs)
  
  print('\n')
  print('Gates: (OUTPUT NODE)/*(GATE TYPE)*/(INPUTS NODE(S))')
  for gate in circuit_gates:
    print(gate)
  
  print('\n')
  print('Levels: (node): (level)')
  for node, level in node_levels.items():
    print(f'{node}: level {level}')
  '''
  
  return {
    'circuit_inputs': circuit_inputs,
    'circuit_outputs': circuit_outputs,
    'circuit_gates': circuit_gates,
    'node_levels': node_levels,
    'node_prerequiste': node_prerequiste,
    'node_dependents': node_dependents
  }

