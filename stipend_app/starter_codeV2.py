"""
/****************************************************************
*                                                               *
* Author: Jahi Miller                                           *
*  Title: starter_codeV2                                          *
*                                                               *
*   1. Modify database name and root title name
    2. Modify character_table variable to stipends_table
    2. Modify Input Variables
       Modify cursor.execute value
       Delete load_viewer function
       Delete root.after_idle(load_viewer)
       Modify the the child Widgets
       Delete Vertical Divider code
       Delete Viewer 
       MODIFY Drop buttonn to Update


*                                                               *
****************************************************************/
"""

from tkinter import *
from tkinter import ttk
import sqlite3

######################### SQL METHODS SECTION ###################################

# Connect to Database
def create_connection(pathToDataBase):
    connection = None
    try:
        connection = sqlite3.connect(pathToDataBase)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        return false

"""
def execute_drop():
    print('dropping')
    if not execute_query(connection,'drop table CHARACTERS'):
        cursor.execute(stipends_table)
"""        

def execute_read_query(connection, query):
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


######################### SQL TABLE SECTION ###################################

stipends_table = """
CREATE table if not exists  stipends(
    name text,
    assignment text,
    day text,
    credit text,
    debit text,
    comment text
);
"""

######################### SQL + PYTHON SECTION ###################################

        
def post(*args):
    try:
        cursor.execute(stipends_table)
        
        profile = (name.get(),day.get(),assignment.get(),credit.get(), debit.get(),comment.get())
        print(len(profile))
        cursor.execute("INSERT into stipends(name,assignment,day,credit,debit,comment) values (?,?,?,?,?,?)", profile)
        
        connection.commit()
        cursor.close

    except ValueError:
        pass

'''
Modify this to update
def drop(*args):
    execute_drop()
    update_viewer(None)
'''
def update():
    print('Fields Updated')

#Inconveniencing piece of code
connection = create_connection('stipend_data')
cursor = connection.cursor() #represents the db connection
cursor.execute(stipends_table) #creates the db table []

###########################################################
################ TKINTER WINDOW SECTION ###################
###########################################################
    
#ROOT Setup
root = Tk()
root.title("Stipends")
root.resizable(False, False)
# root.after_idle(load_viewer)

#MainFrame Window 
window = ttk.Frame(root, padding="3 3 12 12", width=400, height=250)
window.grid(column=0, row=0, sticky=(N, W, E, S))

#Input Variables
name_var = StringVar()
day_var = StringVar()
assignment_var = StringVar()
credit_var = StringVar()
debit_var = StringVar()
comment_var = StringVar()

#Input Fields[Left Side]
name_lbl = ttk.Label(window, text="Name: ")
name = ttk.Entry(window, textvariable=name_var)
name_lbl.grid(column=1, row=0, sticky=W)
name.grid(column=1, row=1, sticky='we',columnspan=3)

day_lbl = ttk.Label(window, text="Date: ")
day = ttk.Entry(window, textvariable=day_var)
day_lbl.grid(column=1, row=2, sticky=W)
day.grid(column=1, row=3, sticky='we', columnspan=3)

assignment_lbl = ttk.Label(window, text="Assigment: ")
assignment = ttk.Entry(window, textvariable=assignment_var)
assignment_lbl.grid(column=1, row=4, sticky=W)
assignment.grid(column=1, row=5, sticky='we', columnspan=3)

credit_lbl = ttk.Label(window, text="Credit: ")
credit = ttk.Entry(window, textvariable=credit_var, width=15)
credit_lbl.grid(column=1, row=6, sticky=W)
credit.grid(column=1, row=7, sticky='we', columnspan=3)

debit_lbl = ttk.Label(window, text="Debit: ")
debit = ttk.Entry(window, textvariable=debit_var, width=3)
debit_lbl.grid(column=1, row=8, sticky=W)
debit.grid(column=1, row=9, sticky='we')

comment_lbl = ttk.Label(window, text="Comment: ")
comment = ttk.Entry(window, textvariable=comment_var, width=3)
comment_lbl.grid(column=1, row=10, sticky=W)
comment.grid(column=1, row=11, sticky='we')

#Buttons [Left Side]
update_btn = ttk.Button(window, text="UPDATE", command=update)
update_btn.grid(column=3, row=12, sticky=W)


post_btn = ttk.Button(window, text="POST", command=post, width=12)
post_btn.grid(column=1, row=12, sticky='we')

def empty_fields():
    character.delete(0, END)
    day.delete(0, END)
    assignment.delete(0, END)
    credit.delete(0, END)
    debit.delete(0, END)
    comment.delete(0,END)


        
root.mainloop()
