import random

class Task(object):
    """
    Creates a new todo item
    """
    def __init__(self, desc, due_date=None, due_time=None):
        self.desc        = desc
        self.due_date    = due_date
        self.due_time    = due_time

    def to_dict(self):
        """
        Dictionary representation of the todo item
        """
        return vars(self)