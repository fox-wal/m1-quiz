import file_handling as files
from quiz import do_quiz
from scores import save_and_view_scores
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

final_score = do_quiz(settings, questions)

save_and_view_scores(name, settings.get_score_file_path, final_score)

print(DisplayText.GOODBYE)
