# IPND Stage 2 Final Project

# You've built a Mad-Libs game with some help from Sean.
# Now you'll work on your own game to practice your skills and demonstrate what you've learned.

# For this project, you'll be building a Fill-in-the-Blanks quiz.
# Your quiz will prompt a user with a paragraph containing several blanks.
# The user should then be asked to fill in each blank appropriately to complete the paragraph.
# This can be used as a study tool to help you remember important vocabulary!

text_easy='''Hello __1__!'  In __2__ this is particularly easy; all you have to do
is type in:
__3__ "Hello __1__!"
Of course, that isn't a very useful thing to do. However, it is an
example of how to output to the user using the __3__ command, and
produces a program which does something, so it is useful in that capacity.

It may seem a bit odd to do something in a Turing complete language that
can be done even more easily with an __4__ file in a browser, but it's
a step in learning __2__ syntax, and that's really its purpose.'''

text_medium = '''A __1__ is created with the def keyword.  You specify the inputs a
__1__ takes by adding __2__ separated by commas between the parentheses.
__1__s by default returns __3__ if you don't specify the value to retrun.
__2__ can be standard data types such as string, integer, dictionary, tuple,
and __4__ or can be more complicated such as objects and lambda functions.'''

text_hard = '''When you create a __1__, certain __2__s are automatically
generated for you if you don't make them manually. These contain multiple
underscores before and after the word defining them.  When you write
a __1__, you almost always include at least the __3__ __2__, defining
variables for when __4__s of the __1__ get made.  Additionally, you generally
want to create a __5__ __2__, which will allow a string representation
of the method to be viewed by other developers.

You can also create binary operators, like __6__ and __7__, which
allow + and - to be used by __4__s of the __1__.  Similarly, __8__,
__9__, and __10__ allow __4__s of the __1__ to be compared
(with <, >, and ==).'''

blanks_easy     = ['__1__','__2__','__3__','__4__']
blanks_medium   = ['__1__','__2__','__3__','__4__']
blanks_hard 	= ['__1__','__2__','__3__','__4__','__5__','__6__','__7__','__8__','__9__','__10__']

answers_easy =[ "world", "Python", "print", "html"]
answers_medium =[ "function", "arguments", "None", "lists" ]
answers_hard =[ "class", "method", "init_", "instance", "repr", "add", "sub", "less than", "greater than", "equals"]

# Variables to store the position on the nested list for the different data for the quiz
# Used to avoid magic numbers in the code

index_text      = 0	# Stores the text for the quiz
index_blanks    = 1 # Stores the blanks for the quiz
index_solutions = 2 # Stores the solutions for the quiz

''' 
Function:  get_attempts

Function that asks the user the number of attempts to use
for solving the quiz. Assumption is that the input value is an integer value

Input:
Output: Value representing the number of attempts available to solve the quiz
'''
def get_attempts():

	message = "\nPlease select the number of attempts to solve the quiz: "

	error_message = '''\nThat's not a valid answer! Integer value mandatory\n'''

	attempts = raw_input(message)

	try:
		num_attempts = int(attempts)
	except ValueError:
		print "\nThis is not a valid answer. Execute the program again!\n"
		return 0

	print "You will get " + attempts + " guesses per problem\n"

	return num_attempts
''' 
Function:  set_dificulty

Function that asks the user the difficulty level for the quiz.

Input:
	quiz --> Variable (nested list) that stores the data for the quiz depending on the difficulty 
				(text[0], blanks[1] and correct answers[2])
Output: String representing the dificulty level selected by user (easy, medium or hard)
'''
def get_difficulty(quiz):

	options = ['easy','medium','hard']
	message = '''Please select a game difficulty by typing it in!
Possible choices are: easy, medium, and hard.\n'''
	error_message = '''\nThat's not an option!\n'''

	input = raw_input(message)

	# Infinit loop until the user enters a valid option
	while input not in options:
		print(error_message)
		input = raw_input(message)

	print("\nYou've chosen " + input + "!\n")

	return input

