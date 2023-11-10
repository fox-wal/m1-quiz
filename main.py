import json as json
from random import shuffle
import datetime as dt
from error_messages import *
from display_messages import *
from keys import *
from load_files import *

def sort_dict(dictionary:dict) -> dict:
    as_list = []
    sorted_dict = {}
    for key, value in dictionary.items():
        as_list.append((key, value))
    as_list.sort(key=lambda item: item[1], reverse=True)
    for i in as_list:
        sorted_dict[i[0]] = i[1]
    return sorted_dict

def sort_scores(scores:dict[str, int]) -> dict[str, int]:
    return sort_dict(scores)

def print_scores(name:str, scores:dict):
    if name not in scores:
        print(NO_SCORES_FOR_USER.format(name))
        return
    print(SCORE_VIEW_HEADER)
    for time_stamp, score in sort_scores(scores[name]).items():
        print(SCORE_FORMAT.format(time_stamp[:-3], score))

def print_answer_options(question:dict, answer_options:list[str], select_using_index:bool):
    """
    Print the answer options for a multiple-choice question.
    """

    for o in range(len(answer_options)):
        if select_using_index:
            print(MULTI_CHOICE_OPTION_WITH_INDEX_LINE.format(o + 1, answer_options[o]))
        else:
            print(answer_options[o])

    # Prompt user to choose.
    if select_using_index:
        print(MULTI_CHOICE_INDEX_PROMPT)
    else:
        print(TYPE_IN_ANSWER_PROMPT)

def get_answer_results(points:int, multiple_choice:bool, select_using_index:bool, max_attempts:int, answer:str, answer_options:list[str] = []) -> tuple[int, bool]:
    """
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
        answer_options : list[str]
            [For multiple-choice questions] All the answer options (including the correct one).

    Returns:
        `tuple[int, bool]`
            The `int` is the number of points the user earned for this question.
            The `bool` is whether or not the user entered the correct answer.
    """

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
                    print(ENTER_INDEX_IN_CORRECT_RANGE_PROMPT.format(1, len(answer_options)))
                else:
                    break
            correct = answer_options[choice] == answer

        # Type in answer

        else:
            print(TYPE_IN_ANSWER_PROMPT)
            correct = input().lower() == answer.lower()

        # Calculate points + attempts.

        if not correct:
            print(INCORRECT.format(max_attempts - attempt))
            points -= 1
        attempt += 1

    return (points, correct)

def get_user_name() -> str:
    """
    Returns:
        User name.
    """
    while True:
        name = input(NAME_PROMPT)
        if "\"" in name:
            print(INVALID_CHARACTER.format("\""))
        else:
            return name

# Load essential files

settings = load_config_file()
questions = load_questions_file(settings[S_QUESTION_FILE_PATH])

# Welcome

print(WELCOME)
name = get_user_name()

# Start Quiz
max_score = 0
score = 0
questions_correct = 0
number_of_questions = min(len(questions), settings[S_NUMBER_OF_QUESTIONS])
for q in range(number_of_questions):

    # Print question.
    print(QUESTION_LINE.format(q + 1, number_of_questions, questions[q][Q_QUESTION]))
    
    # Print answer options.
    answer_options = questions[q][Q_ANSWER_OPTIONS] + [questions[q][Q_ANSWER]]
    attempts = settings[S_NUMBER_OF_ATTEMPTS]
    shuffle(answer_options)
    if settings[S_MULTIPLE_CHOICE]:
        # Ensure number of attempts does not exceed the number of incorrect answer options.
        attempts = min(settings[S_NUMBER_OF_ATTEMPTS], len(questions[q][Q_ANSWER_OPTIONS]))
        print_answer_options(
            question=questions[q]
            ,select_using_index=settings[S_MULTIPLE_CHOICE_USE_INDEX]
            ,answer_options=answer_options
        )

    # User enters answer.
    points = attempts
    max_score += points

    points, correct = get_answer_results(
        points=points
        ,multiple_choice=settings[S_MULTIPLE_CHOICE]
        ,select_using_index=settings[S_MULTIPLE_CHOICE_USE_INDEX]
        ,max_attempts=attempts
        ,answer=questions[q][Q_ANSWER]
        ,answer_options=answer_options
    )

    # Process answer results.

    if correct:
        print(CORRECT.format(points))
        score += points
        questions_correct += 1
    
    print(SCORE_SO_FAR.format(score))

# Quiz Results

adjusted_score = int(100 * (score / max_score))
print(RESULTS.format(questions_correct, number_of_questions, score, max_score, adjusted_score))

# Save Score

## Ask if user wants to save it.

print(SAVE_SCORE_PROMPT.format(YES_NO_PROMPT_SEPARATOR.join(YES_NO)))

while True:
    choice = input().upper()
    if choice not in YES_NO:
        print(ENTER_ONE_OF_PROMPT.format(YES_NO_ERROR_PROMPT_SEPARATOR.join(YES_NO)))
    else:
        break

if choice == YES:
    time_stamp = TIME_STAMP_FORMAT.format(dt.datetime.now())
    scores : dict[str, dict[str, int]] = {}

    # Load score file.
    try:
        scores = load_score_file(settings[S_SCORE_FILE_PATH])
    except FileNotFoundError:
        print(SCORE_FILE_CREATED)
    except ValueError:
        scores = {}
        print(SCORES_FILE_CORRUPTED)

        print(SAVE_SCORE_PROMPT.format(YES_NO_PROMPT_SEPARATOR.join(YES_NO)), OVERWRITE_CORRUPTED_FILE)

        while True:
            choice = input().upper()
            if choice not in YES_NO:
                print(ENTER_ONE_OF_PROMPT.format(YES_NO_ERROR_PROMPT_SEPARATOR.join(YES_NO)))
            else:
                break
        if choice == YES:
            scores[name] = {time_stamp : adjusted_score}
            print(SCORE_SAVED)
            save_score_file(settings[S_SCORE_FILE_PATH], scores)
    else:
        # Save score file.
        if name in scores.keys():
            scores[name][time_stamp] = adjusted_score
        else:
            scores[name] = {time_stamp : adjusted_score}
        print(SCORE_SAVED)
        save_score_file(settings[S_SCORE_FILE_PATH], scores)

    print(VIEW_YOUR_SCORES_PROMPT.format(YES_NO_PROMPT_SEPARATOR.join(YES_NO)))
    while True:
        choice = input().upper()
        if choice in YES_NO:
            break
        else:
            print(ENTER_ONE_OF_PROMPT.format(YES_NO_ERROR_PROMPT_SEPARATOR.join(YES_NO)))
    if choice == YES:
        print_scores(name, scores)

print(GOODBYE)
