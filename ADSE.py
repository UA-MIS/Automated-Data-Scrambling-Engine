from pickle import EMPTY_LIST
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import numpy as np
import faker as faker

fake = faker.Faker()

def add_file(delim_choice): #Function that allows user to upload other files with different delimiters
    if delim_choice.get() == "":
        clearBottomFrame()
        global fileNameLabel
        fileNameLabel = Label(bottomWrapper, text="No file selected")
        fileNameLabel.pack()
        delim_choice = StringVar()
        no_delimiter_label = Label(bottomWrapper, text = "No delimiter chosen.", fg = "red")
        no_delimiter_label.pack()
        delimEntryLabel = Label(bottomWrapper, text = "Please enter the delimiter your file uses:")
        delimEntry = Entry(bottomWrapper, textvariable = delim_choice)
        delimConfirmBTN = Button(bottomWrapper, text="Confirm Delimiter", command = lambda: add_file(delim_choice))
        delimEntryLabel.pack()
        delimEntry.pack()
        delimConfirmBTN.pack()
    else:
        if delim_choice.get() == ',':
            file_name = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("CSV", "*.csv"), ("all files", "*.*")))
        else:
            file_name = filedialog.askopenfilename(initialdir="/", title="Select File")
        data = pd.read_csv(file_name, header=0, sep=delim_choice.get())
        print(file_name)
        fileNameLabel["text"] = file_name
        clearBottomFrame()
        readColumns(data)

def clearTopFrame(): #Function that clears the top wrapper
    for widget in topWrapper.winfo_children():
        widget.destroy()

def clearMiddleFrame(): #Function that clears the middle wrapper
    for widget in middleWrapper.winfo_children():
        widget.destroy()

def clearBottomFrame(): #Function that clears the bottom wrapper
    for widget in bottomWrapper.winfo_children():
        widget.destroy()

def readColumns(data): #Function to read columns from csv and create a list of those columns
    columns = list
    columns = data.columns.values
    clearMiddleFrame()
    displayData(columns, data)

def displayData(columns, data): #Function that displays csv data in the preview
    clear_data()
    data_without_NaN = data.replace(np.nan, '', regex=True)
    tv1["columns"] = columns
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)
    df_rows = data_without_NaN.to_numpy().tolist()
    count = 0
    for row in df_rows:
        if count < 20:
            tv1.insert("", "end", values=row)
            count += 1
    displayDropdown(columns, data)

def updateData(data): #Function that updates data in the preview
    clear_data()
    df_rows = data.to_numpy().tolist()
    count = 0
    for row in df_rows:
        if count < 20:
            tv1.insert("", "end", values=row)
            count += 1

def clear_data(): #Function that clears the preview so that it can be repopulated
    tv1.delete(*tv1.get_children())

def displayDropdown(columns, data): #Function that displays the dropdown to choose the business object
    BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier"]
    objectChoice = StringVar()
    objectChoice.set("--Business Object--")
    dropdownLabel = Label(middleWrapper, text="Select the Business Object that corresponds with your file:")
    objectDropdown = OptionMenu(middleWrapper, objectChoice, *BUSINESSOBJECTS)
    dropdownLabel.pack()
    objectDropdown.pack()
    prior_error = False
    confirmObjectBTN = Button(middleWrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: searchColumns(columns, data, objectChoice, prior_error))
    confirmObjectBTN.pack(expand = "true")

