# CSV-OLAP v0.5
#
# Author: asllop
# Web: https://github.com/asllop/CSV-OLAP

#TODO: show file picker when no file is selected in the command line.
#TODO: add undo/redo arrows to go back to previous queries.
#TODO: support mouse/trackpad scrolling in the table.

from tkinter import *
from pandastable import Table
import pandasql as pdsql
import pandas as pd
import sys
import ntpath

cmd_type = "sql"

def cmd_eval(event):
    print("COMMAND = " + cmd_input.get())
    if cmd_type == "sql":
        pt.model.df = pdsql.sqldf(cmd_input.get())
        pt.redraw()
    elif cmd_type == "pandas":
        try:
            pt.model.df = eval(cmd_input.get())
            pt.redraw()
        except:
            print("Invalid command!")

def clean_strings(df):
    # Remove quotes
    df = df.rename(columns=lambda x: x.replace('"', ''))
    # Remove leading and trailing whitespaces
    df = df.rename(columns=lambda x: x.strip())
    return df

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " CSV_FILE [-l SQL|PANDAS]")
    print()
    sys.exit()
    
if len(sys.argv) == 4:
    if sys.argv[2] == "-l":
        cmd_type = sys.argv[3].lower()

window = Tk()
window.title("CSV-OLAP v0.5 - " + ntpath.basename(sys.argv[1]))
cmd_input = Entry(window)
cmd_input.pack(fill=X)
cmd_input.bind("<Return>", cmd_eval)
parent = Frame(window)
parent.pack(expand=1, fill=BOTH)

model = pd.read_csv(sys.argv[1])
model = clean_strings(model)

pt = Table(parent, dataframe=model)
pt.show()

if cmd_type == "sql":
    cmd_input.insert(0, 'SELECT * FROM model')
elif cmd_type == "pandas":
    cmd_input.insert(0, 'model')

window.mainloop()
