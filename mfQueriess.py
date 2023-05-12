function = """predicates = predicates.split(',') #splits predicates by each predicate statment and creates list to store the parts of each predicate in a single 2D array
pred_list = []
for i in predicates:
	pred_list.append(i.split(' '))
for i in range(int(groupingVarCount)+1):
    # 0th pass of the algorithm, where each row of the MF Struct is initalized for every unique group based on the grouping variables.
    # Each row in the MF struct also has its columns initalized appropriately based on the aggregates in the F-Vect
	if i == 0:
		for row in query:
			key = ''
			value = {}
			for attr in groupingAttributes.split(','):
				key += f'{str(row[attr])},'
			key = key[:-1]
			if key not in MF_Struct.keys():
				for groupAttr in groupingAttributes.split(','):
					col_val = row[groupAttr]
					if col_val:
						value[groupAttr] = col_val
				for fVectAttr in fVect.split(','):
                    # Average is saved as an object with the sum, count, and overall average
					if (fVectAttr.split('_')[1] == 'avg'):
						value[fVectAttr] = {'sum':0, 'count':0, 'avg':0}
                    # Min is initialized as 4994, which is the largest value of 'quant' in the sales table. This allows the first value that the algorithm comes across will be saved as the min (except the row with quant=4994)
					elif (fVectAttr.split('_')[1] == 'min'):
						value[fVectAttr] = 4994
					else:
						value[fVectAttr] = 0
				MF_Struct[key] = value
	else:
        # Begin n passes for each of the n grouping variables
		for aggregate in fVect.split(','):
			agg_list = aggregate.split('_')
			groupVar = agg_list[0]
			agg_func = agg_list[1]
			agg_col = agg_list[2]
            # Check to make sure the aggregate function is being called on the grouping variable you are currently on (i)
            # Also loop through every key in the MF_Struct to update every row of the MF_Struct the predicate statments apply to(1.state = state and 1.cust = cust vs 1.state = state)
			if i == int(groupVar):
				for row in query:
					for key in MF_Struct.keys():
						if agg_func == 'sum':
							eval_string = predicates[i-1]
                            # Creates a string to be run with the eval() method by replacing grouping variables with their actual values
                            # Since it's an EMF query, it must also check if the string is a grouping variable and replace that with the actual value from the table row as well
							for string in pred_list[i-1]:
								if len(string.split('.')) > 1 and string.split('.')[0] == str(i):
									row_val = row[string.split('.')[1]]
									try:
										int(row_val)
										eval_string = eval_string.replace(string, str(row_val))
									except:
										eval_string = eval_string.replace(string, f"'{row_val}'")
								elif string in groupingAttributes.split(','):
									row_val = MF_Struct[key][string]
									try:
										int(row_val)
										eval_string = eval_string.replace(string, str(row_val))
									except:
										eval_string = eval_string.replace(string, f"'{row_val}'")
                            # If eval_string is true, update the sum
							if eval(eval_string.replace('=', '==')):
								sum = int(row[agg_col])
								MF_Struct[key][aggregate] += sum
						elif agg_func == 'avg':
							sum = MF_Struct[key][aggregate]['sum']
							count = MF_Struct[key][aggregate]['count']
							eval_string = predicates[i-1]
							for string in pred_list[i-1]:
								if len(string.split('.')) > 1 and string.split('.')[0] == str(i):
									row_val = row[string.split('.')[1]]
									try:
										int(row_val)
										eval_string = eval_string.replace(string, str(row_val))
									except:
										eval_string = eval_string.replace(string, f"'{row_val}'")
								elif string in groupingAttributes.split(','):
									row_val = MF_Struct[key][string]
									try:
										int(row_val)
										eval_string = eval_string.replace(string, str(row_val))
									except:
										eval_string = eval_string.replace(string, f"'{row_val}'")
                            # If eval_string is true and count isn't 0, update the avg
							if eval(eval_string.replace('=', '==')):
								sum += int(row[agg_col])
								count += 1
								if count != 0:
									MF_Struct[key][aggregate] = {'sum': sum, 'count': count, 'avg': (sum/count)}
						elif agg_func == 'min':
							eval_string = predicates[i-1]
							for string in pred_list[i-1]:
								if len(string.split('.')) > 1 and string.split('.')[0] == str(i):
									row_val = row[string.split('.')[1]]
									try:
										int(row_val)
										eval_string = eval_string.replace(string, str(row_val))
									except:
										eval_string = eval_string.replace(string, f"'{row_val}'")
								elif string in groupingAttributes.split(','):
									row_val = MF_Struct[key][string]
									try:
										int(row_val)
										eval_string = eval_string.replace(string, str(row_val))
									except:
										eval_string = eval_string.replace(string, f"'{row_val}'")
                            # If eval_string is true, update the min
							if eval(eval_string.replace('=', '==')):
								min = int(MF_Struct[key][aggregate])
								if int(row[agg_col]) < min:
									MF_Struct[key][aggregate] = row[agg_col]
						elif agg_func == 'max':
							eval_string = predicates[i-1]
							for string in pred_list[i-1]:
								if len(string.split('.')) > 1 and string.split('.')[0] == str(i):
									row_val = row[string.split('.')[1]]
									try:
										int(row_val)
										valString = eval_string.replace(string, str(row_val))
									except:
										eval_string = eval_string.replace(string, f"'{row_val}'")
								elif string in groupingAttributes.split(','):
									row_val = MF_Struct[key][string]
									try:
										int(row_val)
										valString = eval_string.replace(string, str(row_val))
									except:
										eval_string = eval_string.replace(string, f"'{row_val}'")
                            # If eval_string is true, update the max
							if eval(eval_string.replace('=', '==')):
								max = int(MF_Struct[key][aggregate])
								if int(row[agg_col]) > max:
									MF_Struct[key][aggregate] = row[agg_col]
						elif agg_func == 'count':
							eval_string = predicates[i-1]
							for string in pred_list[i-1]:
								if len(string.split('.')) > 1 and string.split('.')[0] == str(i):
									row_val = row[string.split('.')[1]]
									try:
										int(row_val)
										eval_string = eval_string.replace(string, str(row_val))
									except:
										eval_string = eval_string.replace(string, f"'{row_val}'")
								elif string in groupingAttributes.split(','):
									row_val = MF_Struct[key][string]
									try:
										int(row_val)
										eval_string = eval_string.replace(string, str(row_val))
									except:
										eval_string = eval_string.replace(string, f"'{row_val}'")
                            # If eval_string is true, increment the count
							if eval(eval_string.replace('=', '==')):
								MF_Struct[key][aggregate] += 1
#Generate output table(also checks the HAVING condition)
output = PrettyTable()
output.field_names = selectAttributes.split(',')
for row in MF_Struct:
    #create an eval_string to be used to check each having condition
	eval_string = ''
	if havingCondition != '':
		for string in havingCondition.split(' '):
            #if there is a having condition, loop through each element of the having condition to fill in the correct information into the eval_string
            #the eval string will be equal to the having condition, replaced with the values of the variables in question, 
            #then evaluated to check if the row of the MFStruct being examined is to be included in the output table
			if string not in ['>', '<', '==', '<=', '>=', 'and', 'or', 'not', '*', '/', '+', '-']:
				try:
					float(string)
					eval_string += string
				except:
					if len(string.split('_')) > 1 and string.split('_')[1] == 'avg':
					    eval_string += str(MF_Struct[row][string]['avg'])
					else:
						eval_string += str(MF_Struct[row][string])
			else:
                eval_string += f'{string}'
        
        if eval(eval_string.replace('=', '==')):
            row_info = []
			for val in selectAttributes.split(','):
				if len(val.split('_')) > 1 and val.split('_')[1] == 'avg':
					row_info += [str(MF_Struct[row][val]['avg'])]
				else:
					row_info += [str(MF_Struct[row][val])]
			output.add_row(row_info)
		eval_string = ''
	
    else:
        #there is no having condition, thus every MFStruct row will be added to the output table
		row_info = []
		for val in selectAttributes.split(','):
			if len(val.split('_')) > 1 and val.split('_')[1] == 'avg':
				row_info += [str(MF_Struct[row][val]['avg'])]
			else:
				row_info += [str(MF_Struct[row][val])]
		output.add_row(row_info)
        
print(output)"""
def mfQuery():
    with open('output.py', 'a') as outputfile:
        outputfile.write(function)
        outputfile.close()