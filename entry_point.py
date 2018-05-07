import os, sys
from module import FactorialDesign as fd


obj_dict = {}

def entry_point():
	welcome_msg = """=======================================================================
======================= FACTORIAL DESIGN PROGRAM ======================
======================================================================="""
	global help_msg
	help_msg = """
=========================================
HELP UTILITY FOR FACTORIAL DESIGN PROGRAM
=========================================

Start by typing 'start ::design_name::', where design_name
(without the colons) is the name you are giving to the design
test you are about to run.

You will be prompted to input the required details if it is
your first time running the design test. You now have an
interface that looks like this:
design_name>>

"""
	os.system("cls")
	print(welcome_msg)
	print(help_msg)
	print("-----------------------------------------------------------------\n\n")
	while True:
		try:
			prompt = input(">>").lower()
		except (KeyboardInterrupt, EOFError):
			print("\nProgram exiting...")
			sys.exit()
		if prompt == "quit" or prompt == "exit":
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
=========================================
HELP UTILITY FOR FACTORIAL DESIGN PROGRAM
=========================================

Start by typing 'start ::design_name::', where design_name
(without the colons) is the name you are giving to the design
test you are about to run.

You will be prompted to input the required details if it is
your first time running the design test. You now have an
interface that looks like this:
design_name>>
"""
	print(help_msg)
	options = """
WORKFLOW OF PROGRAM:
	1. Enter the details such as numbers of factors, whole plots, generators, etc.
	2. View the table to see what's automatically generated
	3. Change the generators assigned if need be
	4. View the different options automatically provided for each generator
	5. Select the generators and run the test, results will be displayed upon completion
	6. Try several options for the generators by repeating 6
	7. Vies the best design with the minimum loss function value
	8. View the summary of the tests run so far



TO SHOW THE TABLE GENERATED:
	Command:	show table

TO CHANGE THE GENERATORS AUTOMATICALLY GENERATED:
	Command:	change generators

TO SHOW DIFFERENT OPTIONS FOR GENERATORS:
	Command:	show options

TO SELECT GENERATORS, INTERACTIONS AND TO ANALYZE MATRIX GENERATED:
	Command:	choose generators

TO MAKE THE TABLE AND MATRIX ENTRIES RANDOMLY GENERATED:
	Command:	random

TO RETURN TABLE AND MATRIX TO THEIR NORMAL FORM INSTEAD OF RANDOM FORM:
	Command:	normal

TO AUTOMATE RANDOM DESIGNS GENERATION:
	Command:	automate random
	Type 'auto' when asked for the 'mode' if there are no interaction involved.
	Type 'interactions' when asked for the 'mode' if you want to include interactions
	After that, enter the number of runs you want to carry out.

TO AUTOMATE NORMAL GENERATORS DESIGN:
	Command:	automate normal
	Enter the number of runs you want to carry out
	Then add generators if you wish

	NOTE::::::
	Number of runs here must not be greater than all possible combinations of the generators!

TO SHOW THE VALUE OF THE 'SIGMA' MATRIX:
	Command:	show sigma

TO SHOW THE BEST DESIGN WITH THE MINIMUM LOSS FUNCTION VALUE:
	Command:	show minimum

TO SHOW ALL TESTS RUN SINCE PROGRAM STARTED OR TO SHOW SUMMARY OF TESTS:
	Command:	show tests

TO CREATE A NEW TEST CASE:
	Commands:	back
			start ::design-name::
	::design-name:: is the name to give to the new test case.

TO GO BACK TO A PREVIOUSLY CREATED TEST CASE WITHOUT LOSING TRACK OF THE PRESENT TEST:
	Commands:	back
			start ::design-name::
	::design-name:: is the name you gave to the test case when you created it.

"""
	print(options)

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
				c = input("Press enter to close")
			except Exception as e:
				print("Invalid input")
		os.system("cls")
		obj_dict[prompt_msg] = fd(factors, generators, prompt_msg, whole_plot, sub_plot)
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
		elif prompt == "exit" or prompt == "quit":
			sys.exit()
		elif prompt.startswith("random"):
			# randomize table to get varying values for each column
			obj_handle.randomSelection()
		elif prompt.startswith("normal"):
			# return table to normal flow
			obj_handle.randomToNormal()

		#####################################################
		# for setting varying values
		elif prompt.startswith("choose"):
			try:
				parameter = prompt.split(" ")[1]
			except IndexError:
				print("Command incorrectly typed. Type 'help' to get more information")
				continue
			if parameter.startswith("generator"):
				# set all generators from options given to value
				obj_handle.setRelations()

		#####################################################
		# for showing tables, options, results

		elif prompt.startswith("show"):
			try:
				parameter = prompt.split(" ")[1]
			except IndexError:
				print("Command incorrectly typed. Type 'help' to get more information")
				continue
			if parameter.startswith("sigma"):
				# print sigma
				obj_handle.showSigma()
			if parameter.startswith("option"):
				# print options for each generators
				obj_handle.generateCombinations()
			elif parameter.startswith("table"):
				# print table
				obj_handle.visualizeDefaultTable()
			elif parameter.startswith("test"):
				# show all test cases
				obj_handle.showVariousCombinations()
			elif parameter.startswith("minimu"):
				# set obj_handle.interaction to value
				obj_handle.getMinimumResolution()

		#####################################################
		# for changing generators , etc

		elif prompt.startswith("change"):
			try:
				parameter = prompt.split(" ")[1]
			except IndexError:
				print("Command incorrectly typed. Type 'help' to get more information")
				continue
			if parameter.startswith("generator"):
				# change generators from default value
				obj_handle.changeGenerators()

		#####################################################
		# for automating

		elif prompt.startswith("automate"):
			try:
				parameter = prompt.split(" ")[1]
			except IndexError:
				print("Command incorrectly typed. Type 'help' to get more information")
				continue
			if parameter.startswith("random"):
				# automate randomization
				obj_handle.automateRandom()
			elif parameter.startswith("normal"):
				# automate generator choosing
				obj_handle.automateGens()

if __name__ == '__main__':
	entry_point()