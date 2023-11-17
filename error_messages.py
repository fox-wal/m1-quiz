from display import DisplayText

INVALID_CHARACTER = "Invalid character: {}"
ENTER_INDEX_IN_CORRECT_RANGE_PROMPT = "Please enter an integer between {} and {}."
ENTER_ONE_OF_PROMPT = "Please enter one of {}."

# Config file

CONFIG_FILE_NOT_FOUND = "Config file not found."
SETTINGS_MISSING = "Some settings were missing from the config file."
SETTINGS_WRONG_TYPE = "Some settings in the config file were of the wrong type."

# Question file

QUESTION_FILE_NOT_FOUND = "Question file not found."
QUESTION_FILE_EMPTY = "No questions found in questions file."
FAULTY_QUESTIONS = "Question file contained faulty questions."

# Score file

COULD_NOT_SAVE_SCORE = "Could not save score."
SCORES_FILE_CORRUPTED = "Scores file is corrupted."
NO_SCORES_FOR_USER = "No scores found for user \"{}\"."

def abend(message):
	print(DisplayText.PROGRAM_ABENDED, message)
	exit()
