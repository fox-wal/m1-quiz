from dataclasses import dataclass

@dataclass
class DisplayText:
    class Prompt:
        NAME : str
        '''Prompt the user to enter their name.'''
        ANSWER_TYPED : str
        '''Prompt the user to type in the answer.'''
        ANSWER_BY_INDEX : str
        '''Prompt the user to enter the index of the answer.'''
        SAVE_SCORE : str
        '''Ask the user whether they want to save their score.'''
        VIEW_SCORES : str
        '''Ask the user whether they want to view all of their previous scores.'''
        OVERWRITE_CORRUPTED_SCORES : str
        '''Ask the user whether they want their new score to overwrite everything in the corrupted score file.'''
    WELCOME : str
    '''Welcome the user to the quiz.'''
    SCORE_TABLE_HEADER : str
    '''The header row for the score table.'''
    GOODBYE : str
    '''Say goodbye to the user at the end of the program.'''
    QUESTION : str
    '''
    Use to format a question.

    Format elements:

    1. Question number
    2. Number of questions
    3. Question
    '''
    INDEXED_ANSWER_OPTION : str
    '''
    Use to format an indexed answer option.

    Format elements:

    1. Index
    2. Answer option
    '''
    ANSWER_OPTION : str
    '''
    Use to format a non-indexed answer option.

    1. Answer option
    '''
    CORRECT : str
    '''
    Inform the user their answer was correct.

    Format elements:

    1. Points earned
    '''
    INCORRECT : str
    '''
    Inform the user their answer was incorrect.

    Format elements:

    1. Number of remaining attempts
    '''
    CURRENT_SCORE : str
    '''
    Inform the user of their current score.

    Format elements:

    1. Current score
    '''
    RESULTS : str
    '''
    Use to format a summary of the results of the quiz.

    Format elements:

    1. # correct answers
    2. # questions
    3. Final score
    4. Maximum score
    5. Adjusted score
    '''
    TIME_STAMP : str
    '''
    Use to format a timestamp.

    Format elements:

    1. Year
    2. Month
    3. Day
    4. Hour
    5. Minute
    6. Second
    '''
    SCORE_TABLE_ROW : str
    '''
    A row for the score table.

    Format elements:

    1. Timestamp (formatted, max length 16)
    2. Score (integer, max 3 digits)
    '''
    SCORE_SAVED : str
    '''Inform the user that their score has been saved.'''
    PROGRAM_ABENDED : str
    '''Inform the user that the program has abended.'''
