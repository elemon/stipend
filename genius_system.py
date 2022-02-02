"""
/****************************************************************
*                                                               *
*  Author: Jahi Miller                                          *
*  Title: Genius System                                         *
*                                                               *
*  Description: This program allows for the updating of         *
*  Genius Stipend and User Information via a form.              *
*  Notes:                                                       *
*  1.needs a quit button that closes everything                 *
*  2.needs listing of all comments                              *
*  3.diable update button until one of the fields is change     *
*    then enable it wish enables the upate.  Once clicked or    *
*    stepping to the next genius then disable it.               *
*                                                               *
****************************************************************/
"""

import sqlite3
from sqlite3 import Error

from tkinter import *
from tkinter import ttk

import datetime

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

def execute_read_query(connection, query):
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


############## PYTHON AND SQL SECTION ##############

def load_listbox(genius_name=None, table=None):
    global stipend_id
    query = ""
    mode = 0

    if table and not genius_name:
        query = "SELECT name from students order by name;"
    if table and genius_name:
        mode = 1
        query = """
            SELECT credit,debit,stipends.comment,student_id,stipends.created_at,sum(credit-debit),stipends.id
            FROM students JOIN stipends
            WHERE students.id = stipends.student_id
            AND students.name = '{0}';
        """.format(genius_name)
    if len(query) >= 1:
        records = execute_read_query(connection, query)
        if mode == 0:
            for row in records:
                id_choices.append(row[0])
            genius_name_vars.set(id_choices)
        elif mode == 1:
            stipend_id = records[0][-1]
            update_form(records)

def post(*args):
    try:
        column_values = [updated_at.get(),credit.get(),debit.get(),comment.get("1.0",END),student_id.get()]
        execute_query(connection,create_query(column_values))
    except Error as e:
        print(f"The error '{e}' occurred")

def create_query(val):
    return """
        UPDATE stipends
        SET updated_at="{0}",credit={1},debit={2},comment="{3}"
        WHERE id = {4};
    """.format(val[0],val[1],val[2],val[3],stipend_id)

def update_form(record):
    credit.delete(0, END)
    credit.insert(0, record[0][0])
    debit.delete(0, END)
    debit.insert(0, record[0][1])
    sum_lbl.configure(text="sum: {0}".format(record[0][5]))
    
    comment.delete(1.0, END)
    comment.insert(1.0, record[0][2])

    student_id.configure(state="default")
    student_id.delete(0, END)
    student_id.insert(0, record[0][3])
    student_id.configure(state="disabled")

    updated_at.configure(state="default")
    updated_at.delete(0, END)
    updated_at.insert(0, datetime.datetime.now())
    updated_at.configure(state="disabled")
    updated_at_lbl.configure(text="last updated: {}".format(record[0][4]))

###################################################################################
################ TKINTER WINDOW SECTION + Variable Declarations ###################
###################################################################################

#TKINTER SETUP VARIABLES 
root = Tk()
root.title("GENIUS DIRECTORY")
root.resizable(False, False)
root.after_idle(lambda: load_listbox(None, "stipends"))

window = ttk.Frame(root, padding="7", width=400, height=250)
window.grid(column=0, row=0, sticky=(N, W, E, S))

#SQLITE VARIABLES
connection = create_connection('genius_directory.sqlite3')
cursor = connection.cursor() #represents the db connection
stipend_id = None

#INPUT VARIABLES
id_choices = []
genius_name_vars = StringVar(value=id_choices)

credit_var = IntVar()
debit_var = IntVar()
student_id_var = IntVar()
updated_at_var = StringVar()


############## ENTRY WIDGETS SECTION ##############

credit_lbl = ttk.Label(window, text="credit: ")
credit = ttk.Entry(window, textvariable=credit_var)
credit_lbl.grid(column=0, row=0, sticky="w")
credit.grid(column=0, row=1, sticky="we")

debit_lbl = ttk.Label(window, text="debit: ")
debit = ttk.Entry(window, textvariable=debit_var)
debit_lbl.grid(column=0, row=2, sticky="w")
debit.grid(column=0, row=3, sticky="we")

sum_lbl = ttk.Label(window, text="sum: 0")
sum_lbl.grid(column=0, row=4, sticky="e")

comment_lbl = ttk.Label(window, text="comment: ")
comment = Text(window, width=40, height=10)
comment_lbl.grid(column=0, row=5, sticky="w")
comment.grid(column=0, row=6, sticky="we")

student_id_lbl = ttk.Label(window, text="student ID: ")
student_id = ttk.Entry(window, textvariable=student_id_var)
student_id_lbl.grid(column=0, row=7, sticky="w")
student_id.grid(column=0, row=8, sticky="we")
student_id.configure(state="disabled")

updated_at_lbl = ttk.Label(window, text="last updated: ")
updated_at = ttk.Entry(window, textvariable=updated_at_var)
updated_at_lbl.grid(column=0, row=9, sticky="w")
updated_at.grid(column=0, row=10, sticky="we")

############## SELECT BOX WIDGETS SECTION ##############

genius_name = Listbox(window, height=15, listvariable=genius_name_vars, exportselection=False)
genius_name.grid(column=2, row=0, sticky="nswe", rowspan=12, padx=(5, 5),)
genius_name.bind("<<ListboxSelect>>", lambda e: load_listbox(genius_name.get(genius_name.curselection()[0]), "stipends"))

############## BUTTON WIDGETS SECTION ##############

update_btn = Button(window, text="UPDATE", command=post)
update_btn.grid(column=0, row=11, sticky="we")