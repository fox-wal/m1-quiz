from io import TextIOWrapper
import json as json
from random import shuffle
import datetime as dt
from error_messages import *
from display_messages import *
from keys import *
from file_paths import *

def abend(message):
	print(PROGRAM_ABENDED, message)
	exit()

# Load essential files


## Config file

settings = {
	S_MULTIPLE_CHOICE : bool
	,S_NUMBER_OF_QUESTIONS : int
	,S_NUMBER_OF_QUESTIONS : int
	,S_MULTIPLE_CHOICE_USE_INDEX : bool
	,S_QUESTION_FILE_PATH : str
	,S_SCORE_FILE_PATH : str
	,S_PROGRAM_STATE_FILE_PATH : str
}

try:
	file = open(CONFIG_FILE_PATH, "r")
except FileNotFoundError:
	abend(CONFIG_FILE_NOT_FOUND)
else:
	file_contents = json.load(file)
	file.close()

	# Check if the config file is formatted correctly.
	if len(file_contents) < len(settings):
		abend(SETTINGS_MISSING)
	for setting in file_contents.keys():
		if setting not in settings.keys():
			abend(SETTINGS_MISSING)
		try:
			# Check if the value for the current setting is of the correct type.
			value = settings[setting](file_contents[setting])
		except ValueError:
			abend(SETTINGS_WRONG_TYPE)
		else:
			settings[setting] = value
	
	print("Config file loaded correctly.")

# Ensure numbers of attempts and questions are at least 1.
settings[S_NUMBER_OF_ATTEMPTS] = max(1, settings[S_NUMBER_OF_ATTEMPTS])
settings[S_NUMBER_OF_QUESTIONS] = max(1, settings[S_NUMBER_OF_QUESTIONS])

## Question file

question_template = {
	Q_QUESTION : str
	,Q_ANSWER : str
	,Q_ANSWER_OPTIONS : list[str]
}

questions : list[dict] = []

faulty_questions = 0

try:
	file = open(settings[S_QUESTION_FILE_PATH], "r")
except FileNotFoundError:
	abend(QUESTION_FILE_NOT_FOUND)
else:
	file_contents = json.load(file)
	file.close()

	# Check if question file is formatted correctly.
	try:
		questions = file_contents[Q_QUESTIONS]
	except:
		abend(QUESTION_FILE_EMPTY)
	else:
		# Check if there are any questions.
		try:
			questions[0]
		except:
			abend(QUESTION_FILE_EMPTY)
		for q in range(len(questions)):
			# Check if the question contains all the required elements.
			for element in question_template.keys():
				if element not in questions[q].keys():
					questions.remove(questions[q])
					faulty_questions += 1
					q += 1
					break
			# Check if each element is of the correct type.
			for element in questions[q].keys():
				try:
					questions[q][element] = question_template[element](questions[q][element])
				except ValueError:
					questions.remove(questions[q])
					faulty_questions += 1
					break
	
	print(FAULTY_QUESTIONS_REMOVED, faulty_questions)
	print(NON_FAULTY_QUESTIONS, len(questions))

# Welcome

print(WELCOME)

## Get user's name

while True:
	name = input(NAME_PROMPT)
	if "\"" not in name:
		print(INVALID_CHARACTER.format("\""))
		break

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
		answer_options = questions[q][Q_ANSWER_OPTIONS].copy() + [questions[q][Q_ANSWER]]
		shuffle(answer_options)
		for o in range(len(answer_options)):
			if settings[S_MULTIPLE_CHOICE_USE_INDEX]:
				print(MULTI_CHOICE_OPTION_WITH_INDEX_LINE.format(o + 1, answer_options[o]))
			else:
				print(answer_options[o])
		
		# Prompt user to choose.
		if settings[S_MULTIPLE_CHOICE_USE_INDEX]:
			print(MULTI_CHOICE_INDEX_PROMPT)
		else:
			print(MULTI_CHOICE_ANSWER_PROMPT)

	# User enters answer.
	correct = False
	points = settings[S_NUMBER_OF_ATTEMPTS]
	max_score += points
	attempt = 1
	while not correct and (attempt <= settings[S_NUMBER_OF_ATTEMPTS]):
		if settings[S_MULTIPLE_CHOICE] and settings[S_MULTIPLE_CHOICE_USE_INDEX]:
			while True:
				try:
					choice = int(input()) - 1
					if not choice in range(len(answer_options)):
						raise ValueError
				except ValueError:
					print(MULTI_CHOICE_BAD_INDEX_FORMAT.format(1, len(answer_options)))
				else:
					break
			correct = answer_options[choice] == questions[q][Q_ANSWER]
		else:
			correct = input().lower() == questions[q]["answer"].lower()

		if not correct:
			print(INCORRECT.format(settings[S_NUMBER_OF_ATTEMPTS] - attempt))
			points -= 1

		attempt += 1
	
	if correct:
		print(CORRECT.format(points))
		score += points
		questions_correct += 1
	print(TOTAL_SCORE.format(score))

# Results

print(RESULTS.format(questions_correct, number_of_questions, score, max_score))

# Save score

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
