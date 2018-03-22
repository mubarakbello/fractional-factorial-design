import os
from module import FactorialDesign as fd


obj_dict = {}

def entry_point():
	welcome_msg = """Factorial Design
Start by entering the numbers of factors, generators, whole plot and sub plot.
Type "help" anytime for more information"""
	os.system("cls")
	print(welcome_msg)
	while True:
		prompt = input(">>").lower()
		if prompt == "quit" or prompt == "exit" or prompt == "back":
			break
		elif prompt.startswith("start"):
			obj_name = prompt.split(" ")[1]
			inSampleMode(obj_name)
			os.system("cls")
		elif prompt == "help":
			iHelp()

def iHelp():
	help_msg = """
HELP OPT
"""
	print(help_msg)

def inSampleMode(prompt_msg):
	global obj_dict
	os.system("cls")
	if prompt_msg not in obj_dict:
		factors = int(input("Enter number of factors: "))
		generators = int(input("Enter number of generators: "))
		whole_plot = int(input("Enter number of whole plots: "))
		sub_plot = int(input("Enter number of sub plots: "))
		obj_dict[prompt_msg] = fd(factors, generators, whole_plot, sub_plot)
	obj_handle = obj_dict[prompt_msg]
	while True:
		prompt = input(prompt_msg+">>")
		if prompt == "back":
			break
		elif prompt == "help":
			iHelp()
		elif prompt.startswith("random"):
			# randomize table to get varying values for each column
			pass
		elif prompt.startswith("factors"):
			# set value of factors
			obj_handle.factors = int(prompt.split("=")[-1])
		elif prompt.startswith("generators"):
			# set value of generators
			obj_handle.generators = int(prompt.split("=")[-1])
			print(obj_handle.generators)
		elif prompt.startswith("whole"):
			# set value of whole plots
			obj_handle.whole_plot = int(prompt.split("=")[-1])
		elif prompt.startswith("sub"):
			# set value of sub plots
			obj_handle.sub_plot = int(prompt.split("=")[-1])

		#####################################################
		# for setting varying values

		elif prompt.startswith("set"):
			parameter = prompt.split(" ")[1]
			value = prompt.split(" ")[-1]
			if parameter.startswith("generators"):
				# set obj_handle.generators to value
				obj_handle.generators_letters = [i for i in value]
				obj_handle.generators = len(value)
				print(obj_handle.generators_letters)
			elif parameter.startswith("whole"):
				# set obj_handle.whole_plot to value
				obj_handle.whole_plot_letters = [i for i in value]
				obj_handle.whole_plot = len(value)
			elif parameter.startswith("sub"):
				# set obj_handle.sub_plot to value
				obj_handle.sub_plot_letters = [i for i in value]
				obj_handle.sub_plot = len(value)
			elif parameter.startswith("relation"):
				# set all relations from options given to value
				id = prompt.split(" ")[2]
				values = [i for i in value]
				obj_handle.setRelations(id, values)
		elif prompt.startswith("show"):
			parameter = prompt.split(" ")[1]
			if parameter.startswith("matrix"):
				# print matrix
				obj_handle.visualizeMatrix()
			elif parameter.startswith("options"):
				# print options for each generators
				obj_handle.generateCombinations()
			elif parameter.startswith("table"):
				# print table
				obj_handle.visualizeTable()
			elif parameter.startswith("interaction"):
				# set obj_handle.interaction to value
				pass

entry_point()