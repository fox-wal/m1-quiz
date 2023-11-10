PROGRAM_ABENDED = "Program abended:"

# During Quiz

WELCOME = """
                        -----+-----

                      Welcome to the

     QQQQQQQQQQ  UUUU    UUUU IIIIIIIIIIII ZZZZZZZZZZZZ
    QQQQQQQQQQQQ UUUU    UUUU IIIIIIIIIIII ZZZZZZZZZZZZ
    QQQQ    QQQQ UUUU    UUUU     IIII            ZZZZ
    QQQQ    QQQQ UUUU    UUUU     IIII          ZZZZ
    QQQQ    QQQQ UUUU    UUUU     IIII        ZZZZ
    QQQQ  Q QQQQ UUUU    UUUU     IIII      ZZZZ
    QQQQQQQQQQQ  UUUUUUUUUUUU IIIIIIIIIIII ZZZZZZZZZZZZ
     QQQQQQQQ QQ  UUUUUUUUUU  IIIIIIIIIIII ZZZZZZZZZZZZ

                        -----+-----
"""
NAME_PROMPT = "Name: "
QUESTION_LINE = "\nQuestion {} of {}: {}\n"
MULTI_CHOICE_OPTION_WITH_INDEX_LINE = "{}. {}"
MULTI_CHOICE_INDEX_PROMPT = "\nEnter the index of the correct answer: "
TYPE_IN_ANSWER_PROMPT = "\nType in the correct answer: "
INCORRECT = "Incorrect. {} attempts remaining."
CORRECT = "Correct! [+{}]"
SCORE_SO_FAR = "Total score: {}"

# After Quiz

RESULTS = """
+---------------End of Quiz---------------+

Questions answered correctly: {} out of {}.
Score: {} out of {}.
Adjusted score: {}

+-----------------------------------------+
"""

# Scores

YES = "Y"
NO = "N"
YES_NO_PROMPT_SEPARATOR = "/"
YES_NO_ERROR_PROMPT_SEPARATOR = " or "
YES_NO = [YES, NO]

SAVE_SCORE_PROMPT = "Would you like to save your score? [{}]"

TIME_STAMP_FORMAT = "{:%Y-%m-%d %H:%M:%S%z}"
SCORE_FILE_CREATED = "Score file created."
OVERWRITE_CORRUPTED_FILE = "This will override the corrupted file."
SCORE_SAVED = "Score saved!"
VIEW_YOUR_SCORES_PROMPT = "Would you like to view all your saved scores? [{}]"
SCORE_VIEW_HEADER = """Timestamp        Score
----------------------"""
SCORE_FORMAT = "{}   {:3d}"

GOODBYE = "\nGoodbye!"
