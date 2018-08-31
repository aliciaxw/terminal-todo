import os.path
import sqlite3 as sqlite
import sys
from model import Task

# TODO: better output formatting
# TODO: due date support

class database(object):
    """
    Database driver for the todo table
    """
    def __init__(self):
        self.conn = sqlite.connect('ttd_todo.db')
        self.create_todo_table()


    def create_todo_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE todo
                (id INT NOT NULL, 
                desc TEXT NOT NULL,
                due_date TEXT,
                due_time TEXT);
            """)
        except Exception as e:
            #print(e)
            pass
            

    def delete_todo_table(self):
        self.conn.execute("""DROP TABLE todo;""")
        self.conn.commit()


    def insert_todo_task(self, task):
        """
        Inserts a new task into the todo table. Also increments ID
        when necessary.
        """
        next_id = self.get_largest_id() + 1
        self.conn.execute("""
            INSERT INTO todo (id, desc, due_date, due_time)
            VALUES (?, ?, ?, ?);
        """, (next_id, task.desc, task.due_date, task.due_time))
        self.conn.commit()


    def list_todo_table(self):
        """
        Returns the list of tasks in the todo table. If empty, returns an empty list.
        """
        if self.is_todo_table_empty():
            print("nothing to do!")
            return []
        else:
            cur = self.conn.execute("""SELECT * FROM todo;""")
            lst = []
            for row in cur:
                task = {}
                task['id']            = row[0]
                task['desc']          = row[1]
                task['due_date']      = row[2]
                task['due_time']      = row[3]
                lst.append(task)
            return lst


    def delete_todo_task(self, id):
        """
        Removes a task from the todo table by id
        """
        if self.is_todo_table_empty() == False:
            if id > self.get_largest_id() or id < 0:
                print("\ntask with id %s does not exist\n" % id)
            else:
                self.conn.execute("""DELETE FROM todo WHERE id=?;""", str(id))
                self.decrement_todo_task_ids(id)
                self.conn.commit()
        else:
            print("\nno tasks to delete!\n")


    def delete_all_todo_tasks(self, id):
        """
        Removes all tasks from the todo table but not the table itself
        """
        self.conn.execute("""DELETE FROM todo;""")
        self.conn.commit()

    
    def get_largest_id(self):
        """
        Helper function. Returns the id (int) with the maximum value.
        """
        try:
            cur = self.conn.execute("""SELECT MAX(id) FROM todo;""")
            row = cur.fetchone()
            if row[0] == None:
                return 0
            else:
                return row[0]
        except Exception as e:
            print(e)


    def decrement_todo_task_ids(self, id_removed):
        """
        Decrements by 1 all ids greater than id_removed
        """
        self.conn.execute("""UPDATE todo SET id=id-1 WHERE id>?;""", str(id_removed))
        self.conn.commit()


    def is_todo_table_empty(self):
        """
        Returns if the todo table has any data in it, assuming it exists
        """
        cur = self.conn.execute("""SELECT COUNT(*) FROM todo;""")
        if cur != None:
            row = cur.fetchone()
            if row[0] == 0:
                return True
            else:
                return False
        print("is_todo_table_empty: table does not exist")
