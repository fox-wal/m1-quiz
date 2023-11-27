from random import shuffle
import datetime as dt
from error_handling import *
from display_text import DisplayText
from prompts import Prompts
from load_files import *
from config import Config
from question import Question
from results import Results

def sort_dict(dictionary:dict) -> dict:
    '''
    Sort items in a `dictionary` in descending order according to its values.

    Parameters:
        dictionary : dict
            The dictionary to sort.
    
    Returns:
        The sorted dictionary.
    '''
    as_list = []
    sorted_dict = {}
    for key, value in dictionary.items():
        as_list.append((key, value))
    as_list.sort(key=lambda item: item[1], reverse=True)
    for i in as_list:
        sorted_dict[i[0]] = i[1]
    return sorted_dict

def sort_scores(scores:dict[str, int]) -> dict[str, int]:
    '''
    Sort a scores dictionary according to the scores in descending order.

    Parameters:
        scores : dict[str, int]
            The scores to sort.
    
    Returns:
        The sorted `scores`.
    '''
    return sort_dict(scores)

def print_scores(name:str, scores:dict[str, dict[str, int]]):
    '''
    Display the timestamps and scores saved under the specified `name` in order of score (descending).

    Parameters:
        name : str
            Scores saved under this name will be displayed.
        scores: dict[str, dict[str, int]]
            All the saved scores.
    '''
    if name not in scores:
        print(DisplayText.NO_SCORES_FOR_USER.format(name))
        return
    print(DisplayText.SCORE_TABLE_HEADER)
    for time_stamp, score in sort_scores(scores[name]).items():
        print(DisplayText.SCORE_TABLE_ROW.format(time_stamp[:-3], score))

def print_answer_options(answer_options:list[str], select_using_index:bool):
    '''
    Print the answer options for a multiple-choice question.

    Parameters:
        answer_options : list[str]
            All the answer options (including correct) for the question.
        select_using_index : bool
            If True: the user must enter the index of the answer they think is correct.
            If False: the user must enter the answer they think is correct.
    '''

    for o in range(len(answer_options)):
        if select_using_index:
            print(DisplayText.INDEXED_ANSWER_OPTION.format(o + 1, answer_options[o]))
        else:
            print(DisplayText.ANSWER_OPTION.format(answer_options[o]))

    # Prompt user to choose.
    
    if select_using_index:
        print(Prompts.ANSWER_BY_INDEX)
    else:
        print(Prompts.ANSWER_TYPED)

def select_answer_using_index(question:Question) -> bool:
    while True:
        try:
            choice = int(input()) - 1
            if choice not in range(len(question.get_answer_options)):
                raise ValueError
        except ValueError:
            print(Prompts.VALID_INDEX.format(1, len(question.get_answer_options)))
        else:
            return question.get_answer_options[choice] == question.get_answer

def type_answer(question:Question) -> bool:
    answer = input(Prompts.ANSWER_TYPED + "\n")
    return answer.lower() == question.get_answer.lower()

def get_answer(points:int, multiple_choice:bool, select_using_index:bool, max_attempts:int, question:Question) -> tuple[int, bool]:
    '''
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
        answer : str
            The correct answer to this question.
        answer_options : list[str]
            [For multiple-choice questions] All the answer options (including the correct one).

    Returns:
        `tuple[int, bool]`
            The `int` is the number of points the user earned for this question.
            The `bool` is whether or not the user entered the correct answer.
    '''

    attempt = 1
    correct = False

    while not correct and (attempt <= max_attempts):

        if multiple_choice and select_using_index:
            correct = select_answer_using_index(question)
        else:
            correct = type_answer(question)

        if not correct:
            print(DisplayText.INCORRECT.format(max_attempts - attempt))
            points -= 1

        attempt += 1

    return points, correct

