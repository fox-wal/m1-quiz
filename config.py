class Config:
    '''
    A class to store all the configuration settings for the game.

    Attributes:
        __number_of_questions : int
            The number of questions to ask in the quiz.
        __number_of_attempts : int
            The maximum number of attempts the user should get per question.
        __multiple_choice : bool
            Whether the user should get to choose from different answer options when answering the questions.
        __select_using_index : bool
            Whether the user should be able to select the correct answer by its index or have to type it in (only applies if `__multpile_choice` is true).
        __question_file_path : str
            The path to the file containing all the questions.
        __score_file_path : str
            The path to the file containing all past scores.
        __display_text_file_path : str
            The path to the file containing display text.
        __prompt_file_path : str
            The path to the file containing prompt text.
    '''

    def __init__(self, number_of_questions:int, number_of_attempts:int, multiple_choice:bool, select_using_index:bool, question_file_path:str, score_file_path:str, display_text_file_path:str, prompt_file_path:str):
        # Ensure numbers of attempts and questions are at least 1.
        self.__number_of_questions = max(1, number_of_questions)
        self.__number_of_attempts = max(1, number_of_attempts)
        self.__multiple_choice = multiple_choice
        self.__select_using_index = select_using_index
        self.__question_file_path = question_file_path
        self.__score_file_path = score_file_path
        self.__display_text_file_path = display_text_file_path
        self.__prompt_file_path = prompt_file_path

    def __str__(self) -> str:
        return '''number_of_questions: {}
number_of_attempts: {}
multiple_choice: {}
select_using_index: {}
question_file_path: {}
score_file_path: {}
display_text_file_path: {}
prompt_file_path": {}'''.format(self.get_number_of_questions
        ,self.get_number_of_attempts
        ,self.get_multiple_choice
        ,self.get_select_using_index
        ,self.get_question_file_path
        ,self.get_score_file_path
        ,self.get_display_text_file_path
        ,self.get_prompt_file_path
        )

    @property
    def get_number_of_questions(self):
        return self.__number_of_questions
    @property
    def get_number_of_attempts(self):
        return self.__number_of_attempts
    @property
    def get_multiple_choice(self):
        return self.__multiple_choice
    @property
    def get_select_using_index(self):
        return self.__select_using_index
    @property
    def get_question_file_path(self):
        return self.__question_file_path
    @property
    def get_score_file_path(self):
        return self.__score_file_path
    @property
    def get_display_text_file_path(self):
        return self.__display_text_file_path
    @property
    def get_prompt_file_path(self):
        return self.__prompt_file_path