import datetime
import os
from error_handling import ErrorMessages
import file_handling as files
from display_text import DisplayText
from prompts import Prompts

def save_and_view_scores(name : str, score_file_path:str, score:int):
    '''
    Allow the user to save their score and view their past scores.

    Parameters:
        name : str
            The user's name.
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
        scores = files.load_score_file(score_file_path)
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
        save_score(score_file_path, scores, score_file_corrupted)

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

def save_score(score_file_path:str, scores:dict[str, dict[str, int]], score_file_corrupted:bool):
    '''
    Save scores to the scores file.

    Parameters:
        score_file_path : str
            The path to the score file.
        scores : dict[str, dict[str, int]]
            All the currently saved scores.
        score_file_corrupted : bool
            Whether or not the score file was loaded correctly.

    Calls:
        yes_or_no
        save_score_file
    '''

    if score_file_corrupted:
        print(ErrorMessages.FILE_CORRUPTED.format(os.path.abspath(score_file_path)))
        overwrite_corrupted_score_file = yes_or_no(Prompts.SAVE_SCORE + Prompts.OVERWRITE_CORRUPTED_SCORES)
        if not overwrite_corrupted_score_file:
            return
    files.save_score_file(score_file_path, scores)
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
