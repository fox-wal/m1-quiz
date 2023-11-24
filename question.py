class Question:
    def __init__(self, question:str, answer:str, answer_options:list[str]):
        self.__question = question
        self.__answer = answer
        self.__answer_options = answer_options
    
    def __str__(self):
        return 'Question: {}\nAnswer: {}\nAnswer Options:\n * {}'.format(self.get_question, self.get_answer, '\n * '.join(self.get_answer_options))

    @property
    def get_question(self):
        return self.__question
    @property
    def get_answer(self):
        return self.__answer
    @property
    def get_answer_options(self):
        return self.__answer_options