def searchColumns(columns, data, objectChoice, prior_error): #Function that searches through the data's columns to find the ones that match the business object they want to scramble
    if prior_error:
        if objectChoice.get() == "Street Address":
            possibleColumns = [col for col in columns if 'Street' in col]
            if bool(possibleColumns) == True:
                is_street_empty = False
                selectStreetAddress(possibleColumns, data, objectChoice, columns, is_street_empty)
        elif objectChoice.get() == "Email Address":
            possibleColumns = [col for col in columns if 'Email' in col]
            if bool(possibleColumns) == True:
                is_domain_empty = False
                selectDomain(possibleColumns, data, objectChoice, columns, is_domain_empty)
        elif objectChoice.get() == "Phone Number":
            possibleColumns = [col for col in columns if 'Phone' in col]
            if bool(possibleColumns) == True:
                is_column_selected = True
                selectColumns(possibleColumns, data, objectChoice, columns, is_column_selected)
        elif objectChoice.get() == "National Identifier":
            possibleColumns = [col for col in columns if 'SSN' in col]
            if bool(possibleColumns) == True:
                is_column_selected = True
                selectColumns(possibleColumns, data, objectChoice, columns, is_column_selected)
    else:
        if objectChoice.get() == "Street Address":
            possibleColumns = [col for col in columns if 'Street' in col]
            if bool(possibleColumns) == True:
                is_street_empty = False
                selectStreetAddress(possibleColumns, data, objectChoice, columns, is_street_empty)
            else:
                clearMiddleFrame()
                BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier"]
                object = StringVar()
                object.set("--Business Object--")
                dropdownLabel = Label(middleWrapper, text="Select the Business Object that corresponds with your file:")
                objectDropdown = OptionMenu(middleWrapper, object, *BUSINESSOBJECTS)
                dropdownLabel.pack()
                objectDropdown.pack()
                error = True
                confirmObjectBTN = Button(middleWrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: searchColumns(columns, data, object, error))
                confirmObjectBTN.pack(expand = "true")
                columnNotFoundLabel = Label(middleWrapper, text = "There were not any columns matching that business object. Please select a different object.", fg = "red")
                columnNotFoundLabel.pack()
        elif objectChoice.get() == "Email Address":
            possibleColumns = [col for col in columns if 'Email' in col]
            if bool(possibleColumns) == True:
                is_domain_empty = False
                selectDomain(possibleColumns, data, objectChoice, columns, is_domain_empty)
            else:
                clearMiddleFrame()
                BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier"]
                object = StringVar()
                object.set("--Business Object--")
                dropdownLabel = Label(middleWrapper, text="Select the Business Object that corresponds with your file:")
                objectDropdown = OptionMenu(middleWrapper, object, *BUSINESSOBJECTS)
                dropdownLabel.pack()
                objectDropdown.pack()
                error = True
                confirmObjectBTN = Button(middleWrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: searchColumns(columns, data, object, error))
                confirmObjectBTN.pack(expand = "true")
                columnNotFoundLabel = Label(middleWrapper, text = "There were not any columns matching that business object. Please select a different object.", fg = "red")
                columnNotFoundLabel.pack()
        elif objectChoice.get() == "Phone Number":
            possibleColumns = [col for col in columns if 'Phone' in col]
            if bool(possibleColumns) == True:
                is_column_selected = True
                selectColumns(possibleColumns, data, objectChoice, columns, is_column_selected)
            else:
                clearMiddleFrame()
                BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier"]
                object = StringVar()
                object.set("--Business Object--")
                dropdownLabel = Label(middleWrapper, text="Select the Business Object that corresponds with your file:")
                objectDropdown = OptionMenu(middleWrapper, object, *BUSINESSOBJECTS)
                dropdownLabel.pack()
                objectDropdown.pack()
                error = True
                confirmObjectBTN = Button(middleWrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: searchColumns(columns, data, object, error))
                confirmObjectBTN.pack(expand = "true")
                columnNotFoundLabel = Label(middleWrapper, text = "There were not any columns matching that business object. Please select a different object.", fg = "red")
                columnNotFoundLabel.pack()
        elif objectChoice.get() == "National Identifier":
            possibleColumns = [col for col in columns if 'SSN' in col]
            if bool(possibleColumns) == True:
                is_column_selected = True
                selectColumns(possibleColumns, data, objectChoice, columns, is_column_selected)
            else:
                clearMiddleFrame()
                BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier"]
                object = StringVar()
                object.set("--Business Object--")
                dropdownLabel = Label(middleWrapper, text="Select the Business Object that corresponds with your file:")
                objectDropdown = OptionMenu(middleWrapper, object, *BUSINESSOBJECTS)
                dropdownLabel.pack()
                objectDropdown.pack()
                error = True
                confirmObjectBTN = Button(middleWrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: searchColumns(columns, data, object, error))
                confirmObjectBTN.pack(expand = "true")
                columnNotFoundLabel = Label(middleWrapper, text = "There were not any columns matching that business object. Please select a different object.", fg = "red")
                columnNotFoundLabel.pack()
        else:
            clearMiddleFrame()
            BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier"]
            object = StringVar()
            object.set("--Business Object--")
            dropdownLabel = Label(middleWrapper, text="Select the Business Object that corresponds with your file:")
            objectDropdown = OptionMenu(middleWrapper, object, *BUSINESSOBJECTS)
            dropdownLabel.pack()
            objectDropdown.pack()
            prior_error = True
            confirmObjectBTN = Button(middleWrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: searchColumns(columns, data, object, prior_error))
            confirmObjectBTN.pack(expand = "true")
            columnNotFoundLabel = Label(middleWrapper, text = "There were not any columns matching that business object. Please select a different object.", fg = "red")
            columnNotFoundLabel.pack()

