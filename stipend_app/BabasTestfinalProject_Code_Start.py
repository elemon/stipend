"""
/********************************************************************
*                                                               *
* Author: Jahi Miller                                           *
*  Title: Code from Animpedia v1 
        
    To be used assisting geniuses to create Stipend App Project                                     *
     Create Stipend App Table using DB Browser for SQLITE                                                    *
     Modify database name and root title name
     Modify character_table variable to stipends_table
     Modify Input Variables
     Delete update_viewer function
     Delete references to update_viewer function
     Delete Load_viewer function
     Modify cursor.execute parameter values to  
     Delete root.after_idle(load_viewer)
     Modify the the child Widgets and added needed widgets
     Delete Vertical Divider code
     Delete Viewer 
     MODIFY Drop button text to Update
     Modify Grid column and row values
     Add comment widget
     Modify SQL statements
     add field delete query as part of posting function*                                                               *
****************************************************************/
"""

from tkinter import *
from tkinter import ttk
import sqlite3

######################### Python METHODS SECTION ###################################

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

'''
def execute_drop():
    print('dropping')
    if not execute_query(connection,'drop table CHARACTERS'):
        cursor.execute(STIPENDS_table)
'''

######################### SQL CREATE TABLE SECTION ###################################

STIPENDS_table = """
CREATE table if not exists STIPENDS (
    name text,
    day text,
    assignment text,
    credit text,
    debit text,
    comment text
);
"""

######################### SQL + PYTHON SECTION ###################################

'''
def load_viewer(): #updates the viewer widget
    try:
        cursor.execute('Select character,title,ability,birthday,sex from STIPENDS')

#        update_viewer(cursor)
        
        connection.commit()
        cursor.close
    except ValueError:
        pass
'''
        
def post(*args):
    try:
        cursor.execute(STIPENDS_table)
        
        profile = (name.get(),day.get(),assignment.get(),credit.get(), debit.get(),comment.get())
        cursor.execute("INSERT into STIPENDS(name,day,assignment,credit,debit,comment) values (?,?,?,?,?,?)", profile)
        
        connection.commit()
        cursor.close
        empty_fields()
 #       load_viewer()
    except ValueError:
        pass
'''
def drop(*args):
    execute_drop()
#    update_viewer('')
'''    

###########################################################
################ TKINTER WINDOW SECTION ###################
###########################################################
    
#ROOT Setup
root = Tk()
root.title("STIPENDS")
root.resizable(False, False)

#MainFrame Window 
window = ttk.Frame(root, padding="3 3 12 12", width=400, height=250)
window.grid(column=0, row=0, sticky=(N, W, E, S))

#Inconveniencing piece of code
connection = create_connection('babasTestingProject')
cursor = connection.cursor() #represents the db connection
cursor.execute(STIPENDS_table) #creates the db table []


#Input Variables
name_var = StringVar()
day_var = StringVar()
assignment_var = StringVar()
credit_var = StringVar()
debit_var = StringVar()
comment_var = StringVar()

#Input Fields[Left Side]
name_lbl = ttk.Label(window, text="Name: ")
name_lbl.grid(column=1, row=0, sticky=W)
name = ttk.Entry(window, textvariable=name_var)
name.grid(column=1, row=1, sticky='we',columnspan=3)

day_lbl = ttk.Label(window, text="Date: ")
day_lbl.grid(column=1, row=2, sticky=W)
day = ttk.Entry(window, textvariable=day_var)
day.grid(column=1, row=3, sticky='we', columnspan=3)


assignment_lbl = ttk.Label(window, text="Assignment: ")
assignment_lbl.grid(column=1, row=4, sticky=W)
assignment = ttk.Entry(window, textvariable=assignment_var)
assignment.grid(column=1, row=5, sticky='we', columnspan=3)

credit_lbl = ttk.Label(window, text="Credit: ")
credit_lbl.grid(column=1, row=6, sticky=W)
credit = ttk.Entry(window, textvariable=credit_var, width=15)
credit.grid(column=1, row=7, sticky='we', columnspan=3)

debit_lbl = ttk.Label(window, text="Debit: ")
debit_lbl.grid(column=1, row=8, sticky=W)
debit = ttk.Entry(window, textvariable=debit_var, width=15)
debit.grid(column=1, row=9, sticky='we',columnspan=3)

comment_lbl = ttk.Label(window, text="Comment: ")
comment_lbl.grid(column=1, row=10, sticky=W)
comment = ttk.Entry(window, textvariable=comment_var, width=15)
comment.grid(column=1, row=11, sticky='we',columnspan=3)


#Buttons [Left Side]
update_btn = ttk.Button(window, text="Update", command='')
update_btn.grid(column=2, row=12, sticky=W)


#rand_btn = ttk.Button(window, text="UPDATE")
#rand_btn.grid(column=2, row=8, sticky=W)
#rand_btn.configure(state='disabled')

post_btn = ttk.Button(window, text="POST", command=post, width=10)
post_btn.grid(column=1, row=12, sticky='we')

######################### CENTER SECTION ###################################

'''
#Vertical Divider [Center]
divider = ttk.Separator(window, orient=VERTICAL)
divider.grid(column=4, row=0, rowspan=9, sticky='ns')
'''

def empty_fields():
    name.delete(0, END)
    day.delete(0, END)
    assignment.delete(0, END)
    credit.delete(0, END)
    debit.delete(0, END)
    comment.delete(0, END)

######################### RIGHT SECTION ###################################

#Record Container [Right]
#view of the records as they are added
"""
viewer = Listbox(window, width=40, height=10)
viewer.grid(column=5, row=0, rowspan=9, sticky='ns')
"""

'''
viewer = Text(window, width=50, height=10)
viewer.grid(column=5, row=0, rowspan=9, sticky='ns')#expands it from top to bottom
viewer.configure(state="disabled") #disables the textbox so users cannot make changes
'''

'''
def update_viewer(characters): #called by load_viewer()
    
    viewer.configure(state="normal") #enables the textbox so that the program make changes
    viewer.delete("0.0","end") #deletes everything in the textbox

    if STIPENDS:
        for row in STIPENDS:
            message = str(row) + "\n" 
            viewer.insert('end', message)
            print(message)        
    
    empty_fields()
    viewer.configure(state="disabled")
'''        
root.mainloop()
