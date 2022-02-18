from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import numpy as np
import faker as faker

fake = faker.Faker()


def addFile():  # Function to open the filedialog and prompt the user to choose a file to upload into the application
    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("CSVs", "*.csv"), ("all files", "*.*")))
    data = pd.read_csv(filename, header=0)
    print(filename)
    fileNameLabel["text"] = filename
    readColumns(data)


def clearFrame():
    for widget in middleWrapper.winfo_children():
        widget.destroy()


def readColumns(data):  # Function to read columns from csv and create a list of those columns
    columns = list
    columns = data.columns.values
    clearFrame()
    displayData(columns, data)


def displayData(columns, data):  # Function that displays csv data in the preview
    clear_data()
    tv1["columns"] = columns
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)
    df_rows = data.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values=row)
    displayDropdown(columns, data)


def updateData(data):  # Function that updates data in the preview
    clear_data()
    df_rows = data.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values=row)


def clear_data():  # Function that clears the preview so that it can be repopulated
    tv1.delete(*tv1.get_children())


def displayDropdown(columns, data):  # Function that displays the dropdown to choose the business object
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
    confirmObjectBTN = tk.Button(middleWrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white",
                                 bg="dark blue", command=lambda: searchColumns(columns, data, objectChoice))
    confirmObjectBTN.pack(expand="true")


def searchColumns(columns, data,
                  objectChoice):  # Function that searches through the data's columns to find the ones that match the business object they want to scramble
    print(columns)
    if objectChoice.get() == "Street Address":
        possibleColumns = [col for col in columns if 'Street' in col]
        print(possibleColumns)
        if bool(possibleColumns) == True:
            selectStreetAddress(possibleColumns, data, objectChoice, columns)
            displayStreetLineDropdown(columns, data)
        else:
            columnNotFoundLabel = tk.Label(middleWrapper,
                                           text="There were not any columns matching that business object. Please select a different object.")
            columnNotFoundLabel.pack()
    elif objectChoice.get() == "Email Address":
        possibleColumns = [col for col in columns if 'Email' in col]
        if bool(possibleColumns) == True:
            selectDomain(possibleColumns, data, objectChoice, columns)
        else:
            columnNotFoundLabel = tk.Label(middleWrapper,
                                           text="There were not any columns matching that business object. Please select a different object.")
            columnNotFoundLabel.pack()
    elif objectChoice.get() == "Phone Number":
        possibleColumns = [col for col in columns if 'Phone' in col]
        if bool(possibleColumns) == True:
            selectColumns(possibleColumns, data, objectChoice, columns)
        else:
            columnNotFoundLabel = tk.Label(middleWrapper,
                                           text="There were not any columns matching that business object. Please select a different object.")
            columnNotFoundLabel.pack()
    elif objectChoice.get() == "National Identifier":
        possibleColumns = [col for col in columns if 'SSN' in col]
        if bool(possibleColumns) == True:
            selectColumns(possibleColumns, data, objectChoice, columns)
        else:
            columnNotFoundLabel = tk.Label(middleWrapper,
                                           text="There were not any columns matching that business object. Please select a different object.")
            columnNotFoundLabel.pack()
    else:
        global message
        message = Label(middleWrapper, text="You must select a Business Object Type", fg="red")
        message.pack()


def selectDomain(possibleColumns, data, objectChoice, columns):
    clearFrame()
    domainChoice = StringVar()
    entryLabel = Label(middleWrapper, text="Please enter the domain you want to use for generated data:")
    domainEntry = Entry(middleWrapper, textvariable=domainChoice)
    confirmDomainBTN = tk.Button(middleWrapper, text="Confirm Domain Name", padx=10, pady=5, fg="white", bg="dark blue",
                                 command=lambda: selectColumnsEmail(possibleColumns, data, objectChoice, columns,
                                                                    domainChoice))
    entryLabel.pack()
    domainEntry.pack()
    confirmDomainBTN.pack()


def selectColumns(possibleColumns, data, objectChoice,
                  columns):  # Function that creates radio buttons and allows user to select the column they want to affect
    columnV = {}
    columnWidgetYes = {}
    columnWidgetNo = {}
    columnNames = {}
    clearFrame()

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
                                 command=lambda: createConfigLog(data, objectChoice, columnV, columnWidgetYes,
                                                                 columnWidgetNo, columnNames, possibleColumns, columns))
    confirmColumnBTN.pack(expand="true")


def selectColumnsEmail(possibleColumns, data, objectChoice, columns,
                       domainChoice):  # Function that creates radio buttons and allows user to select the column they want to affect
    columnV = {}
    columnWidgetYes = {}
    columnWidgetNo = {}
    columnNames = {}
    clearFrame()

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
                                 command=lambda: createConfigLogEmail(data, objectChoice, columnV, columnWidgetYes,
                                                                      columnWidgetNo, columnNames, possibleColumns,
                                                                      columns, domainChoice))
    confirmColumnBTN.pack(expand="true")


def createConfigLog(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns,
                    columns):  # Function that creates config log and selects target column
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


