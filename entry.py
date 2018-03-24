import os, sys
from module import FactorialDesign as fd


obj_dict = {}

def entry_point():
	welcome_msg = """Factorial Design
Start by entering the numbers of factors, generators, whole plot and sub plot.
Type "help" anytime for more information"""
	os.system("cls")
	print(welcome_msg)
	while True:
		try:
			prompt = input(">>").lower()
		except (KeyboardInterrupt, EOFError):
			print("\nProgram exiting...")
			sys.exit()
		if prompt == "quit" or prompt == "exit" or prompt == "back":
			break
		elif prompt.startswith("start"):
			try:
				obj_name = prompt.split(" ")[1]
			except IndexError:
				print("Command incorrectly typed. Type 'help' to get more information")
				continue
			inSampleMode(obj_name)
			os.system("cls")
			print(welcome_msg)
		elif prompt == "help":
			iHelp()

def iHelp():
	help_msg = """
HELP UTILITY FOR FACTORIAL DESIGN PROGRAM

Start by typing 'start ::design_name::', where design_name
(without the colons) is the name you are giving to the design
test you are about to run.

You will be prompted to input the required details if it is
your first time running the design test. You now have an
interface that looks like this:
design_name>>
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
			except KeyboardInterrupt:
				print("Program exiting...")
				sys.exit()
			except Exception as e:
				print("Invalid input")
		while True:
			try:
				generators = int(input("Enter number of generators: "))
				break
			except KeyboardInterrupt:
				print("Program exiting...")
				sys.exit()
			except Exception as e:
				print("Invalid input")
		while True:
			try:
				whole_plot = int(input("Enter number of whole plots: "))
				if whole_plot > factors: continue
				else: break
			except KeyboardInterrupt:
				print("Program exiting...")
				sys.exit()
			except Exception as e:
				print("Invalid input")
		while True:
			try:
				sub_plot = int(input("Enter number of sub plots: "))
				if sub_plot != factors - whole_plot:
					print("Number of whole plots and sub plots doesn't add up.")
					continue
				else: break
			except KeyboardInterrupt:
				print("Program exiting...")
				sys.exit()
			except Exception as e:
				print("Invalid input")
		os.system("cls")
		obj_dict[prompt_msg] = fd(factors, generators, whole_plot, sub_plot)
	obj_handle = obj_dict[prompt_msg]
	while True:
		print("\n\n")
		try:
			prompt = input(prompt_msg+">>")
		except (KeyboardInterrupt, EOFError):
			print("Program exiting...")
			sys.exit()
		if prompt == "back":
			break
		elif prompt == "help":
			iHelp()
		elif prompt.startswith("random"):
			# randomize table to get varying values for each column
			obj_handle.randomizeTable()
		elif prompt.startswith("normal"):
			# return table to normal flow
			obj_handle.randomToNormal()

		#####################################################
		# for setting varying values
		elif prompt.startswith("set"):
			try:
				parameter = prompt.split(" ")[1]
			except IndexError:
				print("Command incorrectly typed. Type 'help' to get more information")
				continue
			if parameter.startswith("generat"):
				# set obj_handle.generators to value
				pass
			elif parameter.startswith("relation"):
				# set all relations from options given to value
				obj_handle.setRelations()

		#####################################################
		# for showing tables, options, results

		elif prompt.startswith("show"):
			try:
				parameter = prompt.split(" ")[1:]
			except IndexError:
				print("Command incorrectly typed. Type 'help' to get more information")
				continue
			if "z" in parameter:
				# print matrix
				obj_handle.getZed()
			if "options" in parameter:
				# print options for each generators
				obj_handle.generateCombinations()
			elif "table" in parameter:
				# print table
				obj_handle.visualizeDefaultTable()
			elif "combinations" in parameter:
				# set obj_handle.interaction to value
				obj_handle.showVariousCombinations()
			elif "resolution" in parameter:
				# set obj_handle.interaction to value
				obj_handle.getMinimumResolution()

entry_point()