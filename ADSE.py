from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import numpy as np



def addFile(): #Method to open the filedialog and prompt the user to choose a file to upload into the application
        filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("CSVs", "*.csv"), ("all files", "*.*")))
        data = pd.read_csv(filename, header=0)
        fileNameLabel["text"] = filename
        readColumns(data)

def readColumns(data): #Method to read columns from csv and create a list of those columns
    columns = list
    columns = data.columns.values
    displayData(columns, data)

def displayData(columns, data): #Method that displays csv data in the preview
    clear_data()
    tv1["columns"] = columns
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)
    df_rows = data.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values=row)

def clear_data(): #Clears the preview so that it can be repopulated
    tv1.delete(*tv1.get_children())


def main():                                         #Everything within this "main()" method is the actual application
    root = Tk()                                     #initializes the window and names it "root"

    global topWrapper                               #Makes the topWrapper a global variable so that it can be accessed in any method
    global middleWrapper                            #Makes the middleWrapper a global variable so that it can be accessed in any method
    global bottomWrapper                            #Makes the bottomWrapper a global variable so that it can be accessed in any method
    global fileNameLabel                            #Makes the fileNameLabel a global variable so that it can be accessed in any method
    global tv1                                      #Makes the treeview a global variable so that it can be accessed in any method

    titleText = Label(root, text="Welcome to the Automated Data Scrambling Engine!") #Creates text that appears at top of application
    topWrapper = LabelFrame(root, text="Preview")                                    #Creates preview Section
    middleWrapper = LabelFrame(root, text="Configuration")                           #Creates configure Section
    bottomWrapper = LabelFrame(root, text="Current File")                            #Creates select File section
    fileNameLabel = Label(bottomWrapper, text="No file selected")                    #Creates text for selected file name
    tv1 = ttk.Treeview(topWrapper)                                                   #Creates treeview for previewing data
    openFileBTN = tk.Button(bottomWrapper, text="Choose a File for Scrambling",      #Creates Open File Button
    padx=10, pady=5, fg="white", bg="dark blue", command=addFile)
    treescrolly = tk.Scrollbar(tv1, orient="vertical", command=tv1.yview)            #Updates the y-axis view of the widget
    treescrollx = tk.Scrollbar(tv1, orient="horizontal", command=tv1.xview)          #Updates the x-axis view of the widget
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)    #Assigns the scrollbars to the Treeview
    
    

    titleText.pack(fill="both", expand="yes", padx=20, pady=20)      #Places title text widget in window
    topWrapper.pack(fill="both", expand="yes", padx=20, pady=20)     #Places topWrapper label frame in window
    middleWrapper.pack(fill="both", expand="yes", padx=20, pady=20)  #Places middleWrapper label frame in window
    bottomWrapper.pack(fill="both", expand="yes", padx=20, pady=20)  #Places bottomWrapper label frame in window
    fileNameLabel.pack()                                             #Places fileName Label in bottomWrapper frame
    tv1.pack(fill="both", expand="yes", padx=20, pady=20)            #Places treeview in topWrapper frame
    treescrollx.pack(side="bottom", fill="x")                        #Makes the scrollbar fill the x axis of the Treeview widget
    treescrolly.pack(side="right", fill="y")                         #Makes the scrollbar fill the y axis of the Treeview widget
    openFileBTN.pack(expand = "true")                                #Places the Open File Button in bottomWrapper frame


    root.title("Automated Data Scrambling Engine")  #Sets window title to the name of our project
    root.geometry("800x700")                        #Sets window size to 800x700 pixels
    root.mainloop()                                 #Keeps window open and running
    


if __name__ == "__main__": #Checks to make sure the file is being run as a script and not imported into another file. (Basic Python Boilerplate)
    main()