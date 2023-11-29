from random import shuffle
from display_text import DisplayText
from prompts import Prompts
from question import Question
from results import Results

class Quiz:
    def __init__(self, questions:list[Question], multiple_choice:bool, select_using_index:bool, max_number_of_attempts:int) -> None:
        self.__questions = questions
        self.__results = Results()
        self.__multiple_choice = multiple_choice
        self.__select_using_index = select_using_index
        self.__max_number_of_attempts = max_number_of_attempts
        self.__final_score = None

    def __str__(self) -> str:
        return f'''questions: {self.__questions}
results: {self.__results}
multiple_choice: {self.__multiple_choice}
select_using_index: {self.__select_using_index}
max_number_of_attempts: {self.__max_number_of_attempts}
final_score: {self.__final_score}'''

    @property
    def get_final_score(self) -> int:
        return self.__final_score

    def start(self):
        '''
        Do the quiz, displaying the results at the end.
        
        Returns:
            The final (adjusted) score.

        Calls:
            do_question
        '''
        for q in range(len(self.__questions)):
            print(DisplayText.QUESTION.format(q + 1, len(self.__questions), self.__questions[q].get_question))
            self.do_question(self.__questions[q])

        self.__final_score = self.__results.calculate_adjusted_score()
        print(DisplayText.RESULTS.format(self.__results.get_questions_correct, len(self.__questions), self.__results.get_score, self.__results.get_max_score, self.__final_score))

    def do_question(self, question:Question):
        '''
        Display a question, get the user's response, and tell them whether they were correct.

        Parameters:
            question : Question
                The question to ask the user.

        Calls:
            print_answer_options
            get_answer
        '''
        attempts = self.__max_number_of_attempts

        if self.__multiple_choice:
            shuffle(question.get_answer_options)
            # Ensure number of attempts does not exceed the number of incorrect answer options.
            attempts = min(self.__max_number_of_attempts, len(question.get_answer_options) - 1)
            self.print_answer_options(question.get_answer_options)

        self.__results.increase_max_score_by(attempts)

        points, correct = self.get_answer(question)

        if correct:
            print(DisplayText.CORRECT.format(points))
            self.__results.increase_score_by(points)
            self.__results.increment_questions_correct()

        print(DisplayText.CURRENT_SCORE.format(self.__results.get_score))

    def print_answer_options(self, answer_options:list[str]):
        '''
        Print the answer options for a multiple-choice question.

        Parameters:
            answer_options : list[str]
                All the answer options (including correct) for the question.
        '''
        for o in range(len(answer_options)):
            if self.__select_using_index:
                print(DisplayText.INDEXED_ANSWER_OPTION.format(o + 1, answer_options[o]))
            else:
                print(DisplayText.ANSWER_OPTION.format(answer_options[o]))

        if self.__select_using_index:
            print(Prompts.ANSWER_BY_INDEX)
        else:
            print(Prompts.ANSWER_TYPED)

    def get_answer(self, question:Question) -> tuple[int, bool]:
        '''
        User types in/selects an answer.

        Parameters:
            question : Question
                The question to ask.

        Returns:
            `tuple[int, bool]`
                The `int` is the number of points the user earned for this question.
                The `bool` is whether or not the user entered the correct answer.

        Calls:
            select_answer_using_index
            type_answer
        '''
        attempt = 1
        correct = False
        points = self.__max_number_of_attempts

        while not correct and (attempt <= self.__max_number_of_attempts):

            if self.__multiple_choice and self.__select_using_index:
                correct = self.select_answer_using_index(question)
            else:
                correct = self.type_answer(question)

            if not correct:
                points -= 1
                print(DisplayText.INCORRECT.format(self.__max_number_of_attempts - attempt))

            attempt += 1

        return points, correct

    def select_answer_using_index(self, question:Question) -> bool:
        '''
        Prompt the user to enter a valid index.

        Parameters:
            question : Question

        Returns:
            `True` if the user entered the correct answer.
            `False` otherwise.
        '''
        while True:
            try:
                choice = int(input()) - 1
                if choice not in range(len(question.get_answer_options)):
                    raise ValueError
            except ValueError:
                print(Prompts.VALID_INDEX.format(1, len(question.get_answer_options)))
            else:
                return question.get_answer_options[choice] == question.get_answer

    def type_answer(self, question:Question) -> bool:
        '''
        Prompt the user to type in the answer.

        Parameters:
            question : Question

        Returns:
            `True` if the user typed in the correct answer (has to be exactly correct, non-case-sensitive).
            `False` otherwise.
        '''
        answer = input(Prompts.ANSWER_TYPED + "\n")
        return answer.lower() == question.get_answer.lower()
