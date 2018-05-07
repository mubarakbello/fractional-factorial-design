import copy, csv, datetime, math, random, sys
from fractions import Fraction
from itertools import combinations as cb
try:
	import numpy as np
except (ModuleNotFoundError, ImportError):
	print("\nRequired program files incomplete.")
	print("Read the User's guide for more information or contact the developer for help.")
	d = input(" ")
import matrices as mt

class FactorialDesign():
	"""	docstring for FactorialFinder"""
	def __init__(self, factors, generators, prompt_msg, whole_plot=None, sub_plot=0):
		self.factors = factors
		self.generators = generators
		self.whole_plot = factors if whole_plot == None else whole_plot
		self.sub_plot = sub_plot
		self.tableObject = []
		self.matrixObject = []
		self.whole_plot_combinations = []
		self.sub_plot_combinations = []
		self.whole_plot_combinations_options = []
		self.sub_plot_combinations_options = []
		self.various_combinations = []
		self.is_exhhausted = False
		self.used = []
		self.random_sets = []
		self.design_name = prompt_msg + "_{date:%d-%m-%Y_%H-%M-%S}.txt".format(date=datetime.datetime.now())
		with open("Outputs/"+self.design_name, "w") as f:
			f.write("FACTORIAL DESIGN PROGRAM OUTPUT\n\n")
			f.write("Number of Factors: {}\n".format(self.factors))
			f.write("Number of Generators: {}\n".format(self.generators))
			f.write("Number of Whole Plots: {}\n".format(self.whole_plot))
			f.write("Number of Sub Plots: {}\n".format(self.sub_plot))
			f.write("\n")
		print("New Sampling object created.\n")
		self.__initialize()

	def __initialize(self):
		# to be called once by __init__ and when values change
		self.whole_plot_list = "A B C D E F G H I J K L M N O".split(" ")
		self.sub_plot_list = "p q r s t u v w x y z".split(" ")
		self.whole_plot_letters = self.whole_plot_list[0:self.whole_plot]
		self.sub_plot_letters = self.sub_plot_list[0:self.sub_plot] if self.sub_plot != 0 else []
		#######################################################################
		# to handle changing generators
		if not 'generators_letters' in dir(self) and self.generators!=0:
			if self.sub_plot != 0:
				if self.generators < self.sub_plot:
					self.generators_letters = self.sub_plot_letters[-self.generators:]
				else:
					num = self.generators - self.sub_plot + 1
					self.generators_letters = self.whole_plot_letters[-num:]
					self.generators_letters.extend(self.sub_plot_letters[1:])
			else: self.generators_letters = self.whole_plot_letters[-self.generators:]
		elif self.generators==0:
			self.generators_letters = []
		self.factors_letters = self.whole_plot_letters[:]
		self.factors_letters.extend([i.lower() for i in self.sub_plot_letters[:]])
		self.factors_letters.sort()
		self.non_generators_letters = list(set(self.factors_letters)-set(self.generators_letters))
		self.non_generators_letters.sort()
		self.whole_plot_combinables = list(set(self.whole_plot_letters)-set(self.generators_letters))
		self.whole_plot_combinables.sort()
		self.sub_plot_combinables = self.non_generators_letters[:]
		print(
			"Factors(k) = {}".format(self.factors),
			"Generators(p) = {}".format(self.generators),
			"Whole Plot = {}".format(self.whole_plot),
			"Sub plots = {}".format(self.sub_plot),
			sep=' -- '
		)
		print("\nGenerators assigned as: [", *self.generators_letters, "]", sep=' ')
		self.generate()

	def generate(self):
		"""Method to generate table from values of __init__"""
		self.factor_diff = self.factors - self.generators
		self.number_of_runs = 2**self.factor_diff
		if len(self.tableObject) != 0:
			self.tableObject.clear()
			self.matrixObject.clear()
		for i in range(self.number_of_runs):
			signs = []
			rems = []
			bloated_signs = []
			bloated_rems = []
			for n in range(self.factors):
				bloated_signs.append(" ")
				bloated_rems.append(" ")
			while i > 0:
				if i%2 == 0:
					signs.append("-")
					rems.append(-1)
				else:
					signs.append("+")
					rems.append(+1)
				i = i // 2
			if len(signs) != self.factor_diff:
				[signs.append("-") for i in range(self.factor_diff - len(signs))]
				[rems.append(-1) for i in range(self.factor_diff - len(rems))]
			for i in range(len(signs)):
				ind = self.factors_letters.index(self.non_generators_letters[i])
				bloated_signs.insert(ind, signs[i])
				bloated_rems.insert(ind, rems[i])
				a = bloated_signs.pop(ind+1)
				b = bloated_rems.pop(ind+1)
			bloated_rems.insert(0, 1)
			self.tableObject.append(bloated_signs)
			self.matrixObject.append(bloated_rems)
		self.getZed()

	def visualizeDefaultTable(self):
		print("", *self.factors_letters, sep='\t')
		print("")
		for row, i in zip(self.tableObject, range(len(self.tableObject))):
			print(i+1, *row, sep='\t')

	def visualizeTable(self, factors, table):
		print("", *factors, sep='\t')
		print("")
		for row in table:
			print(*row, sep='\t')

	def visualizeMatrix(self, matrix):
		print("")
		for row in matrix:
			print("", *row, sep='\t')

	def generateCombinations(self):
		self.whole_plot_combinations_options.clear()
		self.whole_plot_combinations.clear()
		self.sub_plot_combinations.clear()
		self.sub_plot_combinations_options.clear()
		if len(self.whole_plot_letters) - len(self.whole_plot_combinables) == 1:
			self.whole_plot_combinations.append(list(self.whole_plot_combinables))
		else:
			self.whole_plot_combinations.extend(list(cb(self.whole_plot_combinables, len(self.whole_plot_combinables))))
			self.whole_plot_combinations.extend(list(cb(self.whole_plot_combinables, len(self.whole_plot_combinables)-1)))
			if len(self.whole_plot_combinables) > 3:
				self.whole_plot_combinations.extend(list(cb(self.whole_plot_combinables, len(self.whole_plot_combinables)-2)))
		self.sub_plot_combinations.extend(list(cb(self.sub_plot_combinables, len(self.sub_plot_combinables))))
		self.sub_plot_combinations.extend(list(cb(self.sub_plot_combinables, len(self.sub_plot_combinables)-1)))
		if len(self.sub_plot_combinables) > 3:
			self.sub_plot_combinations.extend(list(cb(self.sub_plot_combinables, len(self.sub_plot_combinables)-2)))
		self.whole_plot_combinations_options.clear()
		self.sub_plot_combinations_options.clear()
		for i in self.whole_plot_combinations:
			self.whole_plot_combinations_options.append("".join(i))
		for i in self.sub_plot_combinations:
			if (len(list(set(i) - set(self.sub_plot_letters))) >= 1) and (len(list(set(i) - set(self.whole_plot_letters))) >= 1):
				self.sub_plot_combinations_options.append("".join(i))
		print("\n")
		for i in self.generators_letters:
			print("For {}:".format(i))
			if i in self.whole_plot_letters:
				print(*self.whole_plot_combinations_options, sep=' -- ')
				print("\n")
			else:
				print(*self.sub_plot_combinations_options, sep=' -- ')
				print("\n")

	def setRelations(self):
		print("\n")
		lists = []
		while True:
			try:
				for i in self.generators_letters:
					inputted = input(i + ": ")
					lists.append((i, inputted))
					if inputted.lower() == 'help':
						import entry_point
						entry_point.iHelp()
				choice = input("\nDo you want to include interactions?\nEnter 'yes' or 'no': ").lower()
				if choice == "yes":
					print("\nEnter the interactions, one in a line. Press only the 'enter' key when you're done.\n")
					count = 0
					rels = []
					while True:
						count += 1
						prompt = "Interaction " + str(count) + " : "
						keys = input(prompt)
						if keys != "":
							rels.append(keys)
						else: break
				else: rels = []
				factors = copy.deepcopy(self.factors_letters)
				table = copy.deepcopy(self.tableObject)
				matrix = copy.deepcopy(self.matrixObject)
				for ID, values in lists:
					id_index = self.factors_letters.index(ID)
					index_list = []
					factors[id_index] += "=" + "".join(values)
					for i in values:
						index_list.append(factors.index(i))
					for j in range(len(table)):
						row_t = table[j]
						row_m = matrix[j]
						some_value = 1
						for i in index_list:
							some_value *= 1 if row_t[i] == "+" else -1
						row_t[id_index] = "+" if some_value == 1 else "-"
						row_m[id_index+1] = some_value
				break
			except (KeyboardInterrupt,EOFError):
				print("Program interrupted.")
			except Exception:
				print("Invalid inputs / case sensitivity error detected. Type 'help' for more information.")
				lists.clear()
				rels.clear()
				continue
		table_copy = copy.deepcopy(table)
		for i in range(len(table_copy)):
			combos = []
			for j in range(len(table_copy[i])):
				if table_copy[i][j] == "+":
					combos.append(self.factors_letters[j])
			if len(combos) != 0:
				table[i].append("".join(combos))
			else: table[i].append(1)
		factors.append("Trt.")
		for i in rels:
			factors.append(i)
			rels_list = []
			for a in i:
				rels_list.append(factors.index(a))
			for j in range(len(table)):
				row_t = table[j]
				row_m = matrix[j]
				some_value = 1
				for k in rels_list:
					some_value *= 1 if row_t[k] == "+" else -1
				if some_value==1:
					row_t.append("+")
				else: row_t.append("-")
				row_m.append(some_value)
		for i in range(len(table)):
			table[i].insert(0, i+1)
		self.visualizeTable(factors, table)
		print("\n\nMatrix generated:\n")
		self.visualizeMatrix(matrix)
		try:
			res_value, trace, det, pinv_det, min_lamda, pinv = self.getResolution(matrix)
			combinations_info = (factors, table, matrix, trace, det, pinv_det, min_lamda, res_value, pinv)
			self.various_combinations.append(combinations_info)
			self.writeToFile(combinations_info)
		except TypeError:
			print("Outputs not saved.")
			h = input("")

	def automateGens(self):
		self.used.clear()
		inst_minimum = []
		self.whole_plot_combinations_options.clear()
		self.sub_plot_combinations_options.clear()
		self.generateCombinations()
		times = int(input("How many number of runs?: "))
		choice = input("\nDo you want to include interactions?\nEnter 'yes' or 'no': ").lower()
		rels = []
		if choice == "yes":
			print("\nEnter the interactions, one in a line. Press only the 'enter' key when you're done.\n")
			count = 0
			while True:
				count += 1
				prompt = "Interaction " + str(count) + " : "
				keys = input(prompt)
				if keys != "":
					rels.append(keys)
				else: break
		setter = 0
		empty_count = 0
		# if len(rels) != 0:
		# 	self.used.clear()
		while setter < times:
			lists =[]
			wholeplots = len(self.whole_plot_combinations_options)
			subplots = len(self.sub_plot_combinations_options)
			for i in self.generators_letters:
				if i in self.whole_plot_combinations_options:
					lists.append((i, self.whole_plot_combinations_options[random.randint(0, wholeplots-1)]))
				else: lists.append((i, self.sub_plot_combinations_options[random.randint(0, subplots-1)]))
			if lists not in self.used:
				setter += 1
				self.used.append(lists)
				# generate automatically here
				factors = copy.deepcopy(self.factors_letters)
				table = copy.deepcopy(self.tableObject)
				matrix = copy.deepcopy(self.matrixObject)
				for ID, values in lists:
					id_index = self.factors_letters.index(ID)
					index_list = []
					factors[id_index] += "=" + "".join(values)
					for i in values:
						index_list.append(factors.index(i))
					for j in range(len(table)):
						row_t = table[j]
						row_m = matrix[j]
						some_value = 1
						for i in index_list:
							some_value *= 1 if row_t[i] == "+" else -1
						row_t[id_index] = "+" if some_value == 1 else "-"
						row_m[id_index+1] = some_value
				table_copy = copy.deepcopy(table)
				for i in range(len(table_copy)):
					combos = []
					for j in range(len(table_copy[i])):
						if table_copy[i][j] == "+":
							combos.append(self.factors_letters[j])
					if len(combos) != 0:
						table[i].append("".join(combos))
					else: table[i].append(1)
				factors.append("Trt.")
				for i in rels:
					factors.append(i)
					rels_list = []
					for a in i:
						rels_list.append(factors.index(a))
					for j in range(len(table)):
						row_t = table[j]
						row_m = matrix[j]
						some_value = 1
						for k in rels_list:
							some_value *= 1 if row_t[k] == "+" else -1
						if some_value==1:
							row_t.append("+")
						else: row_t.append("-")
						row_m.append(some_value)
				for i in range(len(table)):
					table[i].insert(0, i+1)
				self.visualizeTable(factors, table)
				print("\n\nMatrix generated:\n")
				self.visualizeMatrix(matrix)
				try:
					res_value, trace, det, pinv_det, min_lamda, pinv = self.getResolution(matrix)
					combinations_info = (factors, table, matrix, trace, det, pinv_det, min_lamda, res_value, pinv)
					self.various_combinations.append(combinations_info)
					self.writeToFile(combinations_info)
					inst_minimum.append((pinv_det, pinv))
				except TypeError:
					print("Outputs not saved.")
			else:
				empty_count += 1
				if empty_count >=100:
					print("\n\nExhausted all possible selections already.")
					break
		if len(inst_minimum) != 0:
			inst_max_det = max([i[0] for i in inst_minimum])
			inst_min_ress = min([i[1] for i in inst_minimum])
			print("\nMinimum Loss Function Value for this run only:", inst_min_ress)
			print("Maximum (1 + t)th root of determinant for this run only:", inst_max_det)
		ress = []
		deter = []
		trace = []
		min_res_obj = []
		max_det_obj = []
		max_trace_obj = []
		for i in self.various_combinations:
			if i[-1] != "" and i[-4] != "":
				ress.append(i[-1])
				deter.append(i[-4])
				trace.append(i[3])
		if len(ress) != 0:
			self.min_res = min(ress)
			self.max_det = max(deter)
			self.max_trace = max(trace)
			for i in self.various_combinations:
				if i[-1] == self.min_res:
					min_res_obj.append(i[0])
				if i[-4] == self.max_det:
					max_det_obj.append(i[0])
				if i[3] == self.max_trace:
					max_trace_obj.append(i[0])
			print("\nMinimum Loss Function Value:", self.min_res)
			print("")
			count = 1
			for s in min_res_obj:
				print("("+str(count)+")", *s, sep='\t')
				count += 1
			print("\nMaximum (1 + t)th root of Determinant Value:", self.max_det)
			count = 1
			for s in max_det_obj:
				print("("+str(count)+")", *s, sep='\t')
				count += 1
			print("\nMaximum Trace Value:", self.max_trace)
			count = 1
			for s in max_trace_obj:
				print("("+str(count)+")", *s, sep='\t')
				count += 1
			with open("Outputs/"+self.design_name, "a") as f:
				wr = csv.writer(f, delimiter='\t')
				wr.writerow(["Minimum Loss Function Value:",self.min_res])
				wr.writerow(["Maximum (1 + t)th root of Determinant Value:",self.max_det])
				wr.writerow(["Maximum Trace Value:",self.max_trace])
				wr.writerow([])
				wr.writerow(["========================================================================"])

	def showVariousCombinations(self):
		print("=============================================================================")
		for i in self.various_combinations:
			self.visualizeTable(i[0], i[1])
			self.visualizeMatrix(i[2])
			print("Trace:", i[3])
			print("Determinant:", i[4])
			print("Minimum Eigen Value:", i[5])
			print("Loss function:", i[6])
			print("(1 + t)th root:", i[7])
			print("=============================================================================\n")

	def getZed(self):
		no_of_subs = len(set(self.non_generators_letters) - set(self.whole_plot_letters))
		no_of_wholes = len(self.non_generators_letters) - no_of_subs
		self.zed_list = []
		rows = []
		self.sub_number = 2**no_of_subs
		for i in range(2**(no_of_subs+no_of_wholes)):
			rows.clear()
			pos = i//(self.sub_number)
			for j in range(2**(no_of_wholes)):
				rows.append(1 if len(rows) == pos else 0)
			self.zed_list.append(rows[:])
		self.identity = []
		rows = []
		no_of_rows = len(self.zed_list)
		for i in range(no_of_rows):
			rows.clear()
			for j in range(no_of_rows):
				rows.append(1 if i == j else 0)
			self.identity.append(rows[:])

	def getResolution(self, matrix):
		try:
			zed = copy.deepcopy(self.zed_list)
			identity = copy.deepcopy(self.identity)
			matrix_transpose = mt.transposeMatrix(matrix)
			zed_transpose = mt.transposeMatrix(zed)
			zed_by_zed_transpose = mt.multiplyMatrix(zed, zed_transpose)
			self.sigma = mt.addMatrix(identity, zed_by_zed_transpose)
			sigma_inverse = self.getSigmaInverse(self.sigma)
			if sigma_inverse is not None:
				mul_1 = mt.multiplyMatrix(matrix_transpose, sigma_inverse)
			else:
				print("\nSigma matrix obtained non-invertible, i.e. determinant = 0")
				return None
			mul_2 = mt.multiplyMatrix(mul_1, matrix)
			for a in range(len(mul_2)):
				for b in range(len(mul_2[a])):
					if (mul_2[a][b] > -1.0/(10**10) and mul_2[a][b] < -1.0/(10**20)) or (mul_2[a][b] < 1.0/(10**10) and mul_2[a][b] > 1.0/(10**20)):
						if abs(mul_2[a][b]) == mul_2[a][b]: mul_2[a][b] = 0.0000
						else: mul_2[a][b] = -0.0000
			eig_values = mt._eig(mul_2)
			min_lamda = eig_values.min()
			min_lamda = np.asscalar(min_lamda)
			sign, a = np.linalg.slogdet(mul_2)
			det = sign*np.exp(a)
			trace = 0
			for i in range(len(mul_2)):
				trace += mul_2[i][i]
			print("\nTrace of the matrix:", trace)
			print("Minimum Eigen Value:", min_lamda)
			print("Determinant:", det)
			powe = len(matrix_transpose)
			if det != 0:
				pinv_det = det**(1/powe)
				print("(1 + t)th root for Determinant:", pinv_det)
				res_value = (1 + (2**self.factors) - min_lamda)/det
				print("Loss function:", res_value)
				PInv = res_value**(1/powe)
				print("(1 + t)th root:", PInv)
				return (res_value, trace, det, pinv_det, min_lamda, PInv)
			else:
				print("\nMatrix obtained non-invertible, i.e. determinant = 0")
				return None
		except KeyboardInterrupt:
			print("\nProgram interrupted.")
		except Exception as e:
			print("Error:",e)

	def getSigmaInverse(self, sigma):
		block = []
		for i in range(self.sub_number):
			block.append(sigma[i][:self.sub_number])
		block_inverse = mt.getMatrixInverse(block)
		sigma_copy = copy.deepcopy(sigma[:])
		if block_inverse is not None:
			for i in range(len(sigma_copy[:])):
				pos = i//self.sub_number
				col = i % self.sub_number
				sigma_copy[i][self.sub_number*pos:self.sub_number*(1+pos)] = block_inverse[col][:]
			return sigma_copy
		else: return None

	def getMinimumResolution(self):
		ress = []
		deter = []
		trace = []
		min_res_obj = []
		max_det_obj = []
		max_trace_obj = []
		for i in self.various_combinations:
			if i[-1] != "" and i[-4] != "":
				ress.append(i[-1])
				deter.append(i[-4])
				trace.append(i[3])
		if len(ress) != 0:
			self.min_res = min(ress)
			self.max_det = max(deter)
			self.max_trace = max(trace)
			for i in self.various_combinations:
				if i[-1] == self.min_res:
					min_res_obj.append(i[0])
				if i[-4] == self.max_det:
					max_det_obj.append(i[0])
				if i[3] == self.max_trace:
					max_trace_obj.append(i[0])
			print("Minimum Loss Function Value:", self.min_res)
			print("")
			count = 1
			for s in min_res_obj:
				print("("+str(count)+")", *s, sep='\t')
				count += 1
			print("Maximum (1 + t)th root of Determinant Value:", self.max_det)
			count = 1
			for s in max_det_obj:
				print("("+str(count)+")", *s, sep='\t')
				count += 1
			print("Maximum Trace Value:", self.max_trace)
			count = 1
			for s in max_trace_obj:
				print("("+str(count)+")", *s, sep='\t')
				count += 1
		else: print("No value obtained so far in this running test")

	def randomToNormal(self):
		self.generate()

	def changeGenerators(self):
		msg = "\nType the letters to use as generators.(examples: Cqr, r, DE, and so on.)\nTake note of the case sensitivity: "
		generator_set = []
		while True:
			try:
				options = str(input(msg))
				for i in options:
					if i in self.whole_plot_letters or i in self.sub_plot_letters:
						generator_set.append(str(i))
					else:
						print("Case sensitivity / invalid input error.")
						raise ValueError
				break
			except KeyboardInterrupt:
				print("Program interrupted.")
				continue
			except ValueError:
				continue
			except Exception:
				print("Invalid choice.")
				continue
		self.generators_letters.clear()
		self.generators_letters = copy.deepcopy(generator_set)
		self.__initialize()

	def showSigma(self):
		print("\nSIGMA MATRIX", *self.sigma, sep='\n')

	def writeToFile(self, info_list):
		factors, table, matrix, trace, det, pinv_det, min_lamda, res_value, pinv = info_list
		factors.insert(0, "")
		with open("Outputs/"+self.design_name, "a") as f:
			wr = csv.writer(f, delimiter='\t')
			wr.writerow(["TABLE"])
			wr.writerow([])
			wr.writerow(factors)
			wr.writerows(table)
			wr.writerow([])
			wr.writerow(["MATRIX"])
			wr.writerow([])
			wr.writerows(matrix)
			wr.writerow([])
			wr.writerow(["Trace:", trace])
			wr.writerow(["Determinant:", det])
			wr.writerow(["(1 + t)th root for determinant:", pinv_det])
			wr.writerow(["Minimum Eigen Value:", min_lamda])
			wr.writerow(["Loss function:", res_value])
			wr.writerow(["(1 + t)th root:", pinv])
			wr.writerow([])
			wr.writerow(["===================================================================================="])
			wr.writerow([])

	def randomSelection(self, mode="normal", vals=None):
		while True:
			random_set = []
			random_table = []
			random_matrix = []
			i = 0
			while i < self.number_of_runs:
				random_val = random.randint(1, 2**self.factors)
				if random_val not in random_set:
					random_set.append(random_val)
					i += 1
			if random_set not in self.random_sets:
				break
		for i in random_set:
			i -= 1
			signs = []
			rems = []
			while i > 0:
				if i%2 == 0:
					signs.append("-")
					rems.append(-1)
				else:
					signs.append("+")
					rems.append(+1)
				i = i // 2
			if len(signs) != self.factors:
				[signs.append("-") for i in range(self.factors - len(signs))]
				[rems.append(-1) for i in range(self.factors - len(rems))]
			random_table.append(signs)
			random_matrix.append(rems)
		if mode == "normal":
			while True:
				try:
					choice = input("\nDo you want to include interactions?\nEnter 'yes' or 'no': ").lower()
					if choice == "yes":
						print("\nEnter the interactions, one in a line. Press only the 'enter' key when you're done.\n")
						count = 0
						rels = []
						while True:
							count += 1
							prompt = "Interaction " + str(count) + " : "
							keys = input(prompt)
							if keys != "":
								rels.append(keys)
							else: break
					else: rels = []
					factors = copy.deepcopy(self.factors_letters)
					break
				except (KeyboardInterrupt,EOFError):
					print("Program interrupted.")
				except Exception:
					print("Invalid inputs / case sensitivity error detected. Type 'help' for more information.")
					rels.clear()
					continue
		elif mode == "auto":
			rels = []
			factors = copy.deepcopy(self.factors_letters)
		elif mode == "interactions":
			rels = vals
			factors = copy.deepcopy(self.factors_letters)
		else:
			print("Mode incorrect.")
		table_copy = copy.deepcopy(random_table)
		for i in range(len(table_copy)):
			combos = []
			for j in range(len(table_copy[i])):
				if table_copy[i][j] == "+":
					combos.append(self.factors_letters[j])
			if len(combos) != 0:
				random_table[i].append("".join(combos))
			else: random_table[i].append(1)
		factors.append("Trt.")
		for i in rels:
			factors.append(i)
			rels_list = []
			for a in i:
				rels_list.append(factors.index(a))
			for j in range(len(random_table)):
				row_t = random_table[j]
				row_m = random_matrix[j]
				some_value = 1
				for k in rels_list:
					some_value *= 1 if row_t[k] == "+" else -1
				if some_value==1:
					row_t.append("+")
				else: row_t.append("-")
				row_m.append(some_value)
		for i, g in zip(random_set, range(len(random_table))):
			random_table[g].insert(0, i)
		for i in range(len(random_matrix)):
			random_matrix[i].insert(0, 1)
		self.visualizeTable(factors, random_table)
		print("\n\nMatrix generated:\n")
		self.visualizeMatrix(random_matrix)
		try:
			res_value, trace, det, pinv_det, min_lamda, pinv = self.getResolution(random_matrix)
			combinations_info = (factors, random_table, random_matrix, trace, det, pinv_det, min_lamda, res_value, pinv)
			self.various_combinations.append(combinations_info)
			self.writeToFile(combinations_info)
		except TypeError:
			print("Outputs not saved.")

	def automateRandom(self):
		modes = input("Mode: ")
		no_of_tests = int(input("How many number of runs?: "))
		if modes == "interactions":
			print("\nEnter the interactions, one in a line. Press only the 'enter' key when you're done.\n")
			count = 0
			rels = []
			while True:
				count += 1
				prompt = "Interaction " + str(count) + " : "
				keys = input(prompt)
				if keys != "":
					rels.append(keys)
				else: break
		for i in range(no_of_tests):
			if modes == "auto":
				self.randomSelection(mode="auto")
			elif modes == "interactions":
				self.randomSelection(mode="interactions", vals=rels)
		ress = []
		deter = []
		trace = []
		min_res_obj = []
		max_det_obj = []
		max_trace_obj = []
		for i in self.various_combinations:
			if i[-1] != "" and i[-4] != "":
				ress.append(i[-1])
				deter.append(i[-4])
				trace.append(i[3])
		if len(ress) != 0:
			self.min_res = min(ress)
			self.max_det = max(deter)
			self.max_trace = max(trace)
			for i in self.various_combinations:
				if i[-1] == self.min_res:
					min_res_obj.append(i[0])
				if i[-4] == self.max_det:
					max_det_obj.append(i[0])
				if i[3] == self.max_trace:
					max_trace_obj.append(i[0])
			print("\nMinimum Loss Function Value:", self.min_res)
			print("")
			count = 1
			for s in min_res_obj:
				print("("+str(count)+")", *s, sep='\t')
				count += 1
			print("\nMaximum (1 + t)th root of Determinant Value:", self.max_det)
			count = 1
			for s in max_det_obj:
				print("("+str(count)+")", *s, sep='\t')
				count += 1
			print("\nMaximum Trace Value:", self.max_trace)
			count = 1
			for s in max_trace_obj:
				print("("+str(count)+")", *s, sep='\t')
				count += 1
			with open("Outputs/"+self.design_name, "a") as f:
				wr = csv.writer(f, delimiter='\t')
				wr.writerow(["Minimum Loss Function Value:",self.min_res])
				wr.writerow(["Maximum (1 + t)th root of Determinant Value:",self.max_det])
				wr.writerow(["Maximum Trace Value:",self.max_trace])
