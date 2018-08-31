import db
from model import Task
import sqlite3 as sqlite
import sys

DB = db.database()

if len(sys.argv) == 1:
    print("arguments are: ls | add [task name] | rm [task id] | help")
    sys.exit(0)

command = sys.argv[1]

# TODO: fill out commands

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


def print_table_contents():
    print('====================================================================')
    for task in DB.list_todo_table():
        print(task)
    print('--------------------------------------------------------------------\n')