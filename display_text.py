class DisplayText:
    '''
    A class containing all non-prompt display text.

    Attributes:
        WELCOME : str
            Welcome the user to the quiz.
        SCORE_TABLE_HEADER : str
            The header row for the score table.
        GOODBYE : str
            Say goodbye to the user at the end of the program.
        QUESTION : str
            Use to format a question.

            Arguments:

            1. Question number
            2. Number of questions
            3. Question
        INDEXED_ANSWER_OPTION : str
            Use to format an indexed answer option.
            Arguments:

            1. Index
            2. Answer option
        ANSWER_OPTION : str
            Use to format a non-indexed answer option.
                Arguments:
                1. Answer option
        CORRECT : str
            Inform the user their answer was correct.

            Arguments:

            1. Points earned
        INCORRECT : str
            Inform the user their answer was incorrect.

            Arguments:

            1. Number of remaining attempts
        CURRENT_SCORE : str
            Inform the user of their current score.

            Arguments:

            1. Current score
        RESULTS : str
            Use to format a summary of the results of the quiz.

            Arguments:

            1. # correct answers
            2. # questions
            3. Final score
            4. Maximum score
            5. Adjusted score
        TIME_STAMP : str    
            Use to format a timestamp.

            Arguments:

            1. Year
            2. Month
            3. Day
            4. Hour
            5. Minute
            6. Second
        NO_SCORES_FOR_USER : str
            Inform the user that no previous scores have been found for them.

            Arguments:

            1. User's name
        SCORE_TABLE_ROW : str
            A row for the score table.

            Arguments:

            1. Timestamp (formatted, max length 16)
            2. Score (integer, max 3 digits)
        SCORE_SAVED : str
            Inform the user that their score has been saved.
        INVALID_CHARACTER : str
            Error message for when the user enters an input containing an invalid character.

            Arguments:
            
            1. The character in question.
        COULD_NOT_SAVE_SCORE : str
            Error message for when the user's score could not be saved to the score file.
    '''

    WELCOME : str
    SCORE_TABLE_HEADER : str
    GOODBYE : str
    QUESTION : str
    INDEXED_ANSWER_OPTION : str
    ANSWER_OPTION : str
    CORRECT : str
    INCORRECT : str
    CURRENT_SCORE : str
    RESULTS : str
    TIME_STAMP : str    
    NO_SCORES_FOR_USER : str
    SCORE_TABLE_ROW : str
    SCORE_SAVED : str
    INVALID_CHARACTER : str
    COULD_NOT_SAVE_SCORE : str

    def set_values(self, welcome:str, score_table_header:str, goodbye:str, question:str, indexed_answer_option:str, answer_option:str, correct:str, incorrect:str, current_score:str, results:str, time_stamp:str, no_scores_for_user:str, score_table_row:str, score_saved:str, invalid_character:str, could_not_save_score:str):
        DisplayText.WELCOME = welcome
        DisplayText.SCORE_TABLE_HEADER = score_table_header
        DisplayText.GOODBYE = goodbye
        DisplayText.QUESTION = question
        DisplayText.INDEXED_ANSWER_OPTION = indexed_answer_option
        DisplayText.ANSWER_OPTION = answer_option
        DisplayText.CORRECT = correct
        DisplayText.INCORRECT = incorrect
        DisplayText.CURRENT_SCORE = current_score
        DisplayText.RESULTS = results
        DisplayText.TIME_STAMP = time_stamp
        DisplayText.NO_SCORES_FOR_USER = no_scores_for_user
        DisplayText.SCORE_TABLE_ROW = score_table_row
        DisplayText.SCORE_SAVED = score_saved
        DisplayText.INVALID_CHARACTER = invalid_character
        DisplayText.COULD_NOT_SAVE_SCORE = could_not_save_score
