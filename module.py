class FactorialFinder():
	"""	docstring for FactorialFinder"""
	def __init__(self, factors, generators, whole_plot=None, sub_plot=0):
		self.__whole_plot_letters = "A B C D E F G H I J K L M N O".split(" ")
		self.__sub_plot_letters = "p q r s t u v w x y z".split(" ")
		self.factors = factors
		self.generators = generators
		if whole_plot == None:
			self.whole_plot = factors
		else:
			self.whole_plot = whole_plot
		self.sub_plot = sub_plot
		self.wholes = self.__whole_plot_letters[0:self.whole_plot]
		if self.sub_plot != 0:
			self.subs = self.__sub_plot_letters[0:self.sub_plot]
		else: self.subs = []
		print("New sampling object created with:\nNumber of Factors(k) = {}\nNumber of Generators(p) = {}".format(self.factors, self.generators))
		print("Number of Whole Plot [", *self.wholes, "] = {}".format(self.whole_plot), sep=' ')
		print("Number of Sub Plot [" ,*self.subs, "] = {}".format(self.sub_plot), sep=' ')

	def generateTable(self):
		"""Method to generate table"""
		self.factor_diff = self.factors - self.generators
		number_of_runs = 2**self.factor_diff
		self.tableObject = []
		for i in range(number_of_runs):
			rems = []
			while i > 0:
				rems.append(i%2)
				i = i // 2
			if len(rems) != self.factor_diff:
				[rems.append(0) for i in range(self.factor_diff - len(rems))]
			print(rems)
			self.tableObject.append(rems)

	def visualizeTable(self):
		pass

	def visualizeMatrix(self):
		pass


class ErrorHandlers():
	"""docstring for ErrorHandlers"""
	def __init__(self):
		pass


# myObj = FactorialFinder(10, 3)
