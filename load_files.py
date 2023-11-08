from error_messages import *
from keys import *
from file_paths import CONFIG_FILE_PATH
import json as json

class KeyMissingError(Exception):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)

def format(json_object:dict, template:dict) -> dict:
	"""
	Check if an item from a json file is of the correct format.

	Parameters:
		json_object : dict[str, ?]
			Object from a json file.
		template : dict[str, ?]
			Contains the expected keys and respective value types.

	Raises:
		KeyMissingError
			If the `json_object` does not contain all the keys in the `template`.
		ValueError
			If one of the values in `json_object` is of the wrong type.
	
	Returns:
		The `json_object` formatted according to the `template`.
	"""
	
	result = {}
	
	# Check if all required keys are present.

	if len(json_object) < len(template):
		raise KeyMissingError
	
	# Check if all values are of the correct type.

	for key, value in template.items():
		result[key] = value(json_object[key])

	return result

def parse_json_file(path:str, template:dict, is_list:bool) -> list[dict] | dict:
	"""
	Args:
		path : str
			The path of the file to be loaded and parsed.
		template : dict
			Contains the expected keys and respective value types.
		is_list : bool
			Whether the file contains a dictionary that fits the given `template` (`False`) or a list of such dictionaries (`True`)

	Returns:
		A list/dictionary containing items that fit the `template`.

	Raises:
		FileNotFoundError
			If the file at the specified `path` is not found.
		ValueError
			If some values are of the wrong type.
		KeyMissingError
			If the file does not contain all the required keys.
	"""

	# Load

	file = open(path, "r")

	if is_list:
		result = []
	else:
		result = {}

	try:
		file_contents = json.load(file)

		# Format

		if is_list:
			for item in list[dict](file_contents):
				result.append(format(item, template))
		else:
			result = format(dict(file_contents), template)

	except Exception as e:
		raise e
	else:
		return result
	finally:
		file.close()

def load_config_file() -> dict:
	"""
	Load and parse configuration file.

	Returns:
		A `dict[str, ?]` containing all the config settings, if they were each present and of the correct type.
	
	Will abend upon faulty config file.
	"""

	settings:dict = {
		S_MULTIPLE_CHOICE : bool
		,S_NUMBER_OF_QUESTIONS : int
		,S_NUMBER_OF_ATTEMPTS : int
		,S_MULTIPLE_CHOICE_USE_INDEX : bool
		,S_QUESTION_FILE_PATH : str
		,S_SCORE_FILE_PATH : str
		,S_PROGRAM_STATE_FILE_PATH : str
	}

	try:
		settings = parse_json_file(CONFIG_FILE_PATH, settings, False)
	except FileNotFoundError:
		abend(CONFIG_FILE_NOT_FOUND)
	except KeyMissingError:
		abend(SETTINGS_MISSING)
	except ValueError:
		abend(SETTINGS_WRONG_TYPE)
	else:	
		# Ensure numbers of attempts and questions are at least 1.
		settings[S_NUMBER_OF_ATTEMPTS] = max(1, settings[S_NUMBER_OF_ATTEMPTS])
		settings[S_NUMBER_OF_QUESTIONS] = max(1, settings[S_NUMBER_OF_QUESTIONS])

	return settings

def load_questions_file(file_path : str) -> list[dict]:
	"""
	Load and parse questions file.

	Parameters:
		file_path : str
			Path to the questions file.

	Returns:
		A `dict[str, ?]` object containing the loaded questions.
	
	Will abend upon faulty question file.
	"""

	question_template = {
		Q_QUESTION : str
		,Q_ANSWER : str
		,Q_ANSWER_OPTIONS : list[str]
	}

	try:
		questions:list[dict] = parse_json_file(file_path, question_template, True)
		if len(questions) == 0:
			abend(QUESTION_FILE_EMPTY)
	except FileNotFoundError:
		abend(QUESTION_FILE_NOT_FOUND)
	except KeyMissingError or ValueError:
		abend(FAULTY_QUESTIONS)
	else:
		return questions
