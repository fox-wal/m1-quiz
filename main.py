from random import shuffle
import datetime as dt
from error_handling import *
from display import *
from load_files import *
from display import DisplayText, Prompts
from config import Config
from question import Question

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

def get_answer_results(points:int, multiple_choice:bool, select_using_index:bool, max_attempts:int, answer:str, answer_options:list[str] = []) -> tuple[int, bool]:
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

        # Select answer using index (multiple choice only).

        if multiple_choice and select_using_index:
            while True:
                try:
                    choice = int(input()) - 1
                    if choice not in range(len(answer_options)):
                        raise ValueError
                except ValueError:
                    print(Prompts.VALID_INDEX.format(1, len(answer_options)))
                else:
                    break
            correct = answer_options[choice] == answer

        # Type in answer

        else:
            print(Prompts.ANSWER_TYPED)
            correct = input().lower() == answer.lower()

        # Calculate points + attempts.

        if not correct:
            print(DisplayText.INCORRECT.format(max_attempts - attempt))
            points -= 1
        attempt += 1

    return (points, correct)

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

#------------#
# Initialize #
#------------#

# Load essential files

CONFIG_FILE_PATH = "data/config.json"

settings:Config = load_config_file(CONFIG_FILE_PATH)
questions:list[Question] = load_questions_file(settings.get_question_file_path)

#---------#
# Welcome #
#---------#

print(DisplayText.WELCOME)
name = get_user_name()

#------------#
# Start Quiz #
#------------#

max_score = 0
score = 0
questions_correct = 0
number_of_questions = min(len(questions), settings.get_number_of_questions)
for q in range(number_of_questions):

    # Print question.

    print(DisplayText.QUESTION.format(q + 1, number_of_questions, questions[q].get_question))
    
    # [Multiple choice] Print answer options.

    answer_options = questions[q].get_answer_options
    shuffle(answer_options)
    attempts = settings.get_number_of_attempts
    if settings.get_multiple_choice:
        # Ensure number of attempts does not exceed the number of incorrect answer options.
        attempts = min(settings.get_number_of_attempts, len(questions[q].get_answer_options) - 1)
        print_answer_options(
            select_using_index = settings.get_select_using_index
            ,answer_options    = questions[q].get_answer_options
        )

    # User enters answer.

    points = attempts
    max_score += points

    points, correct = get_answer_results(
        points              = points
        ,multiple_choice    = settings.get_multiple_choice
        ,select_using_index = settings.get_select_using_index
        ,max_attempts       = attempts
        ,answer             = questions[q].get_answer
        ,answer_options     = answer_options
    )

    # Process answer results.

    if correct:
        print(DisplayText.CORRECT.format(points))
        score += points
        questions_correct += 1
    
    print(DisplayText.CURRENT_SCORE.format(score))

#--------------#
# Quiz Results #
#--------------#

adjusted_score = int(100 * (score / max_score))
print(DisplayText.RESULTS.format(questions_correct, number_of_questions, score, max_score, adjusted_score))

#------------#
# Save Score #
#------------#

# Ask if user wants to save it.

print(Prompts.SAVE_SCORE.format('/'.join(['Yes', 'No'])))

while True:
    choice = input().upper()
    if choice not in ['Yes', 'No']:
        print(Prompts.VALID_OPTION.format('/'.join(['Yes', 'No'])))
    else:
        break

if choice == 'YES':
    time_stamp = DisplayText.TIME_STAMP.format(dt.datetime.now())
    scores : dict[str, dict[str, int]] = {}

    # Load scores.

    try:
        scores = load_score_file(settings.get_score_file_path)
    except FileNotFoundError:
        print('DEBUG: Score file created.')
    except ValueError:
        scores = {}
        print(ErrorMessages.FILE_CORRUPTED.format(settings.get_score_file_path))

        # Ask if user wants to overwrite the corrupted file with their new score.
        print(Prompts.SAVE_SCORE.format('/'.join(['Yes', 'No'])), Prompts.OVERWRITE_CORRUPTED_SCORES)

        while True:
            choice = input().upper()
            if choice not in ['Yes', 'No']:
                print(Prompts.VALID_OPTION.format('/'.join(['Yes', 'No'])))
            else:
                break
        if choice == 'YES':
            scores[name] = {time_stamp : adjusted_score}
            print(DisplayText.SCORE_SAVED)
            save_score_file(settings.get_score_file_path, scores)
    else:
        
        # Save scores.

        if name in scores.keys():
            scores[name][time_stamp] = adjusted_score
        else:
            scores[name] = {time_stamp : adjusted_score}
        print(DisplayText.SCORE_SAVED)
        save_score_file(settings.get_score_file_path, scores)

    # View scores.

    print(Prompts.VIEW_SCORES.format('/'.join(['Yes', 'No'])))
    while True:
        choice = input().upper()
        if choice in ['Yes', 'No']:
            break
        else:
            print(Prompts.VALID_OPTION.format('/'.join(['Yes', 'No'])))
    if choice == "YES":
        print_scores(name, scores)

#------#
# Exit #
#------#

print(DisplayText.GOODBYE)
