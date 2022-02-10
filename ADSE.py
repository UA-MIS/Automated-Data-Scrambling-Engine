from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import numpy as np



def addFile():                                      #Method to open the filedialog and prompt the user to choose a file to upload into the application
        filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("CSVs", "*.csv"), ("all files", "*.*")))
        data = pd.read_csv(filename, header=0)
        fileNameLabel["text"] = filename
        readColumns(data)

def readColumns(data):
    columns = list
    columns = data.columns.values
    displayColumns(columns, data)
    print(columns)

def displayColumns(columns, data):
    clear_data()
    tv1["column"] = columns
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)
    df_rows = data.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values=row)

def clear_data():
    tv1.delete(*tv1.get_children())


def main():                                         #Everything within this "main()" method is the actual application
    root = Tk()                                     #initializes the window and names it "root"

    global topWrapper
    global bottomWrapper
    global fileNameLabel
    global tv1

    titleText = Label(root, text="Welcome to the Automated Data Scrambling Engine!") #Text that appears at top of application
    topWrapper = LabelFrame(root, text="Preview")                                    #Upper section
    bottomWrapper = LabelFrame(root, text="Current File")                            #Lower section
    fileNameLabel = Label(bottomWrapper, text="No file selected")
    tv1 = ttk.Treeview(topWrapper)
    treescrolly = tk.Scrollbar(tv1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
    treescrollx = tk.Scrollbar(tv1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
    
    

    titleText.pack(fill="both", expand="yes", padx=20, pady=20)
    topWrapper.pack(fill="both", expand="yes", padx=20, pady=20)
    bottomWrapper.pack(fill="both", expand="yes", padx=20, pady=20)
    fileNameLabel.pack()
    tv1.pack(fill="both", expand="yes", padx=20, pady=20)
    treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
    treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

    openFileBTN = tk.Button(bottomWrapper, text="Choose a File for Scrambling", padx=10, pady=5, fg="white", bg="dark blue", command=addFile)
    openFileBTN.pack(expand = "true")


    root.title("Automated Data Scrambling Engine")  #Sets window title to the name of our project
    root.geometry("800x700")
    root.mainloop()                                 #keeps window open and running
    


if __name__ == "__main__": #Checks to make sure the file is being run as a script and not imported into another file. (Basic Python Boilerplate)
    main()