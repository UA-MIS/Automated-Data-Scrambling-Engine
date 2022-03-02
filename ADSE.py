from fileinput import filename
from pickle import EMPTY_LIST
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
import pandas as pd
import numpy as np
import faker as faker

fake = faker.Faker()

class EmailAddress:
    def __init__(self, data, columns, object_choice, prior_error):
        self.data = data
        self.columns = columns
        self.object_choice = object_choice
        self.prior_error = prior_error
    def new_attribute(self, attr):
        setattr(self, attr, attr)

class StreetAddress:
    def __init__(self, data, columns, object_choice, prior_error):
        self.data = data
        self.columns = columns
        self.object_choice = object_choice
        self.prior_error = prior_error
    def new_attribute(self, attr):
        setattr(self, attr, attr)

class PhoneNumber:
    def __init__(self, data, columns, object_choice, prior_error):
        self.data = data
        self.columns = columns
        self.object_choice = object_choice
        self.prior_error = prior_error
    def new_attribute(self, attr):
        setattr(self, attr, attr)

class NationalIdentifier:
    def __init__(self, data, columns, object_choice, prior_error):
        self.data = data
        self.columns = columns
        self.object_choice = object_choice
        self.prior_error = prior_error
    def new_attribute(self, attr):
        setattr(self, attr, attr)


def add_file(delim_choice): #Function that allows user to upload other files with different delimiters
    if delim_choice.get() == "":
        clear_bottom_frame_2()
        filename_label = Label(bottom_wrapper, text="No file selected")
        filename_label.pack()
        delim_choice = StringVar()
        no_delimiter_label = Label(bottom_wrapper, text = "No delimiter chosen.", fg = "red")
        no_delimiter_label.pack()
        delim_entry_label = Label(bottom_wrapper, text = "Please enter the delimiter your file uses:")
        delim_entry = Entry(bottom_wrapper, textvariable = delim_choice)
        delim_confirm_btn = Button(bottom_wrapper, text="Confirm Delimiter", command = lambda: add_file(delim_choice))
        delim_entry_label.pack()
        delim_entry.pack()
        delim_confirm_btn.pack(padx = 20, pady = 5)
    else:
        if delim_choice.get() == ',':
            file_name = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("CSV", "*.csv"), ("all files", "*.*")))
        else:
            file_name = filedialog.askopenfilename(initialdir="/", title="Select File")
        data = pd.read_csv(file_name, header=0, sep=delim_choice.get())
        file_name_label["text"] = file_name
        read_columns(data)

def clear_middle_frame(): #Function that clears the middle wrapper
    for widget in middle_wrapper.winfo_children():
        widget.destroy()

def clear_bottom_frame_2(): #Function that clears the middle wrapper
    for widget in bottom_wrapper.winfo_children():
        widget.destroy()

def clear_bottom_frame(): #Function that clears the bottom wrapper
    for widget in bottom_wrapper.winfo_children():
        if widget.widgetName != "label" or widget["text"] == "Please enter the delimiter your file uses:" or widget["text"] == "No delimiter chosen.":
            widget.destroy()

def read_columns(data): #Function to read columns from csv and create a list of those columns
    columns = list
    columns = data.columns.values
    clear_middle_frame()
    clear_bottom_frame()
    display_original_data(columns, data)

def display_original_data(columns, data): #Function that displays csv data in the preview
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
    display_original_dropdown(columns, data)

def display_data(object): #Function that displays csv data in the preview
    clear_data()
    object.columns = object.data.columns.values
    data_without_NaN = object.data.replace(np.nan, '', regex=True)
    tv1["columns"] = object.columns
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)
    df_rows = data_without_NaN.to_numpy().tolist()
    count = 0
    for row in df_rows:
        if count < 20:
            tv1.insert("", "end", values=row)
            count += 1
    display_dropdown(object)

def clear_data(): #Function that clears the preview so that it can be repopulated
    tv1.delete(*tv1.get_children())

