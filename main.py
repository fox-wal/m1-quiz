from random import shuffle
import file_handling as files
from scores import save_and_view_scores
from quiz import Quiz
from display_text import DisplayText
from prompts import Prompts

def get_user_name() -> str:
    '''
    Prompt the user to enter a valid name until they do so.

    Returns:
        Valid user name.
    '''
    while True:
        name = input(Prompts.NAME)
        if '"' in name:
            print(DisplayText.INVALID_CHARACTER.format('"'))
        else:
            return name

#---------------#
# PROGRAM START #
#---------------#

settings, questions = files.load_essential_files()

print(DisplayText.WELCOME)
name = get_user_name()

shuffle(questions)
quiz = Quiz(questions[:settings.get_number_of_questions], settings.get_multiple_choice, settings.get_select_using_index, settings.get_number_of_attempts)
quiz.start()

save_and_view_scores(name, settings.get_score_file_path, quiz.get_final_score)

print(DisplayText.GOODBYE)
