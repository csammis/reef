""" Custom exceptions to wrap what SQLAlchemy throws """

class InUseException(Exception):
    """ An exception to be thrown when a foreign key violation occurs """
    pass