def get_user_name() -> str:
    '''
    Prompt the user to enter a valid name until they do so.

    Returns:
        Valid user name.
    '''
    while True:
        name = input(Prompts.NAME)
        if '"' in name:
            print(DisplayText.INVALID_CHARACTER.format('"'))
        else:
            return name

def yes_or_no(prompt:str) -> bool:
    '''
    Prompt the user to enter either yes or no.

    Parameters:
        prompt : str
            The prompt to display to the user.

    Returns:
        True if the user selects "yes".
        False if the user selects "no".
    '''

    YES = 'Y'
    NO = 'N'

    print(prompt, Prompts.YES_OR_NO)

    while True:
        choice = input().upper()

        if choice == YES:
            return True
        elif choice == NO:
            return False
        else:
            print(Prompts.YES_OR_NO)

#

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

    return settings, questions

def do_question(question:Question, results:Results):

    attempts = settings.get_number_of_attempts

    if settings.get_multiple_choice:
        shuffle(question.get_answer_options)
        # Ensure number of attempts does not exceed the number of incorrect answer options.
        attempts = min(settings.get_number_of_attempts, len(question.get_answer_options) - 1)
        print_answer_options(question.get_answer_options, settings.get_select_using_index)

    results.increase_max_score_by(attempts)

    points, correct = get_answer(attempts, settings.get_multiple_choice, settings.get_select_using_index, attempts, question)

    if correct:
        print(DisplayText.CORRECT.format(points))
        results.increase_score_by(points)
        results.increment_questions_correct()

    print(DisplayText.CURRENT_SCORE.format(results.get_score))

def do_quiz(settings:Config, questions:list[Question]) -> Results:
    results = Results()
    for q in range(number_of_questions):
        print(DisplayText.QUESTION.format(q + 1, number_of_questions, questions[q].get_question))
        do_question(questions[q], results)

    return results

def save_score_to_file(user_name:str, scores:dict[str, dict[str, int]], score:int, time_stamp:str):
    if user_name in scores.keys():
        scores[user_name][time_stamp] = score
    else:
        scores[user_name] = {time_stamp : score}
    save_score_file(settings.get_score_file_path, scores)
    print(DisplayText.SCORE_SAVED)

def load_scores(settings:Config) -> dict[str, dict[str, int]]:
    try:
        return load_score_file(settings.get_score_file_path)
    except FileNotFoundError:
        # It doesn't matter if the file does not exist yet: it will be created next time the score is saved.
        return {}

def save_score(name:str, scores, score_file_corrupted:bool):
    time_stamp = DisplayText.TIME_STAMP.format(dt.datetime.now())

    if score_file_corrupted:
        print(ErrorMessages.FILE_CORRUPTED.format(settings.get_score_file_path))
        overwrite_corrupted_score_file = yes_or_no(Prompts.SAVE_SCORE + Prompts.OVERWRITE_CORRUPTED_SCORES)
        if overwrite_corrupted_score_file:
            save_score_to_file(name, scores, results.get_adjusted_score, time_stamp)
    else:
        save_score_to_file(name, scores, results.get_adjusted_score, time_stamp)

#---------------#
# PROGRAM START #
#---------------#

settings, questions = load_essential_files()

print(DisplayText.WELCOME)
name = get_user_name()

# Ensure number of questions doesn't exceed number of available questions.
number_of_questions = min(len(questions), settings.get_number_of_questions)

results = do_quiz(settings, questions)

print(DisplayText.RESULTS.format(results.get_questions_correct, number_of_questions, results.get_score, results.get_max_score, results.get_adjusted_score))

score_file_corrupted = False
try:
    scores = load_scores(settings)
except ValueError:
    score_file_corrupted = True
    scores = {}

save = yes_or_no(Prompts.SAVE_SCORE)
if save:
    save_score(name, scores, score_file_corrupted)

view_scores = yes_or_no(Prompts.VIEW_SCORES)
if view_scores:
    print_scores(name, scores)

print(DisplayText.GOODBYE)