def selectDomain(possibleColumns, data, objectChoice, columns, is_domain_empty): #Function that prompts user to enter a domain for generated email addresses
    if is_domain_empty == False:
        clearMiddleFrame()
        domainChoice = StringVar()
        domainEntryLabel = Label(middleWrapper, text = "Please enter the domain you want to use for generated data:")
        domainEntry = Entry(middleWrapper, textvariable = domainChoice)
        is_column_selected = True
        confirmDomainBTN = Button(middleWrapper, text="Confirm Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: selectColumnsEmail(possibleColumns, data, objectChoice, columns, domainChoice, is_domain_empty, is_column_selected))
        domainEntryLabel.pack()
        domainEntry.pack()
        confirmDomainBTN.pack()
    else:
        clearMiddleFrame()
        empty_domain_label = Label(middleWrapper, text = "The domain is empty. Please enter a domain.", fg = "red")
        empty_domain_label.pack()
        domainChoice = StringVar()
        domainEntryLabel = Label(middleWrapper, text = "Please enter the domain you want to use for generated data:")
        domainEntry = Entry(middleWrapper, textvariable = domainChoice)
        is_column_selected = True
        confirmDomainBTN = Button(middleWrapper, text="Confirm Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: selectColumnsEmail(possibleColumns, data, objectChoice, columns, domainChoice, is_domain_empty, is_column_selected))
        domainEntryLabel.pack()
        domainEntry.pack()
        confirmDomainBTN.pack()
    

def selectStreetAddress(possibleColumns, data, objectChoice, columns, is_street_empty): #Function that prompts user to enter a street name for generated street addresses
    if is_street_empty == False:
        clearMiddleFrame()
        streetChoice = StringVar()
        entryLabelStreet = Label(middleWrapper, text="Please enter the street address you want to use for generated data:")
        streetEntry = Entry(middleWrapper, textvariable=streetChoice)
        frequency_error = False
        confirmStreetBTN = tk.Button(middleWrapper, text="Confirm Street Name", padx=10, pady=5, fg="white", bg="dark blue",
                                    command=lambda: displayStreetLineDropdown(possibleColumns, columns, data, objectChoice,  #NEED TO SWITCH THIS METHOD BACK AFTER DEMO
                                                                        streetChoice, is_street_empty, frequency_error))
        entryLabelStreet.pack()
        streetEntry.pack()
        confirmStreetBTN.pack()
    else:
        clearMiddleFrame()
        empty_street_label = Label(middleWrapper, text = "The street name is empty. Please enter a street name.", fg = "red")
        empty_street_label.pack()
        streetChoice = StringVar()
        entryLabelStreet = Label(middleWrapper, text="Please enter the street address you want to use for generated data:")
        streetEntry = Entry(middleWrapper, textvariable=streetChoice)
        frequency_error = False
        confirmStreetBTN = tk.Button(middleWrapper, text="Confirm Street Name", padx=10, pady=5, fg="white", bg="dark blue",
                                    command=lambda: displayStreetLineDropdown(possibleColumns, columns, data, objectChoice,  #NEED TO SWITCH THIS METHOD BACK AFTER DEMO
                                                                        streetChoice, is_street_empty, frequency_error))
        entryLabelStreet.pack()
        streetEntry.pack()
        confirmStreetBTN.pack()

def displayStreetLineDropdown(possibleColumns, columns, data, objectChoice, streetChoice, is_street_empty, frequency_error):  # Function that displays the dropdown to choose the street line 2 frequency
    if frequency_error == False:
        if streetChoice.get() == "":
            is_street_empty = True
            selectStreetAddress(possibleColumns, data, objectChoice, columns, is_street_empty)
        else:
            clearMiddleFrame()
            STREETOBJECTS = ["10", "20", "50", "100"]
            frequencyChoice = tk.StringVar()
            frequencyChoice.set("--Street Address Line 2 Frequency--")
            freqLabel = tk.Label(middleWrapper, text="Select the frequency of which you want :")
            lineTwoFreqDropdown = tk.OptionMenu(middleWrapper, frequencyChoice, *STREETOBJECTS)
            freqLabel.pack()
            lineTwoFreqDropdown.pack()
            is_column_selected = True
            confirmStreetBTN = tk.Button(middleWrapper, text="Confirm Street Line 2 Frequency Choice", padx=10, pady=5, fg="white",
                                        bg="dark blue", command=lambda: selectColumnsStreet(possibleColumns, data, objectChoice, columns,
                                                                            streetChoice, frequencyChoice, is_street_empty, frequency_error, is_column_selected))
            confirmStreetBTN.pack(expand="true")
    else:
        if streetChoice.get() == "":
            is_street_empty = True
            selectStreetAddress(possibleColumns, data, objectChoice, columns, is_street_empty)
        else:
            clearMiddleFrame()
            STREETOBJECTS = ["10", "20", "50", "100"]
            frequencyChoice = tk.StringVar()
            columnNotFoundLabel = Label(middleWrapper, text = "No frequency selected. Please select a frequency.", fg = "red")
            columnNotFoundLabel.pack()
            frequencyChoice.set("--Street Address Line 2 Frequency--")
            freqLabel = tk.Label(middleWrapper, text="Select the frequency of which you want :")
            lineTwoFreqDropdown = tk.OptionMenu(middleWrapper, frequencyChoice, *STREETOBJECTS)
            freqLabel.pack()
            lineTwoFreqDropdown.pack()
            is_column_selected = True
            confirmStreetBTN = tk.Button(middleWrapper, text="Confirm Street Line 2 Frequency Choice", padx=10, pady=5, fg="white",
                                        bg="dark blue", command=lambda: selectColumnsStreet(possibleColumns, data, objectChoice, columns,
                                                                            streetChoice, frequencyChoice, is_street_empty, frequency_error, is_column_selected))
            confirmStreetBTN.pack(expand="true")
            

def selectColumns(possibleColumns, data, objectChoice, columns, is_column_selected): #Function that creates radio buttons and allows user to select the column they want to affect
    if is_column_selected == True:
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
        confirmColumnBTN = Button(middleWrapper, text="Confirm configuration", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: createConfigLog(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns, columns, is_column_selected))
        confirmColumnBTN.pack(expand = "true")
    else:
        columnV = {}
        columnWidgetYes = {}
        columnWidgetNo = {}
        columnNames = {}
        clearMiddleFrame()
        no_column_selected_label = Label(middleWrapper, text = "No columns selected. Please select a column.", fg = "red")
        no_column_selected_label.pack()

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
        global confirmColBTN
        confirmColBTN = Button(middleWrapper, text="Confirm configuration", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: createConfigLog(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns, columns, is_column_selected))
        confirmColBTN.pack(expand = "true")

def selectColumnsEmail(possibleColumns, data, objectChoice, columns, domainChoice, is_domain_empty, is_column_selected): #Function that creates radio buttons and allows user to select the column they want to affect for EMAIL object
    if is_column_selected == True:
        if domainChoice.get() == "":
            is_domain_empty = True
            selectDomain(possibleColumns, data, objectChoice, columns, is_domain_empty)
        else:
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
            confirmColumnBTN = Button(middleWrapper, text="Confirm Configuration", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: createConfigLogEmail(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns, columns, domainChoice, is_domain_empty, is_column_selected))
            confirmColumnBTN.pack(expand = "true")
    else:
        if domainChoice.get() == "":
            is_domain_empty = True
            selectDomain(possibleColumns, data, objectChoice, columns, is_domain_empty)
        else:
            columnV = {}
            columnWidgetYes = {}
            columnWidgetNo = {}
            columnNames = {}
            clearMiddleFrame()
            no_column_selected_label = Label(middleWrapper, text = "No columns selected. Please select a column.", fg = "red")
            no_column_selected_label.pack()

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
            global confirmBTN
            confirmBTN = Button(middleWrapper, text="Confirm Configuration", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: createConfigLogEmail(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns, columns, domainChoice, is_domain_empty, is_column_selected))
            confirmBTN.pack(expand = "true")
    

def selectColumnsStreet(possibleColumns, data, objectChoice, columns, streetChoice, frequencyChoice, is_street_empty, frequency_error, is_column_selected):  # Function that creates radio buttons and allows user to select the column they want to affect for STREET ADDRESS object
    if is_column_selected == True:
        if frequencyChoice.get() == "--Street Address Line 2 Frequency--":
            frequency_error = True
            displayStreetLineDropdown(possibleColumns, columns, data, objectChoice, streetChoice, is_street_empty, frequency_error)
        else:
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
                                                                            columns, streetChoice, frequencyChoice, is_column_selected, is_street_empty, frequency_error))
            confirmColumnBTN.pack(expand="true")
    else:
        if frequencyChoice.get() == "--Street Address Line 2 Frequency--":
            frequency_error = True
            displayStreetLineDropdown(possibleColumns, columns, data, objectChoice, streetChoice, is_street_empty, frequency_error)
        else:
            columnV = {}
            columnWidgetYes = {}
            columnWidgetNo = {}
            columnNames = {}
            clearMiddleFrame()
            no_column_selected_label = Label(middleWrapper, text = "No columns selected. Please select a column.", fg = "red")
            no_column_selected_label.pack()

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
            global confirmBTN
            confirmBTN = tk.Button(middleWrapper, text="Confirm configuration", padx=10, pady=5, fg="white",
                                        bg="dark blue",
                                        command=lambda: createConfigLogStreet(data, objectChoice, columnV, columnWidgetYes,
                                                                            columnWidgetNo, columnNames, possibleColumns,
                                                                            columns, streetChoice, frequencyChoice, is_column_selected, is_street_empty, frequency_error))
            confirmBTN.pack(expand="true")


