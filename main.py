# Standard Library
import datetime
from random import shuffle

# Modules
import load_files
from error_handling import *

# Classes
from display_text import DisplayText
from prompts import Prompts
from config import Config
from question import Question
from results import Results

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

#

def do_quiz(settings:Config, questions:list[Question]) -> int:
    '''
    Do the quiz, displaying the results at the end.
    
    Parameters:
        settings : Config
            The configuration settings for the quiz.
        questions : list[Question]

    Returns:
        The final (adjusted) score.

    Calls:
        do_question
    '''
    
    results = Results()
    shuffle(questions)
    for q in range(settings.get_number_of_questions):
        print(DisplayText.QUESTION.format(q + 1, settings.get_number_of_questions, questions[q].get_question))
        do_question(settings, questions[q], results)

    final_score = results.calculate_adjusted_score()
    print(DisplayText.RESULTS.format(results.get_questions_correct, settings.get_number_of_questions, results.get_score, results.get_max_score, final_score))
    return final_score

def do_question(settings:Config, question:Question, results:Results):
    '''
    Display a question, get the user's response, and tell them whether they were correct.

    Parameters:
        settings : Config
            The configuration settings for the quiz.
        question : Question
            The question to ask the user.
        results : Results
            These will be adjusted based on the user's answer.

    Calls:
        print_answer_options
        get_answer
    '''

    attempts = settings.get_number_of_attempts

    if settings.get_multiple_choice:
        shuffle(question.get_answer_options)
        # Ensure number of attempts does not exceed the number of incorrect answer options.
        attempts = min(settings.get_number_of_attempts, len(question.get_answer_options) - 1)
        print_answer_options(question.get_answer_options, settings.get_select_using_index)

    results.increase_max_score_by(attempts)

    points, correct = get_answer(settings.get_multiple_choice, settings.get_select_using_index, attempts, question)

    if correct:
        print(DisplayText.CORRECT.format(points))
        results.increase_score_by(points)
        results.increment_questions_correct()

    print(DisplayText.CURRENT_SCORE.format(results.get_score))

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

def get_answer(multiple_choice:bool, select_using_index:bool, max_attempts:int, question:Question) -> tuple[int, bool]:
    '''
    User types in/selects an answer.

    Parameters:
        multiple_choice : bool
            Whether or not the question is a multiple-choice question.
        select_using_index : bool
            [For multiple-choice questions] Whether the user should select the option by typing it in or by entering an index.
        max_attempts : int
            Maximum number of attempts for this question.
        question : Question
            The question to ask.

    Returns:
        `tuple[int, bool]`
            The `int` is the number of points the user earned for this question.
            The `bool` is whether or not the user entered the correct answer.

    Calls:
        select_answer_using_index
        type_answer
    '''

    attempt = 1
    correct = False
    points = max_attempts

    while not correct and (attempt <= max_attempts):

        if multiple_choice and select_using_index:
            correct = select_answer_using_index(question)
        else:
            correct = type_answer(question)

        if not correct:
            points -= 1
            print(DisplayText.INCORRECT.format(max_attempts - attempt))

        attempt += 1

    return points, correct

def select_answer_using_index(question:Question) -> bool:
    '''
    Prompt the user to enter a valid index.

    Parameters:
        question : Question

    Returns:
        `True` if the user entered the correct answer.
        `False` otherwise.
    '''
    
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
    '''
    Prompt the user to type in the answer.

    Parameters:
        question : Question

    Returns:
        `True` if the user typed in the correct answer (has to be exactly correct, non-case-sensitive).
        `False` otherwise.
    '''
    
    answer = input(Prompts.ANSWER_TYPED + "\n")
    return answer.lower() == question.get_answer.lower()

#

def save_and_view_scores(score_file_path:str, score:int):
    '''
    Allow the user to save their score and view their past scores.

    Parameters:
        score_file_path : str
            The path to the score file.
        score : int
            The user's final (adjusted) score.

    Calls:
        load_score_file
        yes_or_no
        save_score
        print_scores
    '''
    
    try:
        scores = load_files.load_score_file(score_file_path)
        score_file_corrupted = False
    except ValueError:
        score_file_corrupted = True
        scores = {}

    time_stamp = DisplayText.TIME_STAMP.format(datetime.datetime.now())
    if name in scores.keys():
        scores[name][time_stamp] = score
    else:
        scores[name] = {time_stamp : score}

    save = yes_or_no(Prompts.SAVE_SCORE)
    if save:
        save_score(scores, score_file_corrupted)

    view_scores = yes_or_no(Prompts.VIEW_SCORES)
    if view_scores:
        print_scores(name, scores)

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

def save_score(scores:dict[str, dict[str, int]], score_file_corrupted:bool):
    '''
    Save scores to the scores file.

    Parameters:
        scores : dict[str, dict[str, int]]
            All the currently saved scores.
        score_file_corrupted : bool
            Whether or not the score file was loaded correctly.

    Calls:
        yes_or_no
        save_score_file
    '''

    if score_file_corrupted:
        print(ErrorMessages.FILE_CORRUPTED.format(settings.get_score_file_path))
        overwrite_corrupted_score_file = yes_or_no(Prompts.SAVE_SCORE + Prompts.OVERWRITE_CORRUPTED_SCORES)
        if not overwrite_corrupted_score_file:
            return
    load_files.save_score_file(settings.get_score_file_path, scores)
    print(DisplayText.SCORE_SAVED)

def print_scores(name:str, scores:dict[str, dict[str, int]]):
    '''
    Display the timestamps and scores saved under the specified `name` in order of score (descending).

    Parameters:
        name : str
            Scores saved under this name will be displayed.
        scores: dict[str, dict[str, int]]
            All the saved scores.

    Calls:
        sort_scores
    '''
    if name not in scores:
        print(DisplayText.NO_SCORES_FOR_USER.format(name))
        return
    print(DisplayText.SCORE_TABLE_HEADER)
    for time_stamp, score in sort_scores(scores[name]).items():
        print(DisplayText.SCORE_TABLE_ROW.format(time_stamp[:-3], score))

def sort_scores(scores:dict[str, int]) -> dict[str, int]:
    '''
    Sort a scores dictionary according to the scores in descending order.

    Parameters:
        scores : dict[str, int]
            The scores to sort.
    
    Returns:
        The sorted `scores`.

    Calls:
        sort_dict
    '''
    return sort_dict(scores)

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

#---------------#
# PROGRAM START #
#---------------#

settings, questions = load_files.load_essential_files()

print(DisplayText.WELCOME)
name = get_user_name()

final_score = do_quiz(settings, questions)

save_and_view_scores(settings.get_score_file_path, final_score)

print(DisplayText.GOODBYE)