def createConfigLogEmail(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns,
                         columns, domainChoice):  # Function that creates config log and selects target column
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
    # generateDataEmail(data, objectChoice, targetColumn, columns, domainChoice)


def generateData(data, objectChoice, targetColumn,
                 columns):  # Function that reads business object choice and directs data to corresponding generate function
    topLabel["text"] = "Data has been updated. You can export by clicking the 'Export Data' button below"
    global exportBTN
    global reorderBTN
    exportBTN = tk.Button(bottomWrapper, text="Export Data", padx=10, pady=5, fg="white", bg="dark blue",
                          command=lambda: exportData(data))
    reorderBTN = tk.Button(bottomWrapper, text="Reorder Columns", padx=10, pady=5, fg="white", bg="dark blue",
                           command=lambda: reorderColumns(data, targetColumn))
    exportBTN.pack()
    reorderBTN.pack()
    if objectChoice.get() == "Street Address":
        generateStreetAddress(data, targetColumn)
        displayData(columns, data)
    elif objectChoice.get() == "Email Address":
        # generateEmailAddress(data, targetColumn)
        displayData(columns, data)
    elif objectChoice.get() == "Phone Number":
        generatePhoneNumber(data, targetColumn)
        displayData(columns, data)
    else:
        generateNationalIdentifier(data, targetColumn)
        displayData(columns, data)


# def generateDataEmail(data, objectChoice, targetColumn, columns,
#                       domainChoice):  # Function that reads business object choice and directs data to corresponding generate function
#     topLabel["text"] = "Data has been updated. You can export by clicking the 'Export Data' button below"
#     global exportBTN
#     global reorderBTN
#     exportBTN = tk.Button(bottomWrapper, text="Export Data", padx=10, pady=5, fg="white", bg="dark blue",
#                           command=lambda: exportData(data))
#     reorderBTN = tk.Button(bottomWrapper, text="Reorder Columns", padx=10, pady=5, fg="white", bg="dark blue",
#                            command=lambda: reorderColumns(data, targetColumn))
#     exportBTN.pack()
#     reorderBTN.pack()
#
#     generateEmailAddress(data, targetColumn, domainChoice)
#     displayData(columns, data)


def selectStreetAddress(possibleColumns, data, objectChoice, columns):
    clearFrame()
    streetChoice = StringVar()
    entryLabelStreet = Label(middleWrapper, text="Please enter the street address you want to use for generated data:")
    streetEntry = Entry(middleWrapper, textvariable=streetChoice)
    confirmStreetBTN = tk.Button(middleWrapper, text="Confirm Street Name", padx=10, pady=5, fg="white", bg="dark blue",
                                 command=lambda: selectColumnsStreet(possibleColumns, data, objectChoice, columns,
                                                                     streetChoice))
    entryLabelStreet.pack()
    streetEntry.pack()
    confirmStreetBTN.pack()



def selectColumnsStreet(possibleColumns, data, objectChoice, columns,
                       streetChoice):  # Function that creates radio buttons and allows user to select the column they want to affect
    columnV = {}
    columnWidgetYes = {}
    columnWidgetNo = {}
    columnNames = {}
    clearFrame()

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
                                 command=lambda: createConfigLogEmail(data, objectChoice, columnV, columnWidgetYes,
                                                                      columnWidgetNo, columnNames, possibleColumns,
                                                                      columns, streetChoice))
    confirmColumnBTN.pack(expand="true")


def displayStreetLineDropdown(columns, data):  # Function that displays the dropdown to choose the business object
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
                                 bg="dark blue", command=lambda: searchColumns(columns, data, frequencyChoice))
    confirmStreetBTN.pack(expand="true")

def generateStreetAddress(data, objectChoice, targetColumn, columns,
                          streetChoice):  # Function that generates street addresses
    for i in data.index:
        data.at[i, targetColumn] = generate_streetaddress()

def generate_streetaddress(data, objectChoice, targetColumn, columns,
                          streetChoice, frequencyChoice):
    displayData(columns, data)
    for i in data.index:
        data.at[i, targetColumn] = (i + " " + streetChoice)           #for each piece of data, create an address with their street name and incremented number
        if i % frequencyChoice == 0:
            StreetAddressLine2 = ("Unit "+i)                          #if the number is a multiple of their chosen number, create a street address line 2
            data['StreetAddressLine2'] = StreetAddressLine2
    return StreetAddressLine2

# def generateEmailAddress(data, targetColumn, domainChoice):  # Function that generates email addresses
#     # Generate Email Address Function
#     domain = domainChoice.get()
#     data[targetColumn] = data[targetColumn].apply(lambda x: x.split("@")[0] + "@" + domain)


def generatePhoneNumber(data, targetColumn):  # Function that generates phone numbers
    # Generate Phone Number Function
    for i in data.index:
        data.at[i, targetColumn] = generate_Phone()


def generateNationalIdentifier(data, targetColumn):  # Function that generates national identifiers
    for i in data.index:
        data.at[i, targetColumn] = generate_SSN()


