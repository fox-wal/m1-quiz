from io import TextIOWrapper
import json as json
from random import shuffle
import datetime as dt

def abend(message):
	print("Program abended:", message)
	exit()

# Load essential files


## Config file

CONFIG_FILE_PATH = "config.json"

settings = {
	"multiple choice" : bool
	,"number of questions" : int
	,"number of attempts" : int
	,"multi-choice: select using index" : bool
}

try:
	file = open(CONFIG_FILE_PATH, "r")
except FileNotFoundError:
	abend("Config file not found.")
else:
	file_contents = json.load(file)
	file.close()

	# Check if the config file is formatted correctly.
	if len(file_contents) < len(settings):
		abend("Some settings were missing from the config file.")
	for setting in file_contents.keys():
		if setting not in settings.keys():
			abend("Some settings were missing from the config file.")
		try:
			# Check if the value for the current setting is of the correct type.
			value = settings[setting](file_contents[setting])
		except ValueError:
			abend("Some settings in the config file were of the wrong type.")
		else:
			settings[setting] = value
	
	print("Config file loaded correctly.")

# Ensure numbers of attempts and questions are at least 1.
settings["number of attempts"] = max(1, settings["number of attempts"])
settings["number of questions"] = max(1, settings["number of questions"])

## Question file

QUESTION_FILE_PATH = "questions.json"

question_template = {
	"question" : str
	,"answer" : str
	,"multi-choice options" : list[str]
}

questions : list[dict] = []

faulty_questions = 0

try:
	file = open(QUESTION_FILE_PATH, "r")
except FileNotFoundError:
	abend("Question file not found.")
else:
	file_contents = json.load(file)
	file.close()

	# Check if question file is formatted correctly.
	try:
		questions = file_contents["questions"]
	except:
		abend("No questions found in questions file.")
	else:
		# Check if there are any questions.
		try:
			questions[0]
		except:
			abend("No questions found in questions file.")
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
	
	print("Faulty questions (removed):", faulty_questions)
	print("Good questions:", len(questions))

# Welcome

print("""
	                    -----+-----
	  
                      Welcome to the
	
	 QQQQQQQQQQ  UUUU    UUUU IIIIIIIIIIII ZZZZZZZZZZZZ
	QQQQQQQQQQQQ UUUU    UUUU IIIIIIIIIIII ZZZZZZZZZZZZ
	QQQQ    QQQQ UUUU    UUUU     IIII            ZZZZ
	QQQQ    QQQQ UUUU    UUUU     IIII          ZZZZ
	QQQQ Q  QQQQ UUUU    UUUU     IIII        ZZZZ
	QQQQ  Q QQQQ UUUU    UUUU     IIII      ZZZZ
	QQQQQQQQQQQ  UUUUUUUUUUUU IIIIIIIIIIII ZZZZZZZZZZZZ
	 QQQQQQQQ QQ  UUUUUUUUUU  IIIIIIIIIIII ZZZZZZZZZZZZ
	
	  					-----+-----
""")

## Get user's name

while True:
	name = input("Name: ")
	if "\"" not in name:
		print("Invalid character: {}".format("\""))
		break

# Start Quiz
max_score = 0
score = 0
questions_correct = 0
number_of_questions = min(len(questions), settings["number of questions"])
for q in range(number_of_questions):

	# Print question.
	print("\nQuestion {} of {}: {}\n".format(q + 1, number_of_questions, questions[q]))
	
	# Print answer options.
	if settings["multiple choice"]:
		# Ensure number of attempts does not exceed the number of options - 1.
		settings["number of attempts"] = min(settings["number of attempts"], len(questions[q]["multi-choice options"]) - 1)
		answer_options = questions[q]["multi-choice options"].copy() + [questions[q]["answer"]]
		shuffle(answer_options)
		for o in range(len(answer_options)):
			if settings["multi-choice: select using index"]:
				print("{}. {}".format(o + 1, answer_options[o]))
			else:
				print(answer_options[o])
		
		# Prompt user to choose.
		if settings["multi-choice: select using index"]:
			print("\nEnter the index of the correct answer: ")
		else:
			print("\nEnter the correct answer: ")

	# User enters answer.
	correct = False
	points = settings["number of attempts"]
	max_score += points
	attempt = 1
	while not correct and (attempt <= settings["number of attempts"]):
		if settings["multiple choice"] and settings["multi-choice: select using index"]:
			try:
				choice = int(input()) - 1
				if not ((choice >= 1) and (choice <= len(answer_options))):
					raise ValueError
			except ValueError:
				print("Please enter an integer between {} and {}.".format(1, len(answer_options)))
			else:
				correct = answer_options[choice] == questions[q]["answer"]
		else:
			correct = input().lower() == questions[q]["answer"].lower()

		if not correct:
			print("Incorrect. {} attempts remaining.".format(settings["number of attempts"] - attempt))
			points -= 1

		attempt += 1
	
	if correct:
		print("Correct! [+{}]".format(points))
		score += points
		questions_correct += 1
	else:
		print("Incorrect.")
	print("Total score: {}", score)

# Results

print("""
+---------------End of Quiz---------------+

Questions answered correctly: {} out of {}.
Score: {} out of {}.

+-----------------------------------------+
""".format(questions_correct, number_of_questions, score, max_score))

# Save score

## Ask if user wants to save it.

options = ["Y", "N"]
print("Would you like to save your score? [{}]".format("/".join(options)))

while True:
	choice = input().upper()
	if choice not in options:
		print("Please enter one of {}.".format(" or ".join(options)))
	else:
		break

if choice == "Y":
	time_stamp = "{:%Y-%m-%d %H:%M:%S%z}".format(dt.datetime.now())
	adjusted_score = 100 * (score / max_score)
	scores : dict[str, dict[str, object]] = {}

	# Load score file.

	SCORE_FILE_PATH = "scores.json"

	try:
		file = open(SCORE_FILE_PATH, "r+")
	except FileNotFoundError:
		print("Score file created.")
	else:
		try:
			file_contents = json.load(file)
		except:
			print("Could not save score: scores file is corrupted.")
		else:

			# Write to score file.

			try:
				scores.update(dict[str, dict[str, object]](file_contents))
			except:
				print("Could not save score. File_contents invalid format?")
			else:
				if name in scores.keys():
					scores[name][time_stamp] = adjusted_score
				else:
					scores[name] = {time_stamp : adjusted_score}
				print("Score saved!")
		finally:
			file.close()
	finally:
		file = open(SCORE_FILE_PATH, "w")
		json.dump(scores, file)
		file.close()


print("Goodbye!")

PROGRAM_STATE_FILE_PATH = "program_state.json"
