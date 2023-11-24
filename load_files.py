from error_handling import *
import json as json

class KeyMissingError(Exception):
    '''
    An exception to be raised when an essential key is missing from a dictionary.
    '''
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def format(json_object:dict, template:dict) -> dict:
    '''
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
    '''
    
    result = {}
    
    # Check if all required keys are present.

    if len(json_object) < len(template):
        raise KeyMissingError
    
    # Check if all values are of the correct type.

    for key, value in template.items():
        result[key] = value(json_object[key])

    return result

def parse_json_file(path:str, template:dict, is_list:bool) -> list[dict] | dict:
    '''
    Parameters:
        path : str
            The path of the file to be loaded and parsed.
        template : dict
            Contains the expected keys and respective value types.
        is_list : bool
            Whether the file contains a dictionary that fits the given `template` (`False`) or a list of such dictionaries (`True`)

    Raises:
        FileNotFoundError
            If the file at the specified `path` is not found.
        ValueError
            If some values are of the wrong type.
        KeyMissingError
            If the file does not contain all the required keys.

    Returns:
        A list/dictionary containing items that fit the `template`.
    '''

    # Load

    file = open(path, 'r')

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

    # Close file

    except Exception as e:
        raise e
    else:
        return result
    finally:
        file.close()

def load_config_file(file_path:str) -> dict:
    '''
    Load and parse configuration file.
    
    Will abend upon faulty config file.

    Parameters:
        file_path : str
            Path to the configuration file.

    Returns:
        A `dict[str, ?]` containing all the config settings, if they were each present and of the correct type.
    '''

    # Template

    settings:dict = {
        S_MULTIPLE_CHOICE : bool
        ,S_NUMBER_OF_QUESTIONS : int
        ,S_NUMBER_OF_ATTEMPTS : int
        ,S_MULTIPLE_CHOICE_USE_INDEX : bool
        ,S_QUESTION_FILE_PATH : str
        ,S_SCORE_FILE_PATH : str
    }

    # Try to parse.

    try:
        settings = parse_json_file(file_path, settings, False)
    except FileNotFoundError:
        abend(ErrorMessages.FILE_NOT_FOUND.format(file_path))
    except KeyMissingError:
        abend(ErrorMessages.FILE_INCOMPLETE.format(file_path))
    except ValueError:
        abend(ErrorMessages.FILE_CORRUPTED.format(file_path))
    else:    
        # Ensure numbers of attempts and questions are at least 1.
        settings[S_NUMBER_OF_ATTEMPTS] = max(1, settings[S_NUMBER_OF_ATTEMPTS])
        settings[S_NUMBER_OF_QUESTIONS] = max(1, settings[S_NUMBER_OF_QUESTIONS])

    return settings

def load_questions_file(file_path:str) -> list[dict]:
    '''
    Load and parse questions file.
    
    Will abend upon faulty question file.

    Parameters:
        file_path : str
            Path to the questions file.

    Returns:
        A `list[dict[str, ?]]` containing the loaded questions.
    '''

    # Template

    question_template = {
        Q_QUESTION : str
        ,Q_ANSWER : str
        ,Q_ANSWER_OPTIONS : list[str]
    }

    # Try to parse

    try:
        questions:list[dict] = parse_json_file(file_path, question_template, True)
        if len(questions) == 0:
            abend(ErrorMessages.FILE_INCOMPLETE.format(file_path))
    except FileNotFoundError:
        abend(ErrorMessages.FILE_NOT_FOUND.format(file_path))
    except KeyMissingError or ValueError:
        abend(ErrorMessages.FILE_CORRUPTED.format(file_path))
    else:
        return questions

def load_score_file(file_path:str) -> dict[str, dict[str, int]]:
    '''
    Load and parse score file.

    Parameters:
        file_path : str
            The path to the score file.

    Raises:
        FileNotFoundError
        ValueError
            If the scores file is formatted incorrectly.
    '''
    file = open(file_path, 'r')
    try:
        contents = dict[str, dict[str, int]](json.load(file))
    finally:
        file.close()

    DATE_TIME_SEPARATOR = ' '
    DATE_SEPARATOR = '-'
    TIME_SEPARATOR = ':'
    DATE_COMPONENTS = 3
    TIME_COMPONENTS = 3

    for score_dict in contents.values():
        for time_stamp, score in score_dict.items():
            date, time = tuple(time_stamp.split(DATE_TIME_SEPARATOR))
            split_date, split_time = date.split(DATE_SEPARATOR), time.split(TIME_SEPARATOR)
            if len(split_date) != DATE_COMPONENTS or len(split_time) != TIME_COMPONENTS:
                raise ValueError
            [int(i) for i in split_date]
            [int(i) for i in split_time]
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