def generate_SSN():  # Actual method that generates SSN's
    return fake.ssn()


def generate_Phone():  # Actual method that generates phone numbers
    return fake.numerify("(###)-###-####")


def exportData(data):
    savePath = filedialog.asksaveasfile(mode='w', defaultextension=".dat")
    data.to_csv(savePath, sep="|", index=False)
    if bool(savePath) == True:
        topLabel["text"] = "File succesfully exported."
    else:
        topLabel["text"] = "File failed to export."


def reorderColumns(data, targetColumn):
    if targetColumn == "PhoneNumber":
        correctOrder = [targetColumn, "SourceSystemOwner", "SourceSystemID", "DateFrom", "DateTo", "PrimaryFlag",
                        "PersonNumber", "PhoneType"]
        data = data[correctOrder]
        topLabel["text"] = "Columns have been reordered. You can export by clicking the 'Export Data' button below"
        readColumns(data)
        exportBTN.destroy()
        reorderBTN.destroy()
        exporttBTN = tk.Button(bottomWrapper, text="Export Data", padx=10, pady=5, fg="white", bg="dark blue",
                               command=lambda: exportData(data))
        exporttBTN.pack()
    else:
        correctOrder = [targetColumn, "SourceSystemOwner", "SourceSystemID", "DateFrom", "DateTo", "PrimaryFlag",
                        "PersonNumber"]
        data = data[correctOrder]
        topLabel["text"] = "Columns have been reordered. You can export by clicking the 'Export Data' button below"
        readColumns(data)
        exportBTN.destroy()
        reorderBTN.destroy()
        exporttBTN = tk.Button(bottomWrapper, text="Export Data", padx=10, pady=5, fg="white", bg="dark blue",
                               command=lambda: exportData(data))
        exporttBTN.pack()


def main():  # Everything within this "main()" Function is the actual application
    root = Tk()  # initializes the window and names it "root"

    global topWrapper  # Makes the topWrapper a global variable so that it can be accessed in any Function
    global middleWrapper  # Makes the middleWrapper a global variable so that it can be accessed in any Function
    global bottomWrapper  # Makes the bottomWrapper a global variable so that it can be accessed in any Function
    global fileNameLabel  # Makes the fileNameLabel a global variable so that it can be accessed in any Function
    global tv1  # Makes the treeview a global variable so that it can be accessed in any Function
    global topLabel

    titleText = Label(root,
                      text="Welcome to the Automated Data Scrambling Engine!")  # Creates text that appears at top of application
    topWrapper = LabelFrame(root, text="Preview")  # Creates preview Section
    middleWrapper = LabelFrame(root, text="Configuration")  # Creates configure Section
    bottomWrapper = LabelFrame(root, text="Current File")  # Creates select File section
    fileNameLabel = Label(bottomWrapper, text="No file selected")  # Creates text for selected file name
    topLabel = Label(topWrapper, text="View preview of data here:")  # Creates text for top label
    tv1 = ttk.Treeview(topWrapper)  # Creates treeview for previewing data
    openFileBTN = tk.Button(bottomWrapper, text="Choose a File for Scrambling",  # Creates Open File Button
                            padx=10, pady=5, fg="white", bg="dark blue", command=addFile)
    treescrolly = tk.Scrollbar(tv1, orient="vertical", command=tv1.yview)  # Updates the y-axis view of the widget
    treescrollx = tk.Scrollbar(tv1, orient="horizontal", command=tv1.xview)  # Updates the x-axis view of the widget
    tv1.configure(xscrollcommand=treescrollx.set,
                  yscrollcommand=treescrolly.set)  # Assigns the scrollbars to the Treeview

    titleText.pack(fill="both", expand="yes", padx=20, pady=20)  # Places title text widget in window
    topWrapper.pack(fill="both", expand="yes", padx=20, pady=20)  # Places topWrapper label frame in window
    middleWrapper.pack(fill="both", expand="yes", padx=20, pady=20)  # Places middleWrapper label frame in window
    bottomWrapper.pack(fill="both", expand="yes", padx=20, pady=20)  # Places bottomWrapper label frame in window
    fileNameLabel.pack()  # Places fileName Label in bottomWrapper frame
    topLabel.pack()  # Places top label in top wrapper frame
    tv1.pack(fill="both", expand="yes", padx=20, pady=20)  # Places treeview in topWrapper frame
    treescrollx.pack(side="bottom", fill="x")  # Makes the scrollbar fill the x axis of the Treeview widget
    treescrolly.pack(side="right", fill="y")  # Makes the scrollbar fill the y axis of the Treeview widget
    openFileBTN.pack(expand="true")  # Places the Open File Button in bottomWrapper frame

    root.title("Automated Data Scrambling Engine")  # Sets window title to the name of our project
    root.geometry("800x700")  # Sets window size to 800x700 pixels
    root.mainloop()  # Keeps window open and running


if __name__ == "__main__":  # Checks to make sure the file is being run as a script and not imported into another file. (Basic Python Boilerplate)
    main()