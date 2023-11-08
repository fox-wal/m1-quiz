from display_messages import PROGRAM_ABENDED

CONFIG_FILE_NOT_FOUND = "Config file not found."
SETTINGS_MISSING = "Some settings were missing from the config file."
SETTINGS_WRONG_TYPE = "Some settings in the config file were of the wrong type."
INVALID_CHARACTER = "Invalid character: {}"
QUESTION_FILE_NOT_FOUND = "Question file not found."
QUESTION_FILE_EMPTY = "No questions found in questions file."
FAULTY_QUESTIONS = "Question file contained faulty questions."
MULTI_CHOICE_BAD_INDEX_FORMAT = "Please enter an integer between {} and {}."
SAVE_SCORE_BAD_INPUT = "Please enter one of {}."
COULD_NOT_SAVE_SCORE = "Could not save score."
SCORES_FILE_CORRUPTED = "Scores file is corrupted."

def abend(message):
	print(PROGRAM_ABENDED, message)
	exit()
