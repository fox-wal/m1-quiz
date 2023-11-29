class Question:
    '''
    A class to store details of a question.

    Attributes:
        __question : str
            The question.
        __answer_options : list[str]
            All the multiple-choice answers to the question (correct *and* incorrect).
        __answer : str
            The correct answer to the question.
    '''
    
    def __init__(self, question:str, answer:str, answer_options:list[str]):
        self.__question = question
        self.__answer = answer
        self.__answer_options = answer_options
    
    def __str__(self):
        answer_options = '\n* '.join(self.__answer_options)
        return f'''Question: {self.__question}
Answer: {self.__answer}
Answer Options:
* {answer_options}'''

    @property
    def get_question(self):
        return self.__question
    @property
    def get_answer(self):
        return self.__answer
    @property
    def get_answer_options(self):
        return self.__answer_options
