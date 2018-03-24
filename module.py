import sys, copy, random
from itertools import combinations as cb
from fractions import Fraction
import matrices as mt
import numpy as np

class FactorialDesign():
	"""	docstring for FactorialFinder"""
	def __init__(self, factors, generators, whole_plot=None, sub_plot=0):
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
		else: self.generators_letters = []
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
		for row, i in zip(table, range(len(table))):
			print(i+1, *row, sep='\t')

	def visualizeMatrix(self, matrix):
		print("")
		for row in matrix:
			print("", *row, sep='\t')

	def generateCombinations(self):
		self.whole_plot_combinations_options.clear()
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
			if (len(list(set(i) - set(self.sub_plot_letters))) > 1) and (len(list(set(i) - set(self.whole_plot_letters))) >= 1):
				self.sub_plot_combinations_options.append("".join(i))
		print(*self.sub_plot_combinables, sep='\t')
		for i in self.generators_letters:
			print("For {}".format(i))
			if i in self.whole_plot_letters:
				print(*self.whole_plot_combinations_options, sep=' -- ')
			else:
				print(*self.sub_plot_combinations_options, sep=' -- ')
			print(" ")

	def setRelations(self):
		lists = []
		while True:
			try:
				for i in self.generators_letters:
					lists.append((i, input(i + ": ")))
				choice = input("\nDo you want to include a requirement set?\nEnter 'yes' or 'no': ").lower()
				if choice == "yes":
					print("\nEnter the defining relations, one in a line. Press only the 'enter' key when you're done.\n")
					count = 0
					rels = []
					while True:
						count += 1
						prompt = "Defining relation " + str(count) + " : "
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
				sys.exit()
			except Exception:
				print("Invalid inputs detected. Type 'help' for more information.")
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
		self.visualizeTable(factors, table)
		print("\n\nMatrix generated:\n")
		self.visualizeMatrix(matrix)
		res_value = self.getResolution(matrix)
		combinations_info = [lists, table, matrix, res_value]
		self.various_combinations.append(combinations_info)

	def showVariousCombinations(self):
		print(*self.various_combinations, sep='\n')

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
			sigma = mt.addMatrix(identity, zed_by_zed_transpose)
			sigma_inverse = self.getSigmaInverse(sigma)
			mul_1 = mt.multiplyMatrix(matrix_transpose, sigma_inverse)
			mul_2 = mt.multiplyMatrix(mul_1, matrix)
			trace = 0
			dets = 1
			eigen_values = []
			for i in range(len(mul_2)):
				eigen_values.append(mul_2[i][i])
				trace += mul_2[i][i]
				dets *= mul_2[i][i]
			print("\nTrace of the matrix:", trace)
			print("Dets of the matrix:", dets)
			# eig_values = mt._eig(mul_2)
			# min_lamda = eig_values.min()
			# min_lamda = np.asscalar(min_lamda)
			min_lamda = min(eigen_values)
			print("Minimum Eigen Value:", min_lamda)
			sign, a = np.linalg.slogdet(mul_2)
			det = sign*np.exp(a)
			print("Determinant:", det)
			powe = len(matrix_transpose)
			if det != 0:
				res_value = (1 + (2**self.factors) - min_lamda)/det
				print("Resolution value:", res_value)
				PInv = res_value**(1/powe)
				print("Loss function:", PInv)
				return res_value
			else:
				print("\nMatrix obtained non-invertible, i.e. determinant = 0")
				return None
		except KeyboardInterrupt:
			print("\nProgram interrupted.")

	def getSigmaInverse(self, sigma):
		block = []
		for i in range(self.sub_number):
			block.append(sigma[i][:self.sub_number])
		block_inverse = mt.getMatrixInverse(block)
		sigma_copy = copy.deepcopy(sigma[:])
		for i in range(len(sigma_copy[:])):
			pos = i//self.sub_number
			col = i % self.sub_number
			sigma_copy[i][self.sub_number*pos:self.sub_number*(1+pos)] = block_inverse[col][:]
		return sigma_copy

	def getMinimumResolution(self):
		ress = []
		for i in self.various_combinations:
			if i[-1] != "":
				ress.append(i[-1])
		if len(ress) != 0:
			self.min_res = min(ress)
			print("Best resolution:", self.min_res)
		else: print("No resolution obtained so far in this running test")

	def randomizeTable(self):
		index_list = []
		for i in range(len(self.tableObject[0])):
			if self.tableObject[0][i] == "+" or self.tableObject[0][i] == "-": index_list.append(i)
		copy_table = []
		copy_matrix = []
		dim_r, dim_c = len(self.tableObject), len(self.tableObject[0])
		i =  0
		while i < dim_r:
			c = ["-", "+"]
			row_i = []
			row_m = [1]
			for j in range(dim_c):
				randkey = random.randint(0,1)
				if len(row_i) in index_list:
					row_i.append(c[randkey])
					row_m.append(randkey)
				else:
					row_i.append(" ")
					row_m.append(" ")
			if row_i not in copy_table:
				copy_table.append(row_i)
				copy_matrix.append(row_m)
				i += 1
		self.tableObject.clear()
		self.matrixObject.clear()
		self.tableObject = copy.deepcopy(copy_table)
		self.matrixObject = copy.deepcopy(copy_matrix)

	def randomToNormal(self):
		self.generate()