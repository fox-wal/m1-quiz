import json as json
from random import shuffle
import datetime as dt
from error_messages import *
from display_messages import *
from keys import *
from load_files import *

def print_answer_options(question:dict, select_using_index:bool):
	"""
	Print the answer options for a multiple-choice question.
	"""

	answer_options = question[Q_ANSWER_OPTIONS].copy() + [question[Q_ANSWER]]
	shuffle(answer_options)

	for o in range(len(answer_options)):
		if select_using_index:
			print(MULTI_CHOICE_OPTION_WITH_INDEX_LINE.format(o + 1, answer_options[o]))
		else:
			print(answer_options[o])

	# Prompt user to choose.
	if select_using_index:
		print(MULTI_CHOICE_INDEX_PROMPT)
	else:
		print(TYPE_IN_ANSWER_PROMPT)

def get_answer_results(points:int, multiple_choice:bool, select_using_index:bool, max_attempts:int, answer_options:list[str] = []) -> tuple[int, bool]:
	"""
	User types in/selects an answer.

	Parameters:
		points : int
			The max number of points for this question.
		multiple_choice : bool
			Whether or not the question is a multiple-choice question.
		select_using_index : bool
			[For multiple-choice questions] Whether the user should select the option by typing it in or by entering an index.
		max_attempts : int
			Maximum number of attempts for this question.
		answer_options : list[str]
			[For multiple-choice questions] All the answer options (including the correct one).

	Returns:
		`tuple[int, bool]`
			The `int` is the number of points the user earned for this question.
			The `bool` is whether or not the user entered the correct answer.
	"""

	attempt = 1
	correct = False

	while not correct and (attempt <= max_attempts):

		# Select answer using index (multiple choice only).

		if multiple_choice and select_using_index:
			while True:
				try:
					choice = int(input()) - 1
					if not choice in range(len(answer_options)):
						raise ValueError
				except ValueError:
					print(ENTER_INDEX_IN_CORRECT_RANGE_PROMPT.format(1, len(answer_options)))
				else:
					break
			correct = answer_options[choice] == questions[q][Q_ANSWER]

		# Type in answer

		else:
			print(TYPE_IN_ANSWER_PROMPT)
			correct = input().lower() == questions[q][Q_ANSWER].lower()

		# Calculate points + attempts.

		if not correct:
			print(INCORRECT.format(max_attempts - attempt))
		points -= 1
		attempt += 1

	return (points, correct)

def get_user_name() -> str:
	"""
	Returns:
		User name.
	"""
	while True:
		name = input(NAME_PROMPT)
		if "\"" in name:
			print(INVALID_CHARACTER.format("\""))
		else:
			return name

# Load essential files

settings = load_config_file()
questions = load_questions_file(settings[S_QUESTION_FILE_PATH])

# Welcome

print(WELCOME)
name = get_user_name()

# Start Quiz
max_score = 0
score = 0
questions_correct = 0
number_of_questions = min(len(questions), settings[S_NUMBER_OF_QUESTIONS])
for q in range(number_of_questions):

	# Print question.
	print(QUESTION_LINE.format(q + 1, number_of_questions, questions[q][Q_QUESTION]))
	
	# Print answer options.
	if settings[S_MULTIPLE_CHOICE]:
		# Ensure number of attempts does not exceed the number of incorrect answer options.
		settings[S_NUMBER_OF_ATTEMPTS] = min(settings[S_NUMBER_OF_ATTEMPTS], len(questions[q][Q_ANSWER_OPTIONS]))
		print_answer_options(questions[q], settings[S_MULTIPLE_CHOICE_USE_INDEX])

	# User enters answer.
	points = settings[S_NUMBER_OF_ATTEMPTS]
	max_score += points

	points, correct = get_answer_results(points, settings[S_MULTIPLE_CHOICE], settings[S_MULTIPLE_CHOICE_USE_INDEX], settings[S_NUMBER_OF_ATTEMPTS], questions[q][Q_ANSWER_OPTIONS])

	# Process answer results.

	if correct:
		print(CORRECT.format(points))
		score += points
	
	print(SCORE_SO_FAR.format(score))

# Quiz Results

print(RESULTS.format(questions_correct, number_of_questions, score, max_score))

# Save Score

## Ask if user wants to save it.

options = ["Y", "N"]
print(SAVE_SCORE_PROMPT.format("/".join(options)))

while True:
	choice = input().upper()
	if choice not in options:
		print(SAVE_SCORE_BAD_INPUT.format(" or ".join(options)))
	else:
		break

if choice == "Y":
	time_stamp = TIME_STAMP_FORMAT.format(dt.datetime.now())
	adjusted_score = int(100 * (score / max_score))
	scores : dict[str, dict[str, object]] = {}

	# Load score file.

	try:
		file = open(settings[S_SCORE_FILE_PATH], "r+")
	except FileNotFoundError:
		print(SCORE_FILE_CREATED)
	else:
		try:
			file_contents = json.load(file)
		except:
			print(COULD_NOT_SAVE_SCORE, SCORES_FILE_CORRUPTED)
		else:

			# Write to score file.

			try:
				scores.update(dict[str, dict[str, object]](file_contents))
			except:
				print(COULD_NOT_SAVE_SCORE, SCORES_FILE_CORRUPTED)
			else:
				if name in scores.keys():
					scores[name][time_stamp] = adjusted_score
				else:
					scores[name] = {time_stamp : adjusted_score}
				print(SCORE_SAVED)
		finally:
			file.close()
	finally:
		file = open(settings[S_SCORE_FILE_PATH], "w")
		json.dump(scores, file)
		file.close()

print(GOODBYE)
