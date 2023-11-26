class Prompts:
    '''
    A class containing all prompts.

    Attributes:
        NAME : str
            Prompt the user to enter their name.
        ANSWER_TYPED : str
            Prompt the user to type in the answer.
        ANSWER_BY_INDEX : str
            Prompt the user to enter the index of the answer.
        SAVE_SCORE : str
            Ask the user whether they want to save their score.
        VIEW_SCORES : str
            Ask the user whether they want to view all of their previous scores.
        OVERWRITE_CORRUPTED_SCORES : str
            Ask the user whether they want their new score to overwrite everything in the corrupted score file.
        VALID_INDEX : str
            Prompt the user to enter a valid index.

            Arguments:
            
            1. The minimum allowed index.
            2. The maximum allowed index.
        
        VALID_OPTION : str
            Prompt the user to enter a valid option.

            Arguments:

            1. The valid options.
    '''

    NAME : str
    ANSWER_TYPED : str
    ANSWER_BY_INDEX : str
    SAVE_SCORE : str
    VIEW_SCORES : str
    OVERWRITE_CORRUPTED_SCORES : str
    VALID_INDEX : str
    VALID_OPTION : str
    YES_OR_NO : str

    def set_values(self, name:str, answer_typed:str, answer_by_index:str, save_score:str, view_scores:str, overwrite_corrupted_scores:str, valid_index:str, valid_option:str, yes_or_no:str):
        self.NAME = name
        self.ANSWER_TYPED = answer_typed
        self.ANSWER_BY_INDEX = answer_by_index
        self.SAVE_SCORE = save_score
        self.VIEW_SCORES = view_scores
        self.OVERWRITE_CORRUPTED_SCORES = overwrite_corrupted_scores
        self.VALID_INDEX = valid_index
        self.VALID_OPTION = valid_option
        self.YES_OR_NO = yes_or_no