def createConfigLog(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns, columns, is_column_selected): #Function that creates config log and selects target column
    configDict = {}
    for i in possibleColumns:
        configDict[i] = columnV[i].get()
        columnWidgetYes[i].destroy()
        columnWidgetNo[i].destroy()
        columnNames[i].destroy()
        confirmColumnBTN.destroy()
    tColumn = [k for k, v in configDict.items() if v == 1]
    if tColumn == []:
        is_column_selected = False
        selectColumns(possibleColumns, data, objectChoice, columns, is_column_selected)
    else:
        targetColumn = StringVar()
        targetColumn = tColumn[0]
        clearMiddleFrame()
        generateData(data, objectChoice, targetColumn, columns)

def createConfigLogEmail(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns, columns, domainChoice, is_domain_empty, is_column_selected): #Function that creates config log and selects target column for EMAIL object
    configDict = {}
    for i in possibleColumns:
        configDict[i] = columnV[i].get()
        columnWidgetYes[i].destroy()
        columnWidgetNo[i].destroy()
        columnNames[i].destroy()
        confirmColumnBTN.destroy()
    tColumn = [k for k, v in configDict.items() if v == 1]
    if tColumn == []:
        is_column_selected = False
        selectColumnsEmail(possibleColumns, data, objectChoice, columns, domainChoice, is_domain_empty, is_column_selected)
    else:
        targetColumn = StringVar()
        targetColumn = tColumn[0]
        clearMiddleFrame()
        generateDataEmail(data, objectChoice, targetColumn, columns, domainChoice)

