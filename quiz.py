from random import shuffle
from config import Config
from display_text import DisplayText
from prompts import Prompts
from question import Question
from results import Results

def do_quiz(settings:Config, questions:list[Question]) -> int:
    '''
    Do the quiz, displaying the results at the end.
    
    Parameters:
        settings : Config
            The configuration settings for the quiz.
        questions : list[Question]

    Returns:
        The final (adjusted) score.

    Calls:
        do_question
    '''
    
    results = Results()
    shuffle(questions)
    for q in range(settings.get_number_of_questions):
        print(DisplayText.QUESTION.format(q + 1, settings.get_number_of_questions, questions[q].get_question))
        do_question(settings, questions[q], results)

    final_score = results.calculate_adjusted_score()
    print(DisplayText.RESULTS.format(results.get_questions_correct, settings.get_number_of_questions, results.get_score, results.get_max_score, final_score))
    return final_score

def do_question(settings:Config, question:Question, results:Results):
    '''
    Display a question, get the user's response, and tell them whether they were correct.

    Parameters:
        settings : Config
            The configuration settings for the quiz.
        question : Question
            The question to ask the user.
        results : Results
            These will be adjusted based on the user's answer.

    Calls:
        print_answer_options
        get_answer
    '''

    attempts = settings.get_number_of_attempts

    if settings.get_multiple_choice:
        shuffle(question.get_answer_options)
        # Ensure number of attempts does not exceed the number of incorrect answer options.
        attempts = min(settings.get_number_of_attempts, len(question.get_answer_options) - 1)
        print_answer_options(question.get_answer_options, settings.get_select_using_index)

    results.increase_max_score_by(attempts)

    points, correct = get_answer(settings.get_multiple_choice, settings.get_select_using_index, attempts, question)

    if correct:
        print(DisplayText.CORRECT.format(points))
        results.increase_score_by(points)
        results.increment_questions_correct()

    print(DisplayText.CURRENT_SCORE.format(results.get_score))

def print_answer_options(answer_options:list[str], select_using_index:bool):
    '''
    Print the answer options for a multiple-choice question.

    Parameters:
        answer_options : list[str]
            All the answer options (including correct) for the question.
        select_using_index : bool
            If True: the user must enter the index of the answer they think is correct.
            If False: the user must enter the answer they think is correct.
    '''

    for o in range(len(answer_options)):
        if select_using_index:
            print(DisplayText.INDEXED_ANSWER_OPTION.format(o + 1, answer_options[o]))
        else:
            print(DisplayText.ANSWER_OPTION.format(answer_options[o]))

    # Prompt user to choose.
    
    if select_using_index:
        print(Prompts.ANSWER_BY_INDEX)
    else:
        print(Prompts.ANSWER_TYPED)

def get_answer(multiple_choice:bool, select_using_index:bool, max_attempts:int, question:Question) -> tuple[int, bool]:
    '''
    User types in/selects an answer.

    Parameters:
        multiple_choice : bool
            Whether or not the question is a multiple-choice question.
        select_using_index : bool
            [For multiple-choice questions] Whether the user should select the option by typing it in or by entering an index.
        max_attempts : int
            Maximum number of attempts for this question.
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
    points = max_attempts

    while not correct and (attempt <= max_attempts):

        if multiple_choice and select_using_index:
            correct = select_answer_using_index(question)
        else:
            correct = type_answer(question)

        if not correct:
            points -= 1
            print(DisplayText.INCORRECT.format(max_attempts - attempt))

        attempt += 1

    return points, correct

def select_answer_using_index(question:Question) -> bool:
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

def type_answer(question:Question) -> bool:
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
