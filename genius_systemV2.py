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

########## Jahi why is this here its not called #######
def execute_drop(table):
    print('dropping')
    if not execute_query(connection,'drop table {0}'.format(table)):
        cursor.execute(characters_table)
        

def execute_read_query(connection, query):
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


############## PYTHON AND SQL SECTION ##############

def load_listbox(stipendID=None, table=None):
    query = ""
    mode = 0
    
    if table and not stipendID:
#        query = "SELECT {0}.id,students.name from {0} JOIN students WHERE {0}.student_id == students.id order by name;".format(table)
        query = "SELECT stipends.id,students.name from stipends JOIN students WHERE stipends.student_id = students.id order by name;"

################ Jahi you need a comment to explain how this section work ########## 
    if table and stipendID:
        mode = 1
        query = "SELECT * from {0} WHERE id == {1}".format(table, stipendID)

    if len(query) >= 1:
        records = execute_read_query(connection, query)
        if mode == 0:
            for row in records:
                id_choices.append("[{0}]: {1}".format(row[0],row[1]))
            id_vars.set(id_choices)
        elif mode == 1:
            update_form(records)
#####################################################################################

def post(stipendID):
    try:
        column_values = [stipendID,updated_at.get(),credit.get(),debit.get(),comment.get("1.0",END),student_id.get()]
        #print(create_query(column_values))
        execute_query(connection,create_query(column_values))
    except Error as e:
        print(f"The error '{e}' occurred")

def create_query(val):
    return """
        UPDATE stipends
        SET updated_at="{0}",credit={1},debit={2},comment="{3}",student_id={4}
        WHERE id={5};
    """.format(val[1],val[2],val[3],val[4],val[5],val[0])

def get_id(id_str):
    stipendID = ""
    for char in id_str:
        if char.isnumeric():
            stipendID+=char
    return stipendID
            

def update_form(record):
    credit.delete(0, END)
    credit.insert(0, record[0][2]) ### Jahi these need explaining  ######
    debit.delete(0, END)
    debit.insert(0, record[0][3])  ### Jahi these need explaining  ######
    comment.delete(1.0, END)
    comment.insert(1.0, record[0][4]) ### Jahi these need explaining  ######
    student_id.delete(0, END)
    student_id.insert(0, record[0][5])  ### Jahi these need explaining  ######

    
    updated_at.delete(0, END)
    updated_at.insert(0, datetime.datetime.now())
    updated_at_lbl.configure(text="last updated: {}".format(record[0][-1]))

###################################################################################
################ TKINTER WINDOW SECTION + Variable Declarations ###################
###################################################################################

#TKINTER SETUP VARIABLES 
root = Tk()
root.title("GENIUS DIRECTORY")
root.after_idle(lambda: load_listbox(None, "stipends"))

window = ttk.Frame(root, padding="5", width=400, height=250)
window.grid(column=0, row=0, sticky=(N, W, E, S))

#SQLITE VARIABLES
connection = create_connection('genius_directoryV2.sqlite3')
cursor = connection.cursor() ####### represents the db connection #######

#INPUT VARIABLES
id_choices = []
id_vars = StringVar(value=id_choices)


######### Jahi when instructing 
######### spend some time explaining these tinker Classes
credit_var = IntVar()
debit_var = IntVar()
student_id_var = IntVar()
updated_at_var = StringVar()


############## ENTRY WIDGETS SECTION ##############

credit_lbl = ttk.Label(window, text="credit: ")
credit = ttk.Entry(window, textvariable=credit_var)
credit_lbl.grid(column=0, row=4, sticky="w")
credit.grid(column=0, row=5, sticky="we")

debit_lbl = ttk.Label(window, text="debit: ")
debit = ttk.Entry(window, textvariable=debit_var)
debit_lbl.grid(column=0, row=6, sticky="w")
debit.grid(column=0, row=7, sticky="we")

comment_lbl = ttk.Label(window, text="comment: ")
comment = Text(window, width=40, height=10)
comment_lbl.grid(column=0, row=8, sticky="w")
comment.grid(column=0, row=9, sticky="we")

student_id_lbl = ttk.Label(window, text="student ID: ")
student_id = ttk.Entry(window, textvariable=student_id_var)
student_id_lbl.grid(column=0, row=10, sticky="w")
student_id.grid(column=0, row=11, sticky="we")

updated_at_lbl = ttk.Label(window, text="last updated: ")
updated_at = ttk.Entry(window, textvariable=updated_at_var)
updated_at_lbl.grid(column=0, row=14, sticky="w")
updated_at.grid(column=0, row=15, sticky="we")


############## SELECT BOX WIDGETS SECTION ##############

stipendID = Listbox(window, height=19, listvariable=id_vars)
stipendID.grid(column=0, row=1, sticky="we")
stipendID.bind("<<ListboxSelect>>", lambda e: load_listbox(get_id(stipendID.get(stipendID.curselection()[0])), "stipends"))
'load_listbox(stipendID.get(stipendID.curselection()[0]), "stipends")'
############## BUTTON WIDGETS SECTION ##############

##############################################
# Jahi you can add code to the post Function #
# that traverses the genius stipend records  #
# and sums the credit and debit fields and   #
# then shows the stipend balance.  The field #
# does not have to in the database           #
##############################################  
update_btn = Button(window, text="UPDATE", command=lambda: post(get_id(stipendID.get(stipendID.curselection()[0]))))
update_btn.grid(column=0, row=16, sticky="we")
