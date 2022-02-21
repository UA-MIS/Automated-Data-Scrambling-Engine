from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import numpy as np
import faker as faker
import random

fake = faker.Faker()

def fileType(fileTypeChoice):
    fileType = fileTypeChoice.get()
    if fileType == ".CSV":
        addCSVFile()
    elif fileType == ".DAT":
        delimChoice = StringVar()
        delimEntryLabel = Label(bottomWrapper, text = "Please enter the delimiter your file uses:")
        delimEntry = Entry(bottomWrapper, textvariable = delimChoice)
        delimConfirmBTN = Button(bottomWrapper, text="Confirm Delimiter", command = lambda: addDATFile(delimChoice))
        delimEntryLabel.pack()
        delimEntry.pack()
        delimConfirmBTN.pack()

def addDATFile(delimChoice):
    fileName = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("DAT", "*.dat"), ("all files", "*.*")))
    print(delimChoice.get())
    data = pd.read_csv(fileName, header=0, sep=delimChoice.get())
    print(fileName)
    fileNameLabel["text"] = fileName
    clearBottomFrame()
    readColumns(data)


def addCSVFile(): #Function to open the filedialog and prompt the user to choose a file to upload into the application
    fileName = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("CSVs", "*.csv"), ("all files", "*.*")))
    data = pd.read_csv(fileName, header=0)
    print(fileName)
    fileNameLabel["text"] = fileName
    clearBottomFrame()
    readColumns(data)

def clearTopFrame():
    for widget in topWrapper.winfo_children():
        widget.destroy()

def clearMiddleFrame():
    for widget in middleWrapper.winfo_children():
        widget.destroy()

def clearBottomFrame():
    for widget in bottomWrapper.winfo_children():
        widget.destroy()

def readColumns(data): #Function to read columns from csv and create a list of those columns
    columns = list
    columns = data.columns.values
    clearMiddleFrame()
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

def updateData(data): #Function that updates data in the preview
    clear_data()
    df_rows = data.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values=row)

def clear_data(): #Function that clears the preview so that it can be repopulated
    tv1.delete(*tv1.get_children())

def displayDropdown(columns, data): #Function that displays the dropdown to choose the business object
    BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier"]
    objectChoice = StringVar()
    objectChoice.set("--Business Object--")
    global dropdownLabel
    global objectDropdown
    dropdownLabel = Label(middleWrapper, text="Select the Business Object that corresponds with your file:")
    objectDropdown = OptionMenu(middleWrapper, objectChoice, *BUSINESSOBJECTS)
    dropdownLabel.pack()
    objectDropdown.pack()
    global confirmObjectBTN
    confirmObjectBTN = Button(middleWrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: searchColumns(columns, data, objectChoice))
    confirmObjectBTN.pack(expand = "true")

def searchColumns(columns, data, objectChoice): #Function that searches through the data's columns to find the ones that match the business object they want to scramble
    print(columns)
    if objectChoice.get() == "Street Address":
        possibleColumns = [col for col in columns if 'Street' in col]
        print(possibleColumns)
        if bool(possibleColumns) == True:
            selectStreetAddress(possibleColumns, data, objectChoice, columns)
        else:
            columnNotFoundLabel = Label(middleWrapper, text = "There were not any columns matching that business object. Please select a different object.")
            columnNotFoundLabel.pack()
    elif objectChoice.get() == "Email Address":
        possibleColumns = [col for col in columns if 'Email' in col]
        if bool(possibleColumns) == True:
            selectDomain(possibleColumns, data, objectChoice, columns)
        else:
            columnNotFoundLabel = Label(middleWrapper, text = "There were not any columns matching that business object. Please select a different object.")
            columnNotFoundLabel.pack()
    elif objectChoice.get() == "Phone Number":
        possibleColumns = [col for col in columns if 'Phone' in col]
        if bool(possibleColumns) == True:
            selectColumns(possibleColumns, data, objectChoice, columns)
        else:
            columnNotFoundLabel = Label(middleWrapper, text = "There were not any columns matching that business object. Please select a different object.")
            columnNotFoundLabel.pack()
    elif objectChoice.get() == "National Identifier":
        possibleColumns = [col for col in columns if 'SSN' in col]
        if bool(possibleColumns) == True:
            selectColumns(possibleColumns, data, objectChoice, columns)
        else:
            columnNotFoundLabel = Label(middleWrapper, text = "There were not any columns matching that business object. Please select a different object.")
            columnNotFoundLabel.pack()
    else:
        global message
        message = Label(middleWrapper, text = "You must select a Business Object Type", fg = "red")
        message.pack()

