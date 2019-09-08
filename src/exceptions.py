class JobInvalidException(Exception):
    """
    Base exception for an invalid job, used to notify the Manager
    that a user's CI template is invalid. Exceptions should identify
    the problem uniquely. IE: invalid format, naming, etc.
    """
    pass

class JobInvalidFormatException(JobInvalidException):
    pass

