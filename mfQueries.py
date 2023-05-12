# function = """
# count = 0
# predicates = predicates.split(',')
# predlist = []
# #here we are splitting predicates by each predicate statement and creating a list to store the parts of teach predicates in a single 2D array
# for i in predicates:
#     predlist.append(i.split(' '))

# #now we loop through the table to evaluate each grouping variable
# for i in range(int(groupingVarCount)+1):
#     if i == 0:
#         for row in query:
#             key = ''
#             value = {}    #for the 0th pass of the algorithm, it initializes the MF Struct for every unique group based on the grouping variables. The loop iterates over each row as well.
#             for attr in groupingAttributes.split(','):
#                 key += f'{str(row[attr])},'
#             key = key[:-1] #Removing the trailing comma form the ky string
#             if key not in MF_Struct.keys():
#                 for groupAttr in groupingAttributes.split(','): #it initializes the columns of the MF Struct row for the grouping attributes
#                     col_val =row[groupAttr]
#                     if col_val:
#                         value[groupAttr] = col_val
#                 for fVectAttr in fVect.split(','):
#                     if (fVectAttr.split('_')[1] == 'avg'):
#                         #for average, a dictonary of sum, count, and avg is created
#                         value[fVectAttr] = {'sum':0, 'count':0, 'avg': 0}
#                     elif (fVectAttr.split('_')[1] == 'min'):
#                          #we will be initializing min = 1000 as it is the largest value of "quant" in th sales table
#                          value[fVectAttr] = 1000
#                     else:
#                         #all the other aggregates i.e. sum, count and max will be initialised to 0
#                         value[fVectAttr] = 0
#                 MF_Struct[key] = value #adding the initailised row into MF Struct
#     else:
#         #now all other n passes for each of the grouping variable
#         for aggregate in fVect.split(','):
#             aggr_list = aggregate.split('_')
#             groupVar = aggr_list[0] # stores the grouping variable number
#             agg_func = aggr_list[1] # stores the aggregate function name
#             agg_col = aggr_list[2] # stores the column name on which the aggregate function is applied
#             #Checking if the current iteration i matches the grouping variable number (int(groupVar)). This ensures that the calculations are performed only for the appropriate grouping variable.
#             if i == int(groupVar):
#                 for row in query:
#                     # key = ''  
#                     # for attr in groupingAttributes.split(','): #Generating the key string by concatenating the values of the grouping attributes from the current row
#                     #     key+= f'{str(row[attr])},'
#                     # key = key[:-1]
#                     for key in MF_Struct.keys():
#                         if agg_func == 'sum':
#                             #Creating an evaluation string (eval_string) by replacing the variables in the predicates with their corresponding values from the current row
#                             eval_string = predicates[i-1] #Creates an evaluation string (eval_string) by assigning the corresponding predicate from the predicates list to the variable. The index i-1 is used to access the specific predicate for the current grouping variable.
#                             for string in predlist[i-1]:
#                                 if len(string.split('.')) > 1 and string.split('.')[0] == str(i): # checks if the string contains dot indicating that it refers to a specific column in row and
#                                     #if the first part of the string matches the current grouping variable number(i)
#                                     row_val = row[string.split('.')[1]]
#                                     try:
#                                         int(row_val)
#                                         eval_string = eval_string.replace(string, str(row_val))
#                                     except:
#                                         eval_string = eval_string.replace(string, f" '{row_val}'") #if the conversion to an integer in the previous step raises an exception (i.e., row_val is not numeric), it means it's a string value. In this case, the occurrence of string in the evaluation string is replaced with row_val surrounded by single quotes, creating a string representation.
#                                 elif string in groupingAttributes.split(','):
#                                     row_val = MF_Struct[key][string]
#                                     try:
#                                         int(row_val)
#                                         eval_string = eval_string.replace(string, str(row_val))
#                                     except:
#                                          eval_string = eval_string.replace(string, f"'{row_val}'")
#                             #if eval_string is true and count isn't 0, update the sum
#                             if eval(eval_string.replace('=',"==")): 
#                                 sum = int(row[agg_col])
#                                 MF_Struct[key][aggregate] += sum
#                         elif agg_func == 'avg':
#                             sum = MF_Struct[key][aggregate]['sum']
#                             count = MF_Struct[key][aggregate]['count']
#                             eval_string = predicates[i-1]
#                             for string in predlist[i-1]:
#                                 if len(string.split('.')) > 1 and string.split('.')[0] == str(i):
#                                     row_val = row[string.split('.')[1]]
#                                     try:
#                                         int(row_val)
#                                         eval_string = eval_string.replace(string, str(row_val))
#                                     except:
#                                         eval_string = eval_string.replace(string, f"'{row_val}'")
#                                 elif string in groupingAttributes.split(','):
#                                     row_val = MF_Struct[key][string]
#                                     try:
#                                         int(row_val)
#                                         eval_string = eval_string.replace(string, str(row_val))
#                                     except:
#                                          eval_string = eval_string.replace(string, f"'{row_val}'")
#                             # If eval_string is true and count isn't 0, update the avg
#                             if eval(eval_string.replace('=', '==')):
#                                 sum += int(row[agg_col])
#                                 count += 1
#                                 if count != 0:
#                                     MF_Struct[key][aggregate] = {'sum': sum, 'count': count, 'avg': (sum/count)}
#                         elif agg_func == 'min':
#                             eval_string = predicates[i-1] 
#                             for string in predlist[i-1]:
#                                 if len(string.split('.')) > 1 and string.split('.')[0] == str(i): 
#                                     row_val = row[string.split('.')[1]]
#                                     try:
#                                         int(row_val)
#                                         eval_string = eval_string.replace(string, str(row_val))
#                                     except:
#                                         eval_string = eval_string.replace(string, f" '{row_val}'")
#                                 elif string in groupingAttributes.split(','):
#                                     row_val = MF_Struct[key][string]
#                                     try:
#                                         int(row_val)
#                                         eval_string = eval_string.replace(string, str(row_val))
#                                     except:
#                                          eval_string = eval_string.replace(string, f"'{row_val}'")
#                             #if eval_string is true, update the min
#                             if eval(eval_string.replace('=',"==")):  
#                                 min = int(MF_Struct[key][aggregate]) # retreives current minimum stored in MF Struct for given key and aggregate
#                                 if int(row[agg_col])<min: #if the value in the row is less than the min, update the min in MF Struct
#                                     MF_Struct[key][aggregate] = row[agg_col]
#                         elif agg_func == 'max':
#                             eval_string = predicates[i-1] 
#                             for string in predlist[i-1]:
#                                 if len(string.split('.')) > 1 and string.split('.')[0] == str(i): 
#                                     row_val = row[string.split('.')[1]]
#                                     try:
#                                         int(row_val)
#                                         eval_string = eval_string.replace(string, str(row_val))
#                                     except:
#                                         eval_string = eval_string.replace(string, f" '{row_val}'")
#                                 elif string in groupingAttributes.split(','):
#                                     row_val = MF_Struct[key][string]
#                                     try:
#                                         int(row_val)
#                                         eval_string = eval_string.replace(string, str(row_val))
#                                     except:
#                                          eval_string = eval_string.replace(string, f"'{row_val}'")
#                             #if eval_string is true, update the max
#                             if eval(eval_string.replace('=',"==")):
#                                 max = int(MF_Struct[key][aggregate])
#                                 if int(row[agg_col])>max: #if the value in the row is greater than the max, update the max in MF Struct
#                                     MF_Struct[key][aggregate] = row[agg_col]
#                         elif agg_func == 'count':
#                             eval_string = predicates[i-1] 
#                             for string in predlist[i-1]:
#                                 if len(string.split('.')) > 1 and string.split('.')[0] == str(i): 
#                                     row_val = row[string.split('.')[1]]
#                                     try:
#                                         int(row_val)
#                                         eval_string = eval_string.replace(string, str(row_val))
#                                     except:
#                                         eval_string = eval_string.replace(string, f" '{row_val}'")
#                                 elif string in groupingAttributes.split(','):
#                                     row_val = MF_Struct[key][string]
#                                     try:
#                                         int(row_val)
#                                         eval_string = eval_string.replace(string, str(row_val))
#                                     except:
#                                         eval_string = eval_string.replace(string, f"'{row_val}'")
#                             #if eval_string is true, update the count by incrementing it
#                             if eval(eval_string.replace('=',"==")):
#                                 MF_Struct[key][aggregate] +=1
# #checking the HAVING condition and generating output table
# # output = PrettyTable()
# # output.field_names = selectAttributes.split(',')
# # for row in MF_Struct:
# #     eval_string = ''
# #     if havingCondition != '':
# #         for string in havingCondition.split(' '):
# #             if string not in ['>', '<', '==', '<=', '>=', 'and', 'or', 'not', '*', '/', '+', '-']:
# #                 try:
# #                     int(string)
# #                     eval_string += string
# #                 except:
# #                     if len(string.split('_')) > 1 and string.split('_')[1] == 'avg':
# #                             eval_string += str(MF_Struct[row][string]['avg'])
# #                     else:
# #                         eval_string += str(MF_Struct[row][string])
# #             else:
# #                 eval_string += f' {string} '
# #         if eval(eval_string.replace('=', '==')):
# #             row_info = []
# #             for val in selectAttributes.split(','):
# #                 if val in ['1_avg_quant', '2_avg_quant']:
# #                     agg = val.split('_')[0]
# #                     attr = val.split('_')[1]
# #                     if attr == 'avg':
# #                         row_info.append(str(MF_Struct[row][agg][attr]))
# #                     else:
# #                         row_info.append(str(eval(f"MF_Struct[row]['{agg}']['{attr}']")))
# #                 elif '/' in val:
# #                     num1, num2 = val.split('/')
# #                     num1_agg, num1_attr = num1.split('_')
# #                     num2_agg, num2_attr = num2.split('_')
# #                     result = eval(f"MF_Struct[row]['{num1_agg}']['{num1_attr}'] / MF_Struct[row]['{num2_agg}']['{num2_attr}']")
# #                     row_info.append(str(result))
# #                 elif '*' in val:
# #                     num1, num2 = val.split('*')
# #                     num1_agg, num1_attr = num1.split('_')
# #                     num2_agg, num2_attr = num2.split('_')
# #                     result = eval(f"MF_Struct[row]['{num1_agg}']['{num1_attr}'] * MF_Struct[row]['{num2_agg}']['{num2_attr}']")
# #                     row_info.append(str(result))
# #                 elif '-' in val:
# #                     num1, num2 = val.split('-')
# #                     num1_agg, num1_attr = num1.split('_')
# #                     num2_agg, num2_attr = num2.split('_')
# #                     result = eval(f"MF_Struct[row]['{num1_agg}']['{num1_attr}'] - MF_Struct[row]['{num2_agg}']['{num2_attr}']")
# #                     row_info.append(str(result))
# #                 elif '+' in val:
# #                     num1, num2 = val.split('+')
# #                     num1_agg, num1_attr = num1.split('_')
# #                     num2_agg, num2_attr = num2.split('_')
# #                     result = eval(f"MF_Struct[row]['{num1_agg}']['{num1_attr}'] + MF_Struct[row]['{num2_agg}']['{num2_attr}']")
# #                     row_info.append(str(result))
# #                 else:
# #                     row_info.append(str(MF_Struct[row][val]))
# #             output.add_row(row_info)
# #     else:
# #         row_info = []
# #         for val in selectAttributes.split(','):
# #             if val in ['1_avg_quant', '2_avg_quant']:
# #                 agg = val.split('_')[0]
# #                 attr = val.split('_')[1]
# #                 if attr == 'avg':
# #                     row_info.append(str(MF_Struct[row][agg][attr]))
# #                 else:
# #                     row_info.append(str(eval(f"MF_Struct[row]['{agg}']['{attr}']")))
# #             elif '/' in val:
# #                 num1, num2 = val.split('/')
# #                 num1_agg, num1_attr = num1.split('_')
# #                 num2_agg, num2_attr = num2.split('_')
# #                 result = eval(f"MF_Struct[row]['{num1_agg}']['{num1_attr}'] / MF_Struct[row]['{num2_agg}']['{num2_attr}']")
# #                 row_info.append(str(result))
# #             elif '*' in val:
# #                 num1, num2 = val.split('*')
# #                 num1_agg, num1_attr = num1.split('_')
# #                 num2_agg, num2_attr = num2.split('_')
# #                 result = eval(f"MF_Struct[row]['{num1_agg}']['{num1_attr}'] * MF_Struct[row]['{num2_agg}']['{num2_attr}']")
# #                 row_info.append(str(result))
# #             elif '-' in val:
# #                 num1, num2 = val.split('-')
# #                 num1_agg, num1_attr = num1.split('_')
# #                 num2_agg, num2_attr = num2.split('_')
# #                 result = eval(f"MF_Struct[row]['{num1_agg}']['{num1_attr}'] - MF_Struct[row]['{num2_agg}']['{num2_attr}']")
# #                 row_info.append(str(result))
# #             elif '+' in val:
# #                 num1, num2 = val.split('+')
# #                 num1_agg, num1_attr = num1.split('_')
# #                 num2_agg, num2_attr = num2.split('_')
# #                 result = eval(f"MF_Struct[row]['{num1_agg}']['{num1_attr}'] + MF_Struct[row]['{num2_agg}']['{num2_attr}']")
# #                 row_info.append(str(result))
# #             else:
# #                 row_info.append(str(MF_Struct[row][val]))
# #         output.add_row(row_info)
# # print(output) #Pretty table corresponding to evaluation of query
# output = PrettyTable()
# output.field_names = selectAttributes.split(',')
# for row in MF_Struct:
#     eval_string = ''
#     if havingCondition != '':
#         for string in havingCondition.split(' '):
#             if string not in ['>', '<', '==', '<=', '>=', 'and', 'or', 'not', '*', '/', '+', '-']:
#                 try:
#                     float(string)
#                     eval_string += string
#                 except:
#                     if len(string.split('_')) > 1 and string.split('_')[1] == 'avg':
#                         eval_string += str(MF_Struct[row][string]['avg'])
#                     else:
#                         eval_string += str(MF_Struct[row][string])
#             else:
#                 eval_string += f' {string} '
#         if eval(eval_string.replace('=', '==')):
#             row_info = []
#             for val in selectAttributes.split(','):
#                 if len(val.split('_')) > 1 and val.split('_')[1] == 'avg':
#                     row_info += [str(MF_Struct[row][val]['avg'])]
#                 else:
#                     row_info += [str(MF_Struct[row][val])]
#                 output.add_row(row_info)
#         eval_string = ''
#     else:
#         #there is no having condition, thus every MFStruct row will be added to the output table
#         row_info = []
#         for val in selectAttributes.split(','):
#             if len(val.split('_')) > 1 and val.split('_')[1] == 'avg':
#                 row_info += [str(MF_Struct[row][val]['avg'])]
#             else:
#                 row_info += [str(MF_Struct[row][val])]
#             output.add_row(row_info)
# print(output)
# """
function = """predicates = predicates.split(',') #splits predicates by each predicate statment and creates list to store the parts of each predicate in a single 2D array
pList = []
for i in predicates:
	pList.append(i.split(' '))
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
					colVal = row[groupAttr]
					if colVal:
						value[groupAttr] = colVal
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
			aggList = aggregate.split('_')
			groupVar = aggList[0]
			aggFunc = aggList[1]
			aggCol = aggList[2]
            # Check to make sure the aggregate function is being called on the grouping variable you are currently on (i)
            # Also loop through every key in the MF_Struct to update every row of the MF_Struct the predicate statments apply to(1.state = state and 1.cust = cust vs 1.state = state)
			if i == int(groupVar):
				for row in query:
					for key in MF_Struct.keys():
						if aggFunc == 'sum':
							evalString = predicates[i-1]
                            # Creates a string to be run with the eval() method by replacing grouping variables with their actual values
                            # Since it's an EMF query, it must also check if the string is a grouping variable and replace that with the actual value from the table row as well
							for string in pList[i-1]:
								if len(string.split('.')) > 1 and string.split('.')[0] == str(i):
									rowVal = row[string.split('.')[1]]
									try:
										int(rowVal)
										evalString = evalString.replace(string, str(rowVal))
									except:
										evalString = evalString.replace(string, f"'{rowVal}'")
								elif string in groupingAttributes.split(','):
									rowVal = MF_Struct[key][string]
									try:
										int(rowVal)
										evalString = evalString.replace(string, str(rowVal))
									except:
										evalString = evalString.replace(string, f"'{rowVal}'")
                            # If evalString is true, update the sum
							if eval(evalString.replace('=', '==')):
								sum = int(row[aggCol])
								MF_Struct[key][aggregate] += sum
						elif aggFunc == 'avg':
							sum = MF_Struct[key][aggregate]['sum']
							count = MF_Struct[key][aggregate]['count']
							evalString = predicates[i-1]
							for string in pList[i-1]:
								if len(string.split('.')) > 1 and string.split('.')[0] == str(i):
									rowVal = row[string.split('.')[1]]
									try:
										int(rowVal)
										evalString = evalString.replace(string, str(rowVal))
									except:
										evalString = evalString.replace(string, f"'{rowVal}'")
								elif string in groupingAttributes.split(','):
									rowVal = MF_Struct[key][string]
									try:
										int(rowVal)
										evalString = evalString.replace(string, str(rowVal))
									except:
										evalString = evalString.replace(string, f"'{rowVal}'")
                            # If evalString is true and count isn't 0, update the avg
							if eval(evalString.replace('=', '==')):
								sum += int(row[aggCol])
								count += 1
								if count != 0:
									MF_Struct[key][aggregate] = {'sum': sum, 'count': count, 'avg': (sum/count)}
						elif aggFunc == 'min':
							evalString = predicates[i-1]
							for string in pList[i-1]:
								if len(string.split('.')) > 1 and string.split('.')[0] == str(i):
									rowVal = row[string.split('.')[1]]
									try:
										int(rowVal)
										evalString = evalString.replace(string, str(rowVal))
									except:
										evalString = evalString.replace(string, f"'{rowVal}'")
								elif string in groupingAttributes.split(','):
									rowVal = MF_Struct[key][string]
									try:
										int(rowVal)
										evalString = evalString.replace(string, str(rowVal))
									except:
										evalString = evalString.replace(string, f"'{rowVal}'")
                            # If evalString is true, update the min
							if eval(evalString.replace('=', '==')):
								min = int(MF_Struct[key][aggregate])
								if int(row[aggCol]) < min:
									MF_Struct[key][aggregate] = row[aggCol]
						elif aggFunc == 'max':
							evalString = predicates[i-1]
							for string in pList[i-1]:
								if len(string.split('.')) > 1 and string.split('.')[0] == str(i):
									rowVal = row[string.split('.')[1]]
									try:
										int(rowVal)
										valString = evalString.replace(string, str(rowVal))
									except:
										evalString = evalString.replace(string, f"'{rowVal}'")
								elif string in groupingAttributes.split(','):
									rowVal = MF_Struct[key][string]
									try:
										int(rowVal)
										valString = evalString.replace(string, str(rowVal))
									except:
										evalString = evalString.replace(string, f"'{rowVal}'")
                            # If evalString is true, update the max
							if eval(evalString.replace('=', '==')):
								max = int(MF_Struct[key][aggregate])
								if int(row[aggCol]) > max:
									MF_Struct[key][aggregate] = row[aggCol]
						elif aggFunc == 'count':
							evalString = predicates[i-1]
							for string in pList[i-1]:
								if len(string.split('.')) > 1 and string.split('.')[0] == str(i):
									rowVal = row[string.split('.')[1]]
									try:
										int(rowVal)
										evalString = evalString.replace(string, str(rowVal))
									except:
										evalString = evalString.replace(string, f"'{rowVal}'")
								elif string in groupingAttributes.split(','):
									rowVal = MF_Struct[key][string]
									try:
										int(rowVal)
										evalString = evalString.replace(string, str(rowVal))
									except:
										evalString = evalString.replace(string, f"'{rowVal}'")
                            # If evalString is true, increment the count
							if eval(evalString.replace('=', '==')):
								MF_Struct[key][aggregate] += 1
#Generate output table(also checks the HAVING condition)
# output = PrettyTable()
# output.field_names = selectAttributes.split(',')
# for row in MF_Struct:
#     #create an evalString to be used to check each having condition
# 	evalString = ''
# 	if havingCondition != '':
# 		for string in havingCondition.split(' '):
#             #if there is a having condition, loop through each element of the having condition to fill in the correct information into the evalString
#             #the eval string will be equal to the having condition, replaced with the values of the variables in question, 
#             #then evaluated to check if the row of the MFStruct being examined is to be included in the output table
# 			if string not in ['>', '<', '==', '<=', '>=', 'and', 'or', 'not', '*', '/', '+', '-']:
# 				try:
# 					float(string)
# 					evalString += string
# 				except:
# 					if len(string.split('_')) > 1 and string.split('_')[1] == 'avg':
# 						evalString += str(MF_Struct[row][string]['avg'])
# 					else:
# 						evalString += str(MF_Struct[row][string])
# 			else:
# 				evalString += f' {string} '
# 		if eval(evalString.replace('=', '==')):
# 			row_info = []
# 			for val in selectAttributes.split(','):
# 				if len(val.split('_')) > 1 and val.split('_')[1] == 'avg':
# 					row_info += [str(MF_Struct[row][val]['avg'])]
# 				else:
# 					row_info += [str(MF_Struct[row][val])]
# 			output.add_row(row_info)
# 		evalString = ''
# 	else:
#         #there is no having condition, thus every MFStruct row will be added to the output table
# 		row_info = []
# 		for val in selectAttributes.split(','):
# 			if len(val.split('_')) > 1 and val.split('_')[1] == 'avg':
# 				row_info += [str(MF_Struct[row][val]['avg'])]
# 			else:
# 				row_info += [str(MF_Struct[row][val])]
# 		output.add_row(row_info)
# print(output)
output = PrettyTable()
output.field_names = selectAttributes.split(',')
for row in MF_Struct:
    #create an evalString to be used to check each having condition
	evalString = ''
	if havingCondition != '':
		for string in havingCondition.split(' '):
            #if there is a having condition, loop through each element of the having condition to fill in the correct information into the evalString
            #the eval string will be equal to the having condition, replaced with the values of the variables in question, 
            #then evaluated to check if the row of the MFStruct being examined is to be included in the output table
			if string not in ['>', '<', '==', '<=', '>=', 'and', 'or', 'not', '*', '/', '+', '-']:
				try:
					float(string)
					evalString += string
				except:
					if len(string.split('_')) > 1 and string.split('_')[1] == 'avg':
						evalString += str(MF_Struct[row][string]['avg'])
					else:
						evalString += str(MF_Struct[row][string])
			else:
				evalString += f' {string} '
		if eval(evalString.replace('=', '==')):
			row_info = []
			for val in selectAttributes.split(','):
				if len(val.split('_')) > 1 and val.split('_')[1] == 'sum':
					if '/' in val:
						num1, num2 = val.split('/')
						result = eval(f"MF_Struct[row][num1]/ MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '+' in val:
						num1, num2 = val.split('+')
						result = eval(f"MF_Struct[row][num1]+ MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '-' in val:
						num1, num2 = val.split('-')
						result = eval(f"MF_Struct[row][num1]- MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '*' in val:
						num1, num2 = val.split('*')
						result = eval(f"MF_Struct[row][num1]* MF_Struct[row][num2]")
						row_info.append(str(result))
					else:
						row_info += [str(MF_Struct[row][val])]
				elif len(val.split('_')) > 1 and val.split('_')[1] == 'avg':
					if '/' in val:
						num1, num2 = val.split('/')
						result = eval(f"MF_Struct[row][num1]/ MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '+' in val:
						num1, num2 = val.split('+')
						result = eval(f"MF_Struct[row][num1]+ MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '-' in val:
						num1, num2 = val.split('-')
						result = eval(f"MF_Struct[row][num1]- MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '*' in val:
						num1, num2 = val.split('*')
						result = eval(f"MF_Struct[row][num1]* MF_Struct[row][num2]")
						row_info.append(str(result))
					else:
						row_info += [str(MF_Struct[row][val])]
				elif len(val.split('_')) > 1 and val.split('_')[1] == 'min':
					if '/' in val:
						num1, num2 = val.split('/')
						result = eval(f"MF_Struct[row][num1]/ MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '+' in val:
						num1, num2 = val.split('+')
						result = eval(f"MF_Struct[row][num1]+ MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '-' in val:
						num1, num2 = val.split('-')
						result = eval(f"MF_Struct[row][num1]- MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '*' in val:
						num1, num2 = val.split('*')
						result = eval(f"MF_Struct[row][num1]* MF_Struct[row][num2]")
						row_info.append(str(result))
					else:
						row_info += [str(MF_Struct[row][val])]
				elif len(val.split('_')) > 1 and val.split('_')[1] == 'max':
					if '/' in val:
						num1, num2 = val.split('/')
						result = eval(f"MF_Struct[row][num1]/ MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '+' in val:
						num1, num2 = val.split('+')
						result = eval(f"MF_Struct[row][num1]+ MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '-' in val:
						num1, num2 = val.split('-')
						result = eval(f"MF_Struct[row][num1]- MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '*' in val:
						num1, num2 = val.split('*')
						result = eval(f"MF_Struct[row][num1]* MF_Struct[row][num2]")
						row_info.append(str(result))
					else:
						row_info += [str(MF_Struct[row][val])]
				elif len(val.split('_')) > 1 and val.split('_')[1] == 'count':
					if '/' in val:
						num1, num2 = val.split('/')
						result = eval(f"MF_Struct[row][num1]/ MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '+' in val:
						num1, num2 = val.split('+')
						result = eval(f"MF_Struct[row][num1]+ MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '-' in val:
						num1, num2 = val.split('-')
						result = eval(f"MF_Struct[row][num1]- MF_Struct[row][num2]")
						row_info.append(str(result))
					elif '*' in val:
						num1, num2 = val.split('*')
						result = eval(f"MF_Struct[row][num1]* MF_Struct[row][num2]")
						row_info.append(str(result))
					else:
						row_info += [str(MF_Struct[row][val])]
				else:
					row_info += [str(MF_Struct[row][val])]
		output.add_row(row_info)
		evalString = ''
	else:
        #there is no having condition, thus every MFStruct row will be added to the output table
		row_info = []
		for val in selectAttributes.split(','):
			if len(val.split('_')) > 1 and val.split('_')[1] == 'sum':
				if '/' in val:
					num1, num2 = val.split('/')
					result = eval(f"MF_Struct[row][num1]/ MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '+' in val:
					num1, num2 = val.split('+')
					result = eval(f"MF_Struct[row][num1]+ MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '-' in val:
					num1, num2 = val.split('-')
					result = eval(f"MF_Struct[row][num1]- MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '*' in val:
					num1, num2 = val.split('*')
					result = eval(f"MF_Struct[row][num1]* MF_Struct[row][num2]")
					row_info.append(str(result))
				else:
					row_info += [str(MF_Struct[row][val])]
			elif len(val.split('_')) > 1 and val.split('_')[1] == 'avg':
				if '/' in val:
					num1, num2 = val.split('/')
					result = eval(f"MF_Struct[row][num1]/ MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '+' in val:
					num1, num2 = val.split('+')
					result = eval(f"MF_Struct[row][num1]+ MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '-' in val:
					num1, num2 = val.split('-')
					result = eval(f"MF_Struct[row][num1]- MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '*' in val:
					num1, num2 = val.split('*')
					result = eval(f"MF_Struct[row][num1]* MF_Struct[row][num2]")
					row_info.append(str(result))
				else:
					row_info += [str(MF_Struct[row][val])]
			elif len(val.split('_')) > 1 and val.split('_')[1] == 'min':
				if '/' in val:
					num1, num2 = val.split('/')
					result = eval(f"MF_Struct[row][num1]/ MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '+' in val:
					num1, num2 = val.split('+')
					result = eval(f"MF_Struct[row][num1]+ MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '-' in val:
					num1, num2 = val.split('-')
					result = eval(f"MF_Struct[row][num1]- MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '*' in val:
					num1, num2 = val.split('*')
					result = eval(f"MF_Struct[row][num1]* MF_Struct[row][num2]")
					row_info.append(str(result))
				else:
					row_info += [str(MF_Struct[row][val])]
			elif len(val.split('_')) > 1 and val.split('_')[1] == 'max':
				if '/' in val:
					num1, num2 = val.split('/')
					result = eval(f"MF_Struct[row][num1]/ MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '+' in val:
					num1, num2 = val.split('+')
					result = eval(f"MF_Struct[row][num1]+ MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '-' in val:
					num1, num2 = val.split('-')
					result = eval(f"MF_Struct[row][num1]- MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '*' in val:
					num1, num2 = val.split('*')
					result = eval(f"MF_Struct[row][num1]* MF_Struct[row][num2]")
					row_info.append(str(result))
				else:
					row_info += [str(MF_Struct[row][val])]
			elif len(val.split('_')) > 1 and val.split('_')[1] == 'count':
				if '/' in val:
					num1, num2 = val.split('/')
					result = eval(f"MF_Struct[row][num1]/ MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '+' in val:
					num1, num2 = val.split('+')
					result = eval(f"MF_Struct[row][num1]+ MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '-' in val:
					num1, num2 = val.split('-')
					result = eval(f"MF_Struct[row][num1]- MF_Struct[row][num2]")
					row_info.append(str(result))
				elif '*' in val:
					num1, num2 = val.split('*')
					result = eval(f"MF_Struct[row][num1]* MF_Struct[row][num2]")
					row_info.append(str(result))
				else:
					row_info += [str(MF_Struct[row][val])]
			else:
				row_info += [str(MF_Struct[row][val])]
		output.add_row(row_info)
print(output)

"""



def mf_Query():
    with open('output.py','a') as outputfile:
        outputfile.write(function)
        outputfile.close()


                        