def selectDomain(possibleColumns, data, objectChoice, columns):
    clearMiddleFrame()
    domainChoice = StringVar()
    domainEntryLabel = Label(middleWrapper, text = "Please enter the domain you want to use for generated data:")
    domainEntry = Entry(middleWrapper, textvariable = domainChoice)
    confirmDomainBTN = Button(middleWrapper, text="Confirm Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: selectColumnsEmail(possibleColumns, data, objectChoice, columns, domainChoice))
    domainEntryLabel.pack()
    domainEntry.pack()
    confirmDomainBTN.pack()

def selectStreetAddress(possibleColumns, data, objectChoice, columns):
    clearMiddleFrame()
    streetChoice = StringVar()
    entryLabelStreet = Label(middleWrapper, text="Please enter the street address you want to use for generated data:")
    streetEntry = Entry(middleWrapper, textvariable=streetChoice)
    confirmStreetBTN = tk.Button(middleWrapper, text="Confirm Street Name", padx=10, pady=5, fg="white", bg="dark blue",
                                 command=lambda: displayStreetLineDropdown(possibleColumns, columns, data, objectChoice, streetChoice))
    entryLabelStreet.pack()
    streetEntry.pack()
    confirmStreetBTN.pack()

def displayStreetLineDropdown(possibleColumns, columns, data, objectChoice, streetChoice):  # Function that displays the dropdown to choose the business object
    clearMiddleFrame()
    STREETOBJECTS = ["10", "20", "50", "100"]
    frequencyChoice = tk.StringVar()
    frequencyChoice.set("--Street Address Line 2 Frequency--")
    global freqLabel
    global lineTwoFreqDropdown
    freqLabel = tk.Label(middleWrapper, text="Select the frequency of which you want :")
    lineTwoFreqDropdown = tk.OptionMenu(middleWrapper, frequencyChoice, *STREETOBJECTS)
    freqLabel.pack()
    lineTwoFreqDropdown.pack()
    global confirmStreetBTN
    confirmStreetBTN = tk.Button(middleWrapper, text="Confirm Street Line 2 Frequency Choice", padx=10, pady=5, fg="white",
                                 bg="dark blue", command=lambda: selectColumnsStreet(possibleColumns, data, objectChoice, columns,
                                                                     streetChoice, frequencyChoice))
    confirmStreetBTN.pack(expand="true")

def selectColumns(possibleColumns, data, objectChoice, columns): #Function that creates radio buttons and allows user to select the column they want to affect
    columnV = {}
    columnWidgetYes = {}
    columnWidgetNo = {}
    columnNames = {}
    clearMiddleFrame()

    for i in possibleColumns:
        v = IntVar()
        v.set(0)
        columnName = Label(middleWrapper, text="Column Name: "+ i)
        columnRadioYes = Radiobutton(middleWrapper, text="Scramble this Column", variable=v, value=1)
        columnRadioNo = Radiobutton(middleWrapper, text="Don't Scramble this Column", variable=v, value=0)
        columnName.pack()
        columnRadioYes.pack()
        columnRadioNo.pack()
        columnV[i] = v
        columnWidgetYes[i] = columnRadioYes
        columnWidgetNo[i] = columnRadioNo
        columnNames[i] = columnName
    global confirmColumnBTN
    confirmColumnBTN = Button(middleWrapper, text="Confirm configuration", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: createConfigLog(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns, columns))
    confirmColumnBTN.pack(expand = "true")

def selectColumnsEmail(possibleColumns, data, objectChoice, columns, domainChoice): #Function that creates radio buttons and allows user to select the column they want to affect
    columnV = {}
    columnWidgetYes = {}
    columnWidgetNo = {}
    columnNames = {}
    clearMiddleFrame()

    for i in possibleColumns:
        v = IntVar()
        v.set(0)
        columnName = Label(middleWrapper, text="Column Name: "+ i)
        columnRadioYes = Radiobutton(middleWrapper, text="Scramble this Column", variable=v, value=1)
        columnRadioNo = Radiobutton(middleWrapper, text="Don't Scramble this Column", variable=v, value=0)
        columnName.pack()
        columnRadioYes.pack()
        columnRadioNo.pack()
        columnV[i] = v
        columnWidgetYes[i] = columnRadioYes
        columnWidgetNo[i] = columnRadioNo
        columnNames[i] = columnName
    global confirmColumnBTN
    confirmColumnBTN = Button(middleWrapper, text="Confirm Configuration", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: createConfigLogEmail(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns, columns, domainChoice))
    confirmColumnBTN.pack(expand = "true")

def selectColumnsStreet(possibleColumns, data, objectChoice, columns,
                       streetChoice, frequencyChoice):  # Function that creates radio buttons and allows user to select the column they want to affect
    columnV = {}
    columnWidgetYes = {}
    columnWidgetNo = {}
    columnNames = {}
    clearMiddleFrame()

    for i in possibleColumns:
        v = tk.IntVar()
        v.set(0)
        columnName = tk.Label(middleWrapper, text="Column Name: " + i)
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
    confirmColumnBTN = tk.Button(middleWrapper, text="Confirm configuration", padx=10, pady=5, fg="white",
                                 bg="dark blue",
                                 command=lambda: createConfigLogStreet(data, objectChoice, columnV, columnWidgetYes,
                                                                      columnWidgetNo, columnNames, possibleColumns,
                                                                      columns, streetChoice, frequencyChoice))
    confirmColumnBTN.pack(expand="true")



def createConfigLog(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns, columns): #Function that creates config log and selects target column
    configDict = {}
    for i in possibleColumns:
        configDict[i] = columnV[i].get()
        columnWidgetYes[i].destroy()
        columnWidgetNo[i].destroy()
        columnNames[i].destroy()
        confirmColumnBTN.destroy()
    print(configDict)
    tColumn = [k for k, v in configDict.items() if v == 1]
    targetColumn = StringVar()
    targetColumn = tColumn[0]
    generateData(data, objectChoice, targetColumn, columns)

def createConfigLogEmail(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns, columns, domainChoice): #Function that creates config log and selects target column
    configDict = {}
    for i in possibleColumns:
        configDict[i] = columnV[i].get()
        columnWidgetYes[i].destroy()
        columnWidgetNo[i].destroy()
        columnNames[i].destroy()
        confirmColumnBTN.destroy()
    print(configDict)
    tColumn = [k for k, v in configDict.items() if v == 1]
    targetColumn = StringVar()
    targetColumn = tColumn[0]
    generateDataEmail(data, objectChoice, targetColumn, columns, domainChoice)

def createConfigLogStreet(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns,
                    columns, streetChoice, frequencyChoice):  # Function that creates config log and selects target column
    configDict = {}
    for i in possibleColumns:
        configDict[i] = columnV[i].get()
        columnWidgetYes[i].destroy()
        columnWidgetNo[i].destroy()
        columnNames[i].destroy()
        confirmColumnBTN.destroy()
    print(configDict)
    tColumn = [k for k, v in configDict.items() if v == 1]
    targetColumn = StringVar()
    targetColumn = tColumn[0]
    generateDataStreet(data, objectChoice, targetColumn, columns, streetChoice, frequencyChoice)


def generateData(data, objectChoice, targetColumn, columns): #Function that reads business object choice and directs data to corresponding generate function
    topLabel["text"] = "Data has been updated. You can export by clicking the 'Export Data' button below"
    global exportBTN
    global reorderBTN
    exportBTN = Button(bottomWrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: exportData(data))
    reorderBTN = Button(bottomWrapper, text = "Reorder Columns", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: reorderColumns(data, targetColumn))
    exportBTN.pack()
    reorderBTN.pack()
    if objectChoice.get() == "Street Address":
        generateStreetAddress(data, targetColumn)
        displayData(columns, data)
    elif objectChoice.get() == "Email Address":
        generateEmailAddress(data, targetColumn)
        displayData(columns, data)
    elif objectChoice.get() == "Phone Number":
        generatePhoneNumber(data, targetColumn)
        displayData(columns, data)
    else:
        generateNationalIdentifier(data, targetColumn)
        displayData(columns, data)

def generateDataEmail(data, objectChoice, targetColumn, columns, domainChoice): #Function that reads business object choice and directs data to corresponding generate function
    topLabel["text"] = "Data has been updated. You can export by clicking the 'Export Data' button below"
    global exportBTN
    global reorderBTN
    exportBTN = Button(bottomWrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: exportData(data))
    reorderBTN = Button(bottomWrapper, text = "Reorder Columns", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: reorderColumns(data, targetColumn))
    exportBTN.pack()
    reorderBTN.pack()
   
    generateEmailAddress(data, targetColumn, domainChoice)
    displayData(columns, data)

def generateDataStreet(data, objectChoice, targetColumn,
                 columns, streetChoice, frequencyChoice):  # Function that reads business object choice and directs data to corresponding generate function
    topLabel["text"] = "Data has been updated. You can export by clicking the 'Export Data' button below"
    global exportBTN
    global reorderBTN
    exportBTN = tk.Button(bottomWrapper, text="Export Data", padx=10, pady=5, fg="white", bg="dark blue",
                          command=lambda: exportData(data))
    reorderBTN = tk.Button(bottomWrapper, text="Reorder Columns", padx=10, pady=5, fg="white", bg="dark blue",
                           command=lambda: reorderColumns(data, targetColumn))
    exportBTN.pack()
    reorderBTN.pack()

    generateStreetAddress(data, columns, targetColumn, streetChoice, frequencyChoice)
    displayData(columns, data)
   

def generateStreetAddress(data, columns, targetColumn, streetChoice, frequencyChoice):  # Function that generates street addresses
    for i in data.index:
        data.at[i, targetColumn] = generate_streetaddress(streetChoice, frequencyChoice, i)
       

def generate_streetaddress(streetChoice, frequencyChoice, i):
    x = str(i)
    return x + " " + streetChoice.get()         #for each piece of data, create an address with their street name and incremented 

def generateEmailAddress(data, targetColumn, domainChoice):            #Function that generates email addresses
    domain = domainChoice.get()
    data[targetColumn] = data[targetColumn].apply(lambda x: x.split("@")[0] + "@" + domain)

def generatePhoneNumber(data, targetColumn):             #Function that generates phone numbers
    for i in data.index[0:-1]:
        if i % 1 == 0:
            data.at[i, targetColumn] = generatePhone()
    for i in data.index[0:-1]:
        if i % 3 == 1:
            data.at[i, targetColumn] = generate_phone_format()
    for i in data.index[0:-1]:
        if i % 5 == 1:
            data.at[i, targetColumn] = generate_phone_format_three()
   

def generateNationalIdentifier(data, targetColumn):      #Function that generates national identifiers
    for i in data.index:
        data.at[i, targetColumn] = generate_SSN()

def generate_SSN(): #Actual method that generates SSN's
    return fake.ssn()

def generatePhone(): #Actual method that generates phone numbers
    return fake.numerify("(###)-###-####")

def generate_phone_format(): #Actual method that generates phone numbers
    return fake.numerify("###-###-####")

def generate_phone_format_three(): #Actual method that generates phone numbers
    return fake.numerify("### ### ####")

def exportData(data):
    savePath = filedialog.asksaveasfile(mode='w', defaultextension=".dat")
    data.to_csv(savePath, sep = "|", index = False)
    print(savePath)
    if bool(savePath) == True:
        topLabel["text"] = "File succesfully exported."
    else:
        topLabel["text"] = "File failed to export."

    zipBTN = Button(middleWrapper, text="export as zip", command =lambda: zipFile(savePath))
    zipBTN.pack()
   
def zipFile(savePath):
    path = savePath.name
    print(path)
    

def reorderColumns(data, targetColumn):
    if targetColumn == "PhoneNumber":
        correctOrder = [targetColumn, "SourceSystemOwner", "SourceSystemID", "DateFrom", "DateTo", "PrimaryFlag", "PersonNumber", "PhoneType"]
        data = data[correctOrder]
        topLabel["text"] = "Columns have been reordered. You can export by clicking the 'Export Data' button below"
        readColumns(data)
        exportBTN.destroy()
        reorderBTN.destroy()
        exporttBTN = Button(bottomWrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: exportData(data))
        exporttBTN.pack()
    else:
        correctOrder = [targetColumn, "SourceSystemOwner", "SourceSystemID", "DateFrom", "DateTo", "PrimaryFlag", "PersonNumber"]
        data = data[correctOrder]
        topLabel["text"] = "Columns have been reordered. You can export by clicking the 'Export Data' button below"
        readColumns(data)
        exportBTN.destroy()
        reorderBTN.destroy()
        exporttBTN = Button(bottomWrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: exportData(data))
        exporttBTN.pack()

def openApplication():
    root = Tk()                                     #initializes the window and names it "root"

    global topWrapper                               #Makes the topWrapper a global variable so that it can be accessed in any Function
    global middleWrapper                            #Makes the middleWrapper a global variable so that it can be accessed in any Function
    global bottomWrapper                            #Makes the bottomWrapper a global variable so that it can be accessed in any Function
    global fileNameLabel                            #Makes the fileNameLabel a global variable so that it can be accessed in any Function
    global tv1                                      #Makes the treeview a global variable so that it can be accessed in any Function
    global topLabel

    fileTypeChoice = StringVar()
    fileTypeChoice.set("--Select a File Type--")

    FILETYPEOPTIONS = [".CSV", ".DAT"]

    titleText = Label(root, text="Welcome to the Automated Data Scrambling Engine!") #Creates text that appears at top of application
    topWrapper = LabelFrame(root, text="Preview")                                    #Creates preview Section
    middleWrapper = LabelFrame(root, text="Configuration")                           #Creates configure Section
    bottomWrapper = LabelFrame(root, text="Current File")                            #Creates select File section
    fileNameLabel = Label(bottomWrapper, text="No file selected")                    #Creates text for selected file name
    topLabel = Label(topWrapper, text="View preview of data here:")                  #Creates text for top label
    tv1 = ttk.Treeview(topWrapper)                                                   #Creates treeview for previewing data
    fileTypeLabel = Label(bottomWrapper, text = "Please select the type of file you would like to upload")
    fileTypeDropdown = OptionMenu(bottomWrapper, fileTypeChoice, *FILETYPEOPTIONS)
    confirmFileTypeBTN = Button(bottomWrapper, text="Confirm File Type",      #Creates confirm file button
    padx=10, pady=5, fg="white", bg="dark blue", command=lambda: fileType(fileTypeChoice))
    treescrolly = Scrollbar(tv1, orient="vertical", command=tv1.yview)            #Updates the y-axis view of the widget
    treescrollx = Scrollbar(tv1, orient="horizontal", command=tv1.xview)          #Updates the x-axis view of the widget
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)    #Assigns the scrollbars to the Treeview
   
   

    titleText.pack(fill="both", expand="yes", padx=20, pady=20)      #Places title text widget in window
    topWrapper.pack(fill="both", expand="yes", padx=20, pady=20)     #Places topWrapper label frame in window
    middleWrapper.pack(fill="both", expand="yes", padx=20, pady=20)  #Places middleWrapper label frame in window
    bottomWrapper.pack(fill="both", expand="yes", padx=20, pady=20)  #Places bottomWrapper label frame in window
    fileNameLabel.pack()                                             #Places fileName Label in bottomWrapper frame
    topLabel.pack()                                                  #Places top label in top wrapper frame          
    tv1.pack(fill="both", expand="yes", padx=20, pady=20)            #Places treeview in topWrapper frame
    treescrollx.pack(side="bottom", fill="x")                        #Makes the scrollbar fill the x axis of the Treeview widget
    treescrolly.pack(side="right", fill="y")                         #Makes the scrollbar fill the y axis of the Treeview widget
    fileTypeLabel.pack()
    fileTypeDropdown.pack()
    confirmFileTypeBTN.pack(expand = "true")                                #Places the Open File Button in bottomWrapper frame


    root.title("Automated Data Scrambling Engine")  #Sets window title to the name of our project
    root.geometry("800x700")                        #Sets window size to 800x700 pixels
    root.mainloop()                                 #Keeps window open and running


def main():                                         #Everything within this "main()" Function is the actual application
    openApplication()
   

if __name__ == "__main__": #Checks to make sure the file is being run as a script and not imported into another file. (Basic Python Boilerplate)
    main()