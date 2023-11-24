class Errors:

    PROGRAM_ABENDED : str
    '''Inform the user that the program has abended.'''
    FILE_NOT_FOUND : str
    '''
    Error message for when a file has not been found.

    Arguments:

    1. File path.
    '''
    FILE_INCOMPLETE : str
    '''
    Error message for when a file does not contain all the expected content.

    Arguments:

    1. File path
    '''
    FILE_CORRUPTED : str
    '''
    Error message for when a file is incorrectly formatted.

    Arguments:

    1. File path
    '''

def abend(error_message):
    print(PROGRAM_ABENDED, error_message)
    exit()