def display_dropdown(object): #Function that displays the dropdown to choose the business object
    BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier"]
    objectChoice = StringVar()
    objectChoice.set("--Business Object--")
    dropdownLabel = Label(middle_wrapper, text="Select the Business Object that corresponds with your file:")
    objectDropdown = OptionMenu(middle_wrapper, objectChoice, *BUSINESSOBJECTS)
    dropdownLabel.pack()
    objectDropdown.pack()
    confirmObjectBTN = Button(middle_wrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: route_configuration(object))
    confirmObjectBTN.pack(expand = "true")

def display_original_dropdown(columns, data): #Function that displays the dropdown to choose the business object
    BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier"]
    objectChoice = StringVar()
    objectChoice.set("--Business Object--")
    dropdownLabel = Label(middle_wrapper, text="Select the Business Object that corresponds with your file:")
    objectDropdown = OptionMenu(middle_wrapper, objectChoice, *BUSINESSOBJECTS)
    dropdownLabel.pack()
    objectDropdown.pack()
    prior_error = False
    confirmObjectBTN = Button(middle_wrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: create_object(columns, data, objectChoice, prior_error))
    confirmObjectBTN.pack(expand = "true")

def create_object(columns, data, objectChoice, prior_error):
    if objectChoice.get() == "Email Address":
        object = EmailAddress(data, columns, objectChoice.get(), prior_error)
        create_columns(object)
    elif objectChoice.get() == "Street Address":
        object = StreetAddress(data, columns, objectChoice.get(), prior_error)
        create_columns(object)
    elif objectChoice.get() == "Phone Number":
        object = PhoneNumber(data, columns, objectChoice.get(), prior_error)
        create_columns(object)
    elif objectChoice.get() == "National Identifier":
        object = NationalIdentifier(data, columns, objectChoice.get(), prior_error)
        create_columns(object)

def create_columns(object):
    if object.object_choice == "Street Address":
        object.data["AddressLine1"] = ""
        object.data["AddressLine2"] = ""
        object.data["METADATA"] = "MERGE"
        object.data["PersonAddress"] = "PersonAddress"
        print(object.data)
        route_configuration(object)
    elif object.object_choice == "Phone Number":
        object.data["PhoneNumber"] = ""
        object.data["METADATA"] = "MERGE"
        object.data["PersonPhone"] = "PersonPhone"
        route_configuration(object)
    elif object.object_choice == "National Identifier":
        object.data["NationalIdentifierNumber"] = ""
        object.data["METADATA"] = "MERGE"
        object.data["NationalIdentifier"] = "NationalIdentifier"
        route_configuration(object)
    elif object.object_choice == "Email Address":
        object.data["METADATA"] = "MERGE"
        object.data["PersonEmail"] = "PersonEmail"
        print(object.data)
        route_configuration(object)

def route_configuration(object):
    if object.object_choice == "Street Address":
        setattr(object, "is_street_empty", False)
        select_street_address(object)
    elif object.object_choice == "Phone Number":
        set_target_column(object)
    elif object.object_choice == "National Identifier":
        set_target_column(object)
    elif object.object_choice == "Email Address":
        setattr(object, "domain", "")
        setattr(object, "is_domain_empty", False)
        select_domain(object)

def set_target_column(object):
    if object.object_choice == "Street Address":
        clear_middle_frame()
        setattr(object, "target_column_1", "AddressLine1")
        setattr(object, "target_column_2", "AddressLine2")
        generate_data_street(object)
    elif object.object_choice == "Phone Number":
        clear_middle_frame()
        setattr(object, "target_column", "PhoneNumber")
        generate_data(object)
    elif object.object_choice == "National Identifier":
        clear_middle_frame()
        setattr(object, "target_column", "NationalIdentifier")
        generate_data(object)
    elif object.object_choice == "Email Address":
        clear_middle_frame()
        setattr(object, "target_column", "EmailAddress")
        generate_data_email(object)
        