''' 
Function:  set_quizData

This function fullfil the quiz variable with all the data depending on the
difficulty level. A nested list variable is used to store all data for the quiz

Input:
	difficulty --> Parameter that stores the difficulty level selected by the user
	quiz --> Parameter (nested list) that will store the data for the quiz depending on the difficulty 
Output: 
'''
def set_quizData(difficulty,quiz):
	
	# Based on the difficulty selected by the user, the list containing all data for the quiz is set
	if difficulty == "easy":
		quiz.append(text_easy)
		quiz.append(blanks_easy)
		quiz.append(answers_easy)
	else:
		if difficulty == "medium":
			quiz.append(text_medium)
			quiz.append(blanks_medium)
			quiz.append(answers_medium)
		else:
			quiz.append(text_hard)
			quiz.append(blanks_hard)
			quiz.append(answers_hard)

''' 
Function:  process_input

This function search for the first "blank" on the quiz that is still pending and asks the user for it.
It checks the correctness and return True or False

Input:
	quiz --> Variable (nested list) that stores the data for the quiz depending on the difficulty 
				(text[0], blanks[1] and correct answers[2])
	correct --> list of blank ids already answered correctly by the user
Output: 
	Boolean -> Depending if the answers from the user is correct or not
'''
def process_input(quiz,correct):

	index = 0
	correct_answer = ''

	# Go through all the blanks from the quiz until we found the first one that is still without a correct answer
	while index < len(quiz[index_blanks]):
		# The "blank" that is not in the "correct" parameter is the one to ask to the user
		if quiz[index_blanks][index] not in correct:  
			part_to_ask = quiz[index_blanks][index]
			correct_answer = quiz[index_solutions][index]
			break
		index += 1

	# Before asking the user for the answer, the system shows the quiz text to solve
	print show_quiz_text(quiz,correct)

	# User input
	user_input = raw_input("\nWhat should be substituted in for " + part_to_ask + "? ")

	# Check if the answer is correct. If so, the "blank" solved is added to the list of already answered by the user
	if user_input != correct_answer:
		return False
	else:
		correct.append(part_to_ask)
		print "Correct answer!\n"

	return True

''' 
Function:  show_quiz_text

Generates the text with the quiz to show to the user. It keeps only the blank spaces not answered by the user, 
the correct ones are shown with the replacement.
The generated text is stored in the same quiz variable, position [0] of the variable.

Input:
	quiz --> Variable (nested list) that stores the data for the quiz depending on the difficulty 
				(text[0], blanks[1] and correct answers[2])
	correct --> list of blank ids already answered correctly by the user
Output:

'''
def show_quiz_text(quiz,correct):
	
	index = 0
	while index < len(correct):
		quiz[index_text] = quiz[index_text].replace(correct[index],quiz[index_solutions][index])
		index += 1

	return quiz[index_text]

''' 
Function:  message_fail

Generates the output message when user fails the attempt to solve one word.

Input:
	attempts_left --> number of attempts remaining
Output: 
	message --> Output message to show
'''
def message_fail(attempts_left):

	message = ''

	if attempts_left > 0:
		if attempts_left == 1:
			message = "\nThat isn't the correct answer! You only have 1 try left! Make it count!\n"
		else:
			message = "\nThat isn't the correct answer! Let's try again; you have " + str(attempts_left) + " trys left!\n"

	return message
''' 
Function:  game_play

Main program for the game play. It sets the difficulty level and process all the attempts
to solve the quiz. Shows a message when finished.

Input: 
Output: 
'''
def game_play():
	
	quiz_correct = [] # List with correct answers from user (containing blank ids)
	quiz		 = [] # List variable to store the quiz data depending on the difficulty
					  # quiz[0] - text, quiz[1] - blanks on text, quiz[2] - correct answers from quiz

	guess_num 		 = 0 #Current attempt

	guess_attempts = get_attempts()	  # Ask user max wrong guesses to solve the quiz
	
	if guess_attempts > 0:
		# Ask user difficulty level
		difficulty = get_difficulty(quiz)

		# Sets the quiz data based on the difficulty
		set_quizData(difficulty,quiz)

		# Main loop: attemps to solve quiz
		while guess_num < guess_attempts and len(quiz_correct) != len(quiz[index_blanks]):

			#process new input from user. If it's correct we don't count as an attempt used
			correct = process_input(quiz,quiz_correct)

			if not correct:			
				guess_num += 1
				print message_fail(guess_attempts - guess_num)  # Print output messages if failed

		#Final result for the quiz
		if len(quiz_correct) == len(quiz[index_blanks]):
			print "Quiz completed! Congratulations!\n"
			print show_quiz_text(quiz,quiz_correct)
		else:
			print "You've failed too many straight guesses! Game over!"
	else:
		print "No attempts, no quiz! ;-)"

# Execute game play
game_play()
