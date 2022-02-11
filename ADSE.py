from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import numpy as np



def addFile(): #Function to open the filedialog and prompt the user to choose a file to upload into the application
        filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("CSVs", "*.csv"), ("all files", "*.*")))
        data = pd.read_csv(filename, header=0)
        fileNameLabel["text"] = filename
        readColumns(data)

def readColumns(data): #Function to read columns from csv and create a list of those columns
    columns = list
    columns = data.columns.values
    displayData(columns, data)

def displayData(columns, data): #Function that displays csv data in the preview
    clear_data()
    tv1["columns"] = columns
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)
    df_rows = data.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values=row)
    displayDropdown(columns, data)

def clear_data(): #Function that clears the preview so that it can be repopulated
    tv1.delete(*tv1.get_children())

def displayDropdown(columns, data): #Function that displays the dropdown to choose the business object
    BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier"]
    objectChoice = tk.StringVar()
    objectChoice.set("--Business Object--")
    global dropdownLabel
    global objectDropdown
    dropdownLabel = tk.Label(middleWrapper, text="Select the Business Object that corresponds with your file:")
    objectDropdown = tk.OptionMenu(middleWrapper, objectChoice, *BUSINESSOBJECTS)
    dropdownLabel.pack()
    objectDropdown.pack()
    global confirmObjectBTN
    confirmObjectBTN = tk.Button(middleWrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: searchColumns(columns, data, objectChoice))
    confirmObjectBTN.pack(expand = "true")

def searchColumns(columns, data, objectChoice): #Function that searches through the data's columns to find the ones that match the business object they want to scramble
    print(columns)
    if objectChoice.get() == "Street Address":
        possibleColumns = [col for col in columns if 'Street' in col or "street" in col]
        selectColumns(possibleColumns, data, objectChoice)
    elif objectChoice.get() == "Email Address":
        possibleColumns = [col for col in columns if 'Email' in col]
        selectColumns(possibleColumns, data, objectChoice)
    elif objectChoice.get() == "Phone Number":
        possibleColumns = [col for col in columns if 'Phone' in col]
        selectColumns(possibleColumns, data, objectChoice)
    elif objectChoice.get() == "National Identifier":
        possibleColumns = [col for col in columns if 'SSN' in col]
        selectColumns(possibleColumns, data, objectChoice)
    else:
        global message
        message = Label(middleWrapper, text = "You must select a Business Object Type", fg = "red")
        message.pack()

def selectColumns(possibleColumns, data, objectChoice): #Function that creates radio buttons and allows user to select the column they want to affect
    columnV = {}
    columnWidgetYes = {}
    columnWidgetNo = {}
    columnNames = {}

    for i in possibleColumns:
        v = tk.IntVar()
        v.set(0)
        columnName = tk.Label(middleWrapper, text="Column Name: "+ i)
        columnRadioYes = tk.Radiobutton(middleWrapper, text="Scramble this Column", variable=v, value=1)
        columnRadioNo = tk.Radiobutton(middleWrapper, text="Don't Scramble this Column", variable=v, value=0)
        columnName.pack()
        columnRadioYes.pack()
        columnRadioNo.pack()
        columnV[i] = v
        columnWidgetYes[i] = columnRadioYes
        columnWidgetNo[i] = columnRadioNo
        columnNames[i] = columnName
    global confirmColumnBTN
    confirmColumnBTN = tk.Button(middleWrapper, text="Confirm these are the columns you want to change", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: createConfigLog(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns))
    confirmColumnBTN.pack(expand = "true")

def createConfigLog(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns): #Function that creates config log and selects target column
    configDict = {}
    for i in possibleColumns:
        configDict[i] = columnV[i].get()
    print(configDict)
    for i in configDict:
        if configDict[i] == 1:
            targetColumn = configDict[i]
    generateData(data, objectChoice, targetColumn)

def generateData(data, objectChoice, targetColumn): #Function that reads business object choice and directs data to corresponding generate function
    if objectChoice.get() == "Street Address":
        generateStreetAddress(data, targetColumn)
    elif objectChoice.get() == "Email Address":
        generateEmailAddress(data, targetColumn)
    elif objectChoice.get() == "Phone Number":
        generatePhoneNumber(data, targetColumn)
    else:
        generateNationalIdentifier(data, targetColumn)

def generateStreetAddress(data, targetColumn):           #Function that generates street addresses
    #Generate Street Address Function
    return NONE

def generateEmailAddress(data, targetColumn):            #Function that generates email addresses
    #Generate Email Address Function
    return NONE

def generatePhoneNumber(data, targetColumn):             #Function that generates phone numbers
    #Generate Phone Number Function
    return NONE

def generateNationalIdentifier(data, targetColumn):      #Function that generates national identifiers
    #Generate National Identifier Function
    return NONE

def main():                                         #Everything within this "main()" Function is the actual application
    root = Tk()                                     #initializes the window and names it "root"

    global topWrapper                               #Makes the topWrapper a global variable so that it can be accessed in any Function
    global middleWrapper                            #Makes the middleWrapper a global variable so that it can be accessed in any Function
    global bottomWrapper                            #Makes the bottomWrapper a global variable so that it can be accessed in any Function
    global fileNameLabel                            #Makes the fileNameLabel a global variable so that it can be accessed in any Function
    global tv1                                      #Makes the treeview a global variable so that it can be accessed in any Function

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