def createConfigLogStreet(data, objectChoice, columnV, columnWidgetYes, columnWidgetNo, columnNames, possibleColumns,
                    columns, streetChoice, frequencyChoice, is_column_selected, is_street_empty, frequency_error):  # Function that creates config log and selects target column for STREET ADDRESS object
    configDict = {}
    for i in possibleColumns:
        configDict[i] = columnV[i].get()
        columnWidgetYes[i].destroy()
        columnWidgetNo[i].destroy()
        columnNames[i].destroy()
        confirmColumnBTN.destroy()
    tColumn = [k for k, v in configDict.items() if v == 1]
    if tColumn == []:
        is_column_selected = False
        selectColumnsStreet(possibleColumns, data, objectChoice, columns, streetChoice, frequencyChoice, is_street_empty, frequency_error, is_column_selected)
    else:
        targetColumn = StringVar()
        targetColumn = tColumn[0]
        clearMiddleFrame()
        generateDataStreet(data, objectChoice, targetColumn, columns, streetChoice, frequencyChoice)


def generateData(data, objectChoice, targetColumn, columns): #Function that reads business object choice and directs data to corresponding generate function
    topLabel["text"] = "Data has been updated. You can export by clicking the 'Export Data' button below"
    global exportBTN
    global reorderBTN
    exportBTN = Button(bottomWrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: exportData(data))
    reorderBTN = Button(bottomWrapper, text = "Reorder Columns", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: reorderColumns(data, targetColumn))
    exportBTN.pack()
    reorderBTN.pack()
    if objectChoice.get() == "Phone Number":
        generatePhoneNumber(data, targetColumn)
        displayData(columns, data)
    else:
        generateNationalIdentifier(data, targetColumn)
        displayData(columns, data)

def generateDataEmail(data, objectChoice, targetColumn, columns, domainChoice): #Function that directs data to email generate function
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
                 columns, streetChoice, frequencyChoice):  # Function that directs data to street address generate function
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
    x = str(i + 110)
    return x + " " + streetChoice.get()         #for each piece of data, create an address with their street name and incremented

def generateEmailAddress(data, targetColumn, domainChoice):            #Function that generates email addresses
    domain = domainChoice.get()
    data[targetColumn] = data[targetColumn].apply(lambda x: x.split("@")[0] + "@" + domain)

def generatePhoneNumber(data, targetColumn):             #Function that generates phone numbers
    for i in data.index[0:-1]:
        if i % 1 == 0:
            data.at[i, targetColumn] = generatePhone() #normal format
    for i in data.index[0:-1]:
        if i % 3 == 1:
            data.at[i, targetColumn] = generate_phone_format() #different format
    for i in data.index[0:-1]:
        if i % 5 == 1:
            data.at[i, targetColumn] = generate_phone_format_three() #different format
   

def generateNationalIdentifier(data, targetColumn):      #Function that generates national identifiers
    for i in data.index:
        data.at[i, targetColumn] = generate_SSN()

def generate_SSN(): #Actual Function that generates SSN's
    return fake.ssn()

def generatePhone(): #Actual Function that generates phone numbers
    return fake.numerify("(###)-###-####")

def generate_phone_format(): #Actual Function that generates phone numbers
    return fake.numerify("###-###-####")

def generate_phone_format_three(): #Actual Function that generates phone numbers
    return fake.numerify("### ### ####")

def exportData(data): #Function that exports data as pipe delimited .dat file
    savePath = filedialog.asksaveasfile(mode='w', defaultextension=".dat")
    data.to_csv(savePath, sep = "|", index = False, line_terminator='\n')
    print(savePath)
    if bool(savePath) == True:
        topLabel["text"] = "File succesfully exported."
    else:
        topLabel["text"] = "File failed to export."


def reorderColumns(data, targetColumn): # Function that reorders columns based on what they need the order to be **STILL NEED ORDER
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

def openApplication(): #Function that opens the application
    root = Tk()                                     #initializes the window and names it "root"

    global topWrapper                               #Makes the topWrapper a global variable so that it can be accessed in any Function
    global middleWrapper                            #Makes the middleWrapper a global variable so that it can be accessed in any Function
    global bottomWrapper                            #Makes the bottomWrapper a global variable so that it can be accessed in any Function
    global fileNameLabel                            #Makes the fileNameLabel a global variable so that it can be accessed in any Function
    global tv1                                      #Makes the treeview a global variable so that it can be accessed in any Function
    global topLabel

    titleText = Label(root, text="Welcome to the Automated Data Scrambling Engine!") #Creates text that appears at top of application
    topWrapper = LabelFrame(root, text="Preview")                                    #Creates preview Section
    middleWrapper = LabelFrame(root, text="Configuration")                           #Creates configure Section
    bottomWrapper = LabelFrame(root, text="Current File")                            #Creates select File section
    fileNameLabel = Label(bottomWrapper, text="No file selected")                    #Creates text for selected file name
    topLabel = Label(topWrapper, text="View preview of data here:")                  #Creates text for top label
    tv1 = ttk.Treeview(topWrapper)                                                   #Creates treeview for previewing data
    delim_choice = StringVar()
    delimEntryLabel = Label(bottomWrapper, text = "Please enter the delimiter your file uses:")
    delimEntry = Entry(bottomWrapper, textvariable = delim_choice)
    delimConfirmBTN = Button(bottomWrapper, text="Confirm Delimiter", command = lambda: add_file(delim_choice))
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
    delimEntryLabel.pack()
    delimEntry.pack()
    delimConfirmBTN.pack()


    root.title("Automated Data Scrambling Engine")  #Sets window title to the name of our project
    root.geometry("800x700")                        #Sets window size to 800x700 pixels
    root.mainloop()                                 #Keeps window open and running


def main():                                         #Everything within this "main()" Function is the actual application
    openApplication()
   

if __name__ == "__main__": #Checks to make sure the file is being run as a script and not imported into another file. (Basic Python Boilerplate)
    main()