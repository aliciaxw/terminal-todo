import db
from model import Task
import sqlite3 as sqlite
import sys

EXTRA_SPACING = 3 # change as you will

DB = db.database()

if len(sys.argv) == 1:
    print("arguments are: ls | add [task name] | rm [task id] | help")
    sys.exit(0)

command = sys.argv[1]

def print_task(task):
    """
    For formatting an individual task. Requires an input of a dict
    """
    print(str(task['id'])+create_spacing(task['id'], 'id')+str(task['desc']))

def create_spacing(item, column):
    """
    Returns the necessary amount of spacing to make things look nice
    Input item is the item you are finding the spacing after for
    Input column is the column you need to find spacing for
    """
    max_len = DB.length_longest_str(column)
    return ' ' * (max_len - len(str(item)) + EXTRA_SPACING)

def header_spacing(header, column):
    """
    Creates spacing for the headers
    """
    length = DB.length_longest_str(column) + EXTRA_SPACING
    return ' ' * (length - len(header))

    
def print_table_contents():
    """
    Prints the entirety of the todo table
    """
    print('====================================================================')
    print('ID' + header_spacing('ID', 'id') + 'TASK')
    print('--------------------------------------------------------------------')
    for task in DB.list_todo_table():
        print_task(task)
    print('--------------------------------------------------------------------')


if command == 'ls':
    print_table_contents()

elif command == 'add':
    if len(sys.argv) < 3:
        print("requires a task")
        sys.exit(0)
    DB.insert_todo_task(Task(sys.argv[2]))
    print_table_contents()

elif command == 'rm':
    if len(sys.argv) < 3:
        print("requires a task id")
        sys.exit(0)
    DB.delete_todo_task(int(sys.argv[2]))
    print_table_contents()

elif command == 'help':
    pass

else:
    print(command + " is not a valid option")