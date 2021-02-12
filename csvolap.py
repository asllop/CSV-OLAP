from tkinter import *
from pandastable import Table
import pandas as pd

def cmd_eval(event):
    print("COMMAND = " + cmd_input.get())
    try:
        pt.model.df = eval(cmd_input.get())
        pt.redraw()
    except:
        print("Invalid command!")

if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " CSV_FILE")
    print()
    sys.exit()

window = Tk()
window.title("CSV-OLAP v0.1.0")
cmd_input = Entry(window)
cmd_input.pack(fill=X)
cmd_input.bind("<Return>", cmd_eval)
parent = Frame(window)
parent.pack(expand=1, fill=BOTH)

df = pd.read_csv(sys.argv[1])
pt = Table(parent, dataframe=df)
pt.show()

model = pt.model.df

window.mainloop()
