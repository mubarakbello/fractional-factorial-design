import copy
from itertools import combinations as cb

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
		print("New Sampling object created.\n")
		self.__initialize()

	def __initialize(self):
		# to be called once by __init__ and when values change
		self.whole_plot_list = "A B C D E F G H I J K L M N O".split(" ")
		self.sub_plot_list = "p q r s t u v w x y z".split(" ")
		self.whole_plot_letters = self.whole_plot_list[0:self.whole_plot]
		self.sub_plot_letters = self.sub_plot_list[0:self.sub_plot] if self.sub_plot != 0 else []
		if self.sub_plot != 0:
			if self.generators < self.sub_plot:
				self.generators_letters = self.sub_plot_letters[-self.generators:]
			else:
				num = self.generators - self.sub_plot + 1
				self.generators_letters = self.whole_plot_letters[-num:]
				self.generators_letters.extend(self.sub_plot_letters[1:])
		else: self.generators_letters = self.whole_plot_letters[-self.generators:]
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
		number_of_runs = 2**self.factor_diff
		if len(self.tableObject) != 0:
			self.tableObject.clear()
			self.matrixObject.clear()
		for i in range(number_of_runs):
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
			self.tableObject.append(bloated_signs)
			self.matrixObject.append(bloated_rems)

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

	def visualizeMatrix(self):
		print("")
		for row in self.matrixObject:
			print("", *row, sep='\t')

	def generateCombinations(self):
		if len(self.whole_plot_letters) - len(self.whole_plot_combinables) == 1:
			self.whole_plot_combinations.append(list(self.whole_plot_combinables))
		else:
			self.whole_plot_combinations.extend(list(cb(self.whole_plot_combinables, len(self.whole_plot_combinables)-1)))
			if len(self.whole_plot_combinables) > 3:
				self.whole_plot_combinations.extend(list(cb(self.whole_plot_combinables, len(self.whole_plot_combinables)-2)))
		self.sub_plot_combinations.extend(list(cb(self.sub_plot_combinables, len(self.sub_plot_combinables)-1)))
		# if len(list(set(self.sub_plot_combinables) - self.whole_plot_combinables))
		self.sub_plot_combinations.extend(list(cb(self.sub_plot_combinables, len(self.sub_plot_combinables)-2)))
		self.whole_plot_combinations_options.clear()
		self.sub_plot_combinations_options.clear()
		for i in self.whole_plot_combinations:
			self.whole_plot_combinations_options.append("".join(i))
		for i in self.sub_plot_combinations:
			self.sub_plot_combinations_options.append("".join(i))
		for i in self.generators_letters:
			print("For {}".format(i))
			if i in self.whole_plot_letters:
				print(*self.whole_plot_combinations_options, sep=' -- ')
			else:
				print(*self.sub_plot_combinations_options, sep=' -- ')
			print(" ")

	def setRelations(self):
		lists = []
		for i in self.generators_letters:
			lists.append((i, input(i + ": ")))
		factors = copy.deepcopy(self.factors_letters)
		table = copy.deepcopy(self.tableObject)
		for ID, values in lists:
			id_index = self.factors_letters.index(ID)
			index_list = []
			factors[id_index] += "=" + "".join(values)
			for i in values:
				index_list.append(factors.index(i))
			for row in table:
				some_value = 1
				for i in index_list:
					some_value *= 1 if row[i] == "+" else -1
				row[id_index] = "+" if some_value == 1 else "-"
		self.visualizeTable(factors=factors,table=table)


class ErrorHandlers():
	"""docstring for ErrorHandlers"""
	def __init__(self):
		pass
