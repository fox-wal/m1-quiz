import json
import os
import re as regex

from error_handling import *
from question import Question
from config import Config
from display_text import DisplayText
from prompts import Prompts

class KeyMissingError(Exception):
    '''
    An exception to be raised when an essential key is missing from a dictionary.
    '''
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def load_file(file_path:str) -> str:
    '''
    Load a file.

    Will abend if the file is not found.

    Parameters:
        file_path : str
            The path to the file to load.

    Returns:
        The file contents as a string where each line is separated by an empty string.
    '''

    try:
        file = open(file_path, 'r')
    except FileNotFoundError:
        abend(ErrorMessages.FILE_NOT_FOUND.format(os.path.abspath(file_path)))
    else:
        return ''.join(file.readlines())
    finally:
        file.close()

def load_config_file(file_path:str) -> Config:
    '''
    Load and parse configuration file.

    Will abend if the config file is:

    - Not found
    - Empty
    - Corrupted

    Parameters:
        file_path : str
            Path to the configuration file.

    Returns:
        A new, populated instance of `Config` containing all the config settings, if they were all present and of the correct type.
    '''

    file_contents = load_file(file_path)

    try:
        settings = Config(*tuple(json.loads(file_contents).values()))
    except TypeError:
        abend(ErrorMessages.FILE_INCOMPLETE.format(os.path.abspath(file_path)))
    except ValueError:
        abend(ErrorMessages.FILE_CORRUPTED.format(os.path.abspath(file_path)))
    else:
        return settings

    abend("Unhandled exception.") # DEBUG

def load_questions_file(file_path:str) -> list[Question]:
    '''
    Load and parse questions file.

    Will abend if the config file is:

    - Not found
    - Empty
    - Corrupted

    Parameters:
        file_path : str
            Path to the questions file.

    Returns:
        A `list[Question]` containing the loaded questions.
    '''

    file_contents = load_file(file_path)

    questions:list[Question] = []

    try:
        for question in list(json.loads(file_contents)):
            questions.append(Question(*question.values()))

        if len(questions) == 0:
            abend(ErrorMessages.FILE_INCOMPLETE.format(os.path.abspath(file_path)))

    except KeyMissingError | ValueError:
        abend(ErrorMessages.FILE_CORRUPTED.format(os.path.abspath(file_path)))
    else:
        return questions

def load_data_class(file_path:str, the_class):
    '''
    Load values into a non-instance class of constants.

    Will abend upon a non-existent, empty, or corrupted file at the specified path.

    Parameters:
        file_path : str
            The path to the file containing the values for `the_class`.
        the_class : class
            The class to load the values into. It must have a `set_values` method.
    '''
    file_contents = load_file(file_path)

    try:
        values = json.loads(file_contents)
    except ValueError:
        abend(ErrorMessages.FILE_CORRUPTED.format(os.path.abspath(file_path)))

    try:
        the_class.set_values(the_class, *values.values())
    except IndexError:
        abend(ErrorMessages.FILE_INCOMPLETE.format(os.path.abspath(file_path)))

def load_score_file(file_path:str) -> dict[str, dict[str, int]]:
    '''
    Load and parse score file.

    Parameters:
        file_path : str
            The path to the score file.

    Raises:
        ValueError
            If the scores file is formatted incorrectly.

    Returns:
        The correctly loaded score dictionary, or an empty dictionary if the score file was not found.
    '''
    
    file = open(file_path, 'r')
    try:
        contents = dict[str, dict[str, int]](json.load(file))
    except FileNotFoundError:
        # It doesn't matter if the file does not exist yet: it will be created next time the score is saved.
        return {}

    finally:
        file.close()

    TIME_STAMP_PATTERN = r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}"
    pattern = regex.compile(TIME_STAMP_PATTERN)

    for score_dict in contents.values():
        for time_stamp, score in score_dict.items():
            if pattern.match(time_stamp) is None:
                raise ValueError
            if score not in range(0, 101):
                raise ValueError

    return contents

def save_score_file(file_path : str, scores:dict[str, dict[str, int]]):
    '''
    Save `scores` to the score file. Overwrites curent file contents.

    Parameters:
        file_path : str
            Path to the score file.
        scores : dict[str, dict[str, int]]
            The scores to save tp the file.
    '''
    file = open(file_path, 'w')
    try:
        json.dump(scores, file)
    finally:
        file.close()

def load_essential_files() -> tuple[Config, list[Question]]:
    '''
    Load essential files and dataclasses.

    Will abend if the files can't be loaded properly.

    Returns:
        A tuple containing the loaded settings and questions.
    '''

    CONFIG_FILE_PATH = "data/config.json"

    settings:Config = load_config_file(CONFIG_FILE_PATH)
    questions:list[Question] = load_questions_file(settings.get_question_file_path)
    load_data_class(settings.get_display_text_file_path, DisplayText)
    load_data_class(settings.get_prompt_file_path, Prompts)

    # Ensure number of questions doesn't exceed number of available questions.
    settings.set_number_of_questions = min(len(questions), settings.get_number_of_questions)

    return settings, questions
