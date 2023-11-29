class Results:
    '''
    A class to store quiz results.

    Attributes:
        __max_score : int
            The maximum possible score for this quiz.
        __score : int
            The user's current score.
        __questions_correct : int
            The number of questions the user has answered correctly.

    Methods:
        increase_max_score(self, increase_by:int)
        increase_score(self, increase_by:int)
        increment_questions_correct(self)
        calculate_adjusted_score(self)
    '''

    def __init__(self, max_score:int = 0, score:int = 0, questions_correct:int = 0) -> None:
        self.__max_score = max_score
        self.__score = score
        self.__questions_correct = questions_correct

    def __str__(self) -> str:
        return f'''max_score: {self.__max_score}
score: {self.__score}
questions_correct: {self.__questions_correct}'''

    @property
    def get_max_score(self) -> int:
        return self.__max_score
    @property
    def get_score(self) -> int:
        return self.__score
    @property
    def get_questions_correct(self) -> int:
        return self.__questions_correct

    def increase_max_score_by(self, increase_by:int):
        ''''''
        self.__max_score += increase_by

    def increase_score_by(self, increase_by:int):
        self.__score += increase_by

    def increment_questions_correct(self):
        self.__questions_correct += 1

    def calculate_adjusted_score(self) -> int:
        '''
        Returns:
            The score as a percentage (score / max_score).
        '''
        return int(100 * (self.__score / self.__max_score))
