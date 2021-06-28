# CSV-OLAP v0.6
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

csv_olap_version = "0.6"

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

def setup_window(csv_path):
    global cmd_input
    global model
    global pt

    window = Tk()
    window.title("CSV-OLAP v" + csv_olap_version + " - " + ntpath.basename(csv_path))
    cmd_input = Entry(window)
    cmd_input.pack(fill=X)
    cmd_input.bind("<Return>", cmd_eval)
    parent = Frame(window)
    parent.pack(expand=1, fill=BOTH)

    model = pd.read_csv(csv_path)
    model = clean_strings(model)

    pt = Table(parent, dataframe=model)
    pt.show()

    return window

def main(args):
    global cmd_type

    cmd_type = "sql"

    if len(args) < 2:
        print("Usage: " + args[0] + " CSV_FILE [-l SQL|PANDAS]")
        print()
        sys.exit()
        
    if len(args) == 4:
        if args[2] == "-l":
            cmd_type = args[3].lower()

    window = setup_window(args[1])

    if cmd_type == "sql":
        cmd_input.insert(0, 'SELECT * FROM model')
    elif cmd_type == "pandas":
        cmd_input.insert(0, 'model')

    window.mainloop()

if __name__ == "__main__":
    main(sys.argv)