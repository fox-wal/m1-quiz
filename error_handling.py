class ErrorMessages:
    '''
    A class containing error messages.

    Attributes:
        PROGRAM_ABENDED : str
            Inform the user that the program has abended.
        FILE_NOT_FOUND : str
            Error message for when a file has not been found.

            Arguments:

            1. File path.
        FILE_INCOMPLETE : str
            Error message for when a file does not contain all the expected content.

            Arguments:

            1. File path
        FILE_CORRUPTED : str
            Error message for when a file is incorrectly formatted.

            Arguments:

            1. File path
    '''

    PROGRAM_ABENDED : str
    FILE_NOT_FOUND : str
    FILE_INCOMPLETE : str
    FILE_CORRUPTED : str

def abend(error_message):
    '''
    Ends the program after displaying an error message to the user.

    Parameters:
        error_message
            A message containing details of why the program has abnormally ended.
    '''
    print(ErrorMessages.PROGRAM_ABENDED, error_message)
    exit()
