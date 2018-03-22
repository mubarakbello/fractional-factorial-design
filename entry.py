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
		while True:
			try:
				factors = int(input("Enter number of factors: "))
				break
			except Exception as e:
				print("Invalid input")
		while True:
			try:
				generators = int(input("Enter number of generators: "))
				break
			except Exception as e:
				print("Invalid input")
		while True:
			try:
				whole_plot = int(input("Enter number of whole plots: "))
				if whole_plot > factors: continue
				else: break
			except Exception as e:
				print("Invalid input")
		while True:
			try:
				sub_plot = int(input("Enter number of sub plots: "))
				if sub_plot != factors - whole_plot:
					print("Number of whole plots and sub plots doesn't add up.")
					continue
				else: break
			except Exception as e:
				print("Invalid input")
		os.system("cls")
		obj_dict[prompt_msg] = fd(factors, generators, whole_plot, sub_plot)
	obj_handle = obj_dict[prompt_msg]
	while True:
		print("\n\n")
		prompt = input(prompt_msg+">>")
		if prompt == "back":
			break
		elif prompt == "help":
			iHelp()
		elif prompt.startswith("random"):
			# randomize table to get varying values for each column
			pass

		#####################################################
		# for setting varying values
		elif prompt.startswith("set"):
			parameter = prompt.split(" ")[1]
			# value = prompt.split(" ")[-1]
			if parameter.startswith("generators"):
				# set obj_handle.generators to value
				pass
			elif parameter.startswith("relation"):
				# set all relations from options given to value
				obj_handle.setRelations()
				# id = prompt.split(" ")[2]
				# values = [i for i in value]
				# obj_handle.setRelations(id, values)

		#####################################################
		# for showing tables, options, results

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
				obj_handle.visualizeDefaultTable()
			elif parameter.startswith("interaction"):
				# set obj_handle.interaction to value
				pass

entry_point()