def select_domain(object): #Function that prompts user to enter a domain for generated email addresses
    if object.is_domain_empty == False:
        clear_middle_frame()
        domain_choice = StringVar()
        domain_entry_label = Label(middle_wrapper, text = "Please enter the domain you want to use for generated data:")
        domain_entry = Entry(middle_wrapper, textvariable = domain_choice)
        confirm_domain_btn = Button(middle_wrapper, text="Confirm Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_domain(object, domain_choice))
        domain_entry_label.pack()
        domain_entry.pack()
        confirm_domain_btn.pack()
    else:
        clear_middle_frame()
        empty_domain_label = Label(middle_wrapper, text = "The domain is empty. Please enter a domain.", fg = "red")
        empty_domain_label.pack()
        domain_choice = StringVar()
        domain_entry_label = Label(middle_wrapper, text = "Please enter the domain you want to use for generated data:")
        domain_entry = Entry(middle_wrapper, textvariable = domain_choice)
        confirm_domain_btn = Button(middle_wrapper, text="Confirm Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_domain(object, domain_choice))
        domain_entry_label.pack()
        domain_entry.pack()
        confirm_domain_btn.pack()
    
def set_domain(object, domain_choice):
    if domain_choice.get() == "":
        object.is_domain_empty = True
        select_domain(object)
    else:
        setattr(object, "domain", domain_choice.get())
        set_target_column(object)


def select_street_address(object): #Function that prompts user to enter a street name for generated street addresses
    if object.is_street_empty == False:
        clear_middle_frame()
        street_choice = StringVar()
        entry_label_street = Label(middle_wrapper, text="Please enter the street address you want to use for generated data:")
        street_entry = Entry(middle_wrapper, textvariable=street_choice)
        confirm_street_btn = tk.Button(middle_wrapper, text="Confirm Street Name", padx=10, pady=5, fg="white", bg="dark blue",
                                    command=lambda: set_street_address(object, street_choice))
        entry_label_street.pack()
        street_entry.pack()
        confirm_street_btn.pack()
    else:
        clear_middle_frame()
        empty_street_label = Label(middle_wrapper, text = "The street name is empty. Please enter a street name.", fg = "red")
        empty_street_label.pack()
        street_choice = StringVar()
        entry_label_street = Label(middle_wrapper, text="Please enter the street address you want to use for generated data:")
        street_entry = Entry(middle_wrapper, textvariable=street_choice)
        confirm_street_btn = tk.Button(middle_wrapper, text="Confirm Street Name", padx=10, pady=5, fg="white", bg="dark blue",
                                    command=lambda: set_street_address(object, street_choice))
        entry_label_street.pack()
        street_entry.pack()
        confirm_street_btn.pack()

def set_street_address(object, street_choice):
    if street_choice.get() == "":
        object.is_street_empty = True
        select_street_address(object)
    else:
        setattr(object, "street", street_choice.get())
        setattr(object, "frequency_error", False)
        select_frequency(object)

def select_frequency(object):  # Function that displays the dropdown to choose the street line 2 frequency
    if object.frequency_error == False:
        clear_middle_frame()
        STREETOBJECTS = ["10", "20", "50", "100"]
        frequency_choice = tk.StringVar()
        frequency_choice.set("--Street Address Line 2 Frequency--")
        frequency_label = tk.Label(middle_wrapper, text="Select the frequency of which you want :")
        frequency_dropdown = tk.OptionMenu(middle_wrapper, frequency_choice, *STREETOBJECTS)
        frequency_label.pack()
        frequency_dropdown.pack()
        confirm_street_btn = tk.Button(middle_wrapper, text="Confirm Street Line 2 Frequency Choice", padx=10, pady=5, fg="white",
                                    bg="dark blue", command=lambda: set_frequency(object, frequency_choice))
        confirm_street_btn.pack(expand="true")
    else:
        clear_middle_frame()
        STREETOBJECTS = ["10", "20", "50", "100"]
        frequency_choice = tk.StringVar()
        frequency_error_label = Label(middle_wrapper, text = "No frequency selected. Please select a frequency.", fg = "red")
        frequency_error_label.pack()
        frequency_choice.set("--Street Address Line 2 Frequency--")
        frequency_label = tk.Label(middle_wrapper, text="Select the frequency of which you want :")
        frequency_dropdown = tk.OptionMenu(middle_wrapper, frequency_choice, *STREETOBJECTS)
        frequency_label.pack()
        frequency_dropdown.pack()
        confirm_street_btn = tk.Button(middle_wrapper, text="Confirm Street Line 2 Frequency Choice", padx=10, pady=5, fg="white",
                                    bg="dark blue", command=lambda: set_frequency(object, frequency_choice))
        confirm_street_btn.pack(expand="true")

def set_frequency(object, frequency_choice):
    if frequency_choice.get() == "--Street Address Line 2 Frequency--":
        object.frequency_error = True
        select_frequency(object)
    else:
        setattr(object, "frequency", frequency_choice.get())
        set_target_column(object)
            
def generate_data(object): #Function that reads business object choice and directs data to corresponding generate function
    top_label["text"] = "Data has been updated. You can export by clicking the 'Export Data' button below"
    global export_btn
    global reorder_btn
    export_btn = Button(bottom_wrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: exportData(object))
    reorder_btn = Button(bottom_wrapper, text = "Reorder Columns", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: reorderColumns(object))
    export_btn.pack()
    reorder_btn.pack()
    if object.object_choice == "Phone Number":
        generate_phone_number(object)
        display_data(object)
    else:
        generate_national_identifier(object)
        display_data(object)

def generate_data_email(object): #Function that directs data to email generate function
    top_label["text"] = "Data has been updated. You can export by clicking the 'Export Data' button below"
    global export_btn
    global reorder_btn
    export_btn = Button(bottom_wrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: exportData(object))
    reorder_btn = Button(bottom_wrapper, text = "Reorder Columns", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: reorderColumns(object))
    export_btn.pack()
    reorder_btn.pack()
   
    generate_email_address(object)
    display_data(object)

def generate_email_address(object):            #Function that generates email addresses
    object.data[object.target_column] = object.data[object.target_column].apply(lambda x: x.split("@")[0] + "@" + object.domain)

def generate_data_street(object):  # Function that directs data to street address generate function
    top_label["text"] = "Data has been updated. You can export by clicking the 'Export Data' button below"
    global export_btn
    global reorder_btn
    export_btn = tk.Button(bottom_wrapper, text="Export Data", padx=10, pady=5, fg="white", bg="dark blue",
                          command=lambda: exportData(object))
    reorder_btn = tk.Button(bottom_wrapper, text="Reorder Columns", padx=10, pady=5, fg="white", bg="dark blue",
                            command=lambda: reorderColumns(object))
    export_btn.pack()
    reorder_btn.pack()

    generate_street_address(object)
    display_data(object)
   

def generate_street_address(object):  # Function that generates street addresses

    for i in object.data.index:
        object.data.at[i, object.target_column_1] = return_streetaddress(object.street, i)
        if object.frequency == "10":
            frequency = 10
            print(i % frequency)
            if i % frequency == 0:
                object.data.at[i, object.target_column_2] = return_streetaddress_line2(i)
        elif object.frequency == "20":
            frequency = 20
            if i % frequency == 0:
                object.data.at[i, object.target_column_2] = return_streetaddress_line2(i)
        elif object.frequency == "50":
            frequency = 50
            if i % frequency == 0:
                object.data.at[i, object.target_column_2] = return_streetaddress_line2(i)
        else:
            frequency = 100
            if i % frequency == 0:
                object.data.at[i, object.target_column_2] = return_streetaddress_line2(i)
       

def return_streetaddress(street_choice, i):
    x = str(i + 110)
    return x + " " + street_choice         #for each piece of data, create an address with their street name and incremented

def return_streetaddress_line2(i):  # this method will generate the line 2 data in the column if divisible by the frequency choice
    x = str(i + 11)
    return "Unit " + x

def generate_phone_number(object):             #Function that generates phone numbers
    for i in object.data.index[0:-1]:
        if i % 1 == 0:
            object.data.at[i, object.target_column] = generatePhone() #normal format
    for i in object.data.index[0:-1]:
        if i % 3 == 1:
            object.data.at[i, object.target_column] = generate_phone_format() #different format
    for i in object.data.index[0:-1]:
        if i % 5 == 1:
            object.data.at[i, object.target_column] = generate_phone_format_three() #different format
   

def generate_national_identifier(object):      #Function that generates national identifiers
    for i in object.data.index:
        object.data.at[i, object.target_column] = generate_SSN()

def generate_SSN(): #Actual Function that generates SSN's
    return fake.ssn()

def generatePhone(): #Actual Function that generates phone numbers
    return fake.numerify("(###)-###-####")

def generate_phone_format(): #Actual Function that generates phone numbers
    return fake.numerify("###-###-####")

def generate_phone_format_three(): #Actual Function that generates phone numbers
    return fake.numerify("### ### ####")

def exportData(object): #Function that exports data as pipe delimited .dat file
    savePath = filedialog.asksaveasfile(mode='w', defaultextension=".dat")
    object.data.to_csv(savePath, sep = "|", index = False, line_terminator='\n')
    print(savePath)
    if bool(savePath) == True:
        top_label["text"] = "File succesfully exported."
    else:
        top_label["text"] = "File failed to export."


def reorderColumns(object): # Function that reorders columns based on what they need the order to be **STILL NEED ORDER
    if object.object_choice == "Street Address":
        correct_order = ["METADATA", "PersonAddress", "SourceSystemID", "SourceSystemOwner", "EffectiveStartDate", "EffectiveEndDate", "AddressType", "PrimaryFlag", "AddressLine1", "AddressLine2", "AddressLine3", "AddressLine4",  "Country", "PostalCode", "Region1", "Region2", "Region3", "TownOrCity"]
        object.data = object.data[correct_order]
        top_label["text"] = "Columns have been reordered. You can export by clicking the 'Export Data' button below"
        read_columns(object.data)
        export_btn.destroy()
        reorder_btn.destroy()
        export_data_btn = Button(bottom_wrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: exportData(object))
        export_data_btn.pack()
    elif object.object_choice == "Email Address":
        correct_order = ["METADATA", "PersonEmail", "SourceSystemID", "SourceSystemOwner", "DateFrom", "DateTo", "EmailType", "PrimaryFlag", "EmailAddress"]
        object.data = object.data[correct_order]
        top_label["text"] = "Columns have been reordered. You can export by clicking the 'Export Data' button below"
        read_columns(object.data)
        export_btn.destroy()
        reorder_btn.destroy()
        export_data_btn = Button(bottom_wrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: exportData(object))
        export_data_btn.pack()
    elif object.object_choice == "Phone Number":
        correct_order = ["METADATA", "PersonPhone", "SourceSystemID", "SourceSystemOwner", "DateFrom", "DateTo", "PhoneType", "PrimaryFlag", "PhoneNumber"]
        object.data = object.data[correct_order]
        top_label["text"] = "Columns have been reordered. You can export by clicking the 'Export Data' button below"
        read_columns(object.data)
        export_btn.destroy()
        reorder_btn.destroy()
        export_data_btn = Button(bottom_wrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: exportData(object))
        export_data_btn.pack()
    elif object.object_choice == "National Identifier":
        correct_order = ["METADATA", "NationalIdentifier", "SourceSystemID", "SourceSystemOwner", "EffectiveStartDate", "EffectiveEndDate", "NationalIdentifierType", "LegislationCode", "PrimaryFlag", "NationalIdentifierNumber"]
        object.data = object.data[correct_order]
        top_label["text"] = "Columns have been reordered. You can export by clicking the 'Export Data' button below"
        read_columns(object.data)
        export_btn.destroy()
        reorder_btn.destroy()
        export_data_btn = Button(bottom_wrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: exportData(object))
        export_data_btn.pack()

def open_application(): #Function that opens the application
    root = Tk()                                     #initializes the window and names it "root"
    title_font = ("Calibri", 20, "bold")
    small_font = ("Calibri", 10, "bold")

    global top_wrapper                               #Makes the top_wrapper a global variable so that it can be accessed in any Function
    global middle_wrapper                            #Makes the middle_wrapper a global variable so that it can be accessed in any Function
    global bottom_wrapper                            #Makes the bottom_wrapper a global variable so that it can be accessed in any Function
    global file_name_label                            #Makes the file_name_label a global variable so that it can be accessed in any Function
    global tv1                                      #Makes the treeview a global variable so that it can be accessed in any Function
    global top_label
    global delim_entry_label
    global delim_entry
    global delim_confirm_btn

    title_text = Label(root, text="Welcome to the Automated Data Scrambling Engine!", font=title_font) #Creates text that appears at top of application
    top_wrapper = LabelFrame(root, text="Preview")                                    #Creates preview Section
    middle_wrapper = LabelFrame(root, text="Configuration")                           #Creates configure Section
    bottom_wrapper = LabelFrame(root, text="Current File")                            #Creates select File section
    file_name_label = Label(bottom_wrapper, text="No file selected", name = "file_name_label")                    #Creates text for selected file name
    top_label = Label(top_wrapper, text="View preview of data here:", font=small_font)                  #Creates text for top label
    tv1 = ttk.Treeview(top_wrapper)                                                   #Creates treeview for previewing data
    delim_choice = StringVar()
    delim_entry_label = Label(bottom_wrapper, text = "Please enter the delimiter your file uses:")
    delim_entry = Entry(bottom_wrapper, textvariable = delim_choice)
    delim_confirm_btn = Button(bottom_wrapper, text="Confirm Delimiter", command = lambda: add_file(delim_choice))
    treescrolly = Scrollbar(tv1, orient="vertical", command=tv1.yview)            #Updates the y-axis view of the widget
    treescrollx = Scrollbar(tv1, orient="horizontal", command=tv1.xview)          #Updates the x-axis view of the widget
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)    #Assigns the scrollbars to the Treeview
   
   

    title_text.pack(padx=5, pady=5)      #Places title text widget in window
    top_wrapper.pack(fill="both", expand="yes", padx=20, pady=20)     #Places top_wrapper label frame in window
    middle_wrapper.pack(fill="both", expand="yes", padx=20, pady=20)  #Places middle_wrapper label frame in window
    bottom_wrapper.pack(fill="x", padx=20, pady=20)  #Places bottom_wrapper label frame in window
    file_name_label.pack()                                             #Places fileName Label in bottom_wrapper frame
    top_label.pack()                                                  #Places top label in top wrapper frame          
    tv1.pack(fill="both", expand="yes", padx=20, pady=20)            #Places treeview in top_wrapper frame
    treescrollx.pack(side="bottom", fill="x")                        #Makes the scrollbar fill the x axis of the Treeview widget
    treescrolly.pack(side="right", fill="y")                         #Makes the scrollbar fill the y axis of the Treeview widget
    delim_entry_label.pack()
    delim_entry.pack()
    delim_confirm_btn.pack(padx = 20, pady = 5)
    print(file_name_label.winfo_name)


    root.title("Automated Data Scrambling Engine")  #Sets window title to the name of our project
    root.geometry("800x700")                        #Sets window size to 800x700 pixels
    root.mainloop()                                 #Keeps window open and running


def main():                                         #Everything within this "main()" Function is the actual application
    open_application()
   

if __name__ == "__main__": #Checks to make sure the file is being run as a script and not imported into another file. (Basic Python Boilerplate)
    main()