#=================================IMPORTS===================================#
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
import zipfile
import os.path

#=================================INITIALIZE FAKER===================================#
fake = faker.Faker()

#=================================BUSINESS OBJECT===================================#
class BusinessObject:
    def __init__(self, data, columns, object_choice, prior_error):
        self.data = data
        self.columns = columns
        self.object_choice = object_choice
        self.prior_error = prior_error
    def new_attribute(self, attr):
        setattr(self, attr, attr)

def create_object(columns, data, objectChoice, prior_error):
    object = BusinessObject(data, columns, objectChoice.get(), prior_error)
    create_columns(object)

def create_columns(object):
    if object.object_choice == "Street Address":
        object.data["AddressLine1"] = ""
        object.data["AddressLine2"] = ""
        object.data["METADATA"] = "MERGE"
        object.data["PersonAddress"] = "PersonAddress"
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
    elif object.object_choice == "Name": #creating the name columns
        object.data["METADATA"] = "MERGE"
        object.data["PersonName"] = "PersonName"
        object.data["FirstName"] = ""
        object.data["LastName"] = ""
        route_configuration(object)
    elif object.object_choice == "Salary": #creating the name columns
        object.data["METADATA"] = "MERGE"
        object.data["PersonSalary"] = "PersonSalary"
        object.data["Salary"] = ""
        route_configuration(object)

def route_configuration(object):
    if object.object_choice == "Street Address":
        setattr(object, "is_street_empty", False)
        select_street_address(object)
    elif object.object_choice == "Email Address":
        setattr(object, "domain", "")
        setattr(object, "is_domain_empty", False)
        select_domain(object)
    else: #routing to the target column for the name choice
        set_target_column(object)

def set_target_column(object):
    if object.object_choice == "Street Address":
        clear_middle_frame()
        setattr(object, "target_column_1", "AddressLine1")
        setattr(object, "target_column_2", "AddressLine2")
        generate_data(object)
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
        generate_data(object)
    elif object.object_choice == "Name": #setting the target firstname and lastname columns
        clear_middle_frame()
        setattr(object, "target_firstname_column", "FirstName")
        setattr(object, "target_lastname_column", "LastName")
        generate_data(object)
    elif object.object_choice == "Salary": #setting the target firstname and lastname columns
        clear_middle_frame()
        setattr(object, "target_column", "Salary")
        generate_data(object)

#=================================FILE OPERATIONS===================================#
def add_file(delim_choice): #Function that allows user to upload files with different delimiters
    if delim_choice.get() == "":
        clear_bottom_frame_except_filenamelabel()
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
            file_extension = os.path.splitext(file_name)[1]
            if file_extension != ".csv" and file_extension != ".txt" and file_extension != ".dat":
                clear_bottom_frame_except_filenamelabel()
                not_acceptable_label = Label(bottom_wrapper, text="The file type you have chosen is not acceptable.", fg="red")
                not_acceptable_label.pack()
                chooseCorrectFileBTN = Button(bottom_wrapper, text="Choose a New File", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: add_file(delim_choice))
                chooseCorrectFileBTN.pack(expand="true")
        else:
            file_name = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("DAT", "*.dat"), ("TXT", "*.txt"), ("all files", "*.*")))
            file_extension = os.path.splitext(file_name)[1]
            if file_extension != ".txt" and file_extension != ".dat":
                clear_bottom_frame_except_filenamelabel()
                not_acceptable_label = Label(bottom_wrapper, text="The file type you have chosen is not acceptable.", fg="red", padx=5, pady=5)
                not_acceptable_label.pack()
                chooseCorrectFileBTN = Button(bottom_wrapper, text="Choose a New File", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: add_file(delim_choice))
                chooseCorrectFileBTN.pack(expand="true")
        data = pd.read_csv(file_name, header=0, sep=delim_choice.get())
        file_name_label["text"] = file_name
        read_columns(data)

def read_columns(data): #Function to read columns from csv and create a list of those columns
    columns = list
    columns = data.columns.values
    clear_middle_frame()
    clear_bottom_frame_except_filenamelabel()
    display_original_data(columns, data)

def export_data(object): #Function that exports data as pipe delimited .dat file
    savePath = filedialog.asksaveasfile(mode='w', defaultextension=".dat")
    object.data.to_csv(savePath, sep = "|", index = False, line_terminator='\n')
    savePath.flush()
    print(savePath)
    if bool(savePath) == True:
        top_label["text"] = "File succesfully exported. Use the 'Convert Exported Data to ZIP' button below to zip your data."
    else:
        top_label["text"] = "File failed to export."
    clear_bottom_frame()
    export_zip_btn = Button(bottom_wrapper, text = "Convert Exported Data to ZIP", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: export_zip(savePath))
    export_zip_btn.pack()

def export_zip(name_path):                                    #function to export the data as a compressed zip file
    savePath = filedialog.askopenfile(mode='r')     #this is setting the savePath variable to a read only portion of the file dialog selection
    path = savePath.name                            #the next two lines make it to where the zip is saved wherever the application is on the machine
    the_path = str(name_path).split(".dat")[0]
    the_path = the_path.split("name='")[1]
    the_path = the_path + ".zip"
    zipFile = zipfile.ZipFile(os.path.basename(the_path) + ".zip", 'w')
    zipFile.write(path, compress_type=zipfile.ZIP_DEFLATED)         #this is the type of zip written, and can be changed if need be
    zipFile.close()
    if bool(savePath) == True:
        top_label["text"] = "File succesfully zipped. Your zipped data is located in the same location you have this app."
    else:
        top_label["text"] = "File failed to export."

def reorder_columns(object): # Function that reorders columns based on what they need the order to be **STILL NEED ORDER
    if object.object_choice == "Street Address":
        correct_order = ["METADATA", "PersonAddress", "SourceSystemID", "SourceSystemOwner", "EffectiveStartDate", "EffectiveEndDate", "AddressType", "PrimaryFlag", "AddressLine1", "AddressLine2", "AddressLine3", "AddressLine4",  "Country", "PostalCode", "Region1", "Region2", "Region3", "TownOrCity"]
        object.data = object.data[correct_order]
    elif object.object_choice == "Email Address":
        correct_order = ["METADATA", "PersonEmail", "SourceSystemID", "SourceSystemOwner", "DateFrom", "DateTo", "EmailType", "PrimaryFlag", "EmailAddress"]
        object.data = object.data[correct_order]
    elif object.object_choice == "Phone Number":
        correct_order = ["METADATA", "PersonPhone", "SourceSystemID", "SourceSystemOwner", "DateFrom", "DateTo", "PhoneType", "PrimaryFlag", "PhoneNumber"]
        object.data = object.data[correct_order]
    elif object.object_choice == "National Identifier":
        correct_order = ["METADATA", "NationalIdentifier", "SourceSystemID", "SourceSystemOwner", "EffectiveStartDate", "EffectiveEndDate", "NationalIdentifierType", "LegislationCode", "PrimaryFlag", "NationalIdentifierNumber"]
        object.data = object.data[correct_order]
    elif object.object_choice == "Name":
        correct_order = ["METADATA", "PersonName", "SourceSystemID", "SourceSystemOwner", "EffectiveStartDate", "EffectiveEndDate", "NameType", "LegislationCode", "FirstName", "LastName"]
        object.data = object.data[correct_order]

#=================================UI OPERATIONS===================================#
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
   
   

    title_text.pack(fill="x", padx=5, pady=5)      #Places title text widget in window
    top_wrapper.pack(fill="both", expand="yes", padx=20, pady=20)     #Places top_wrapper label frame in window
    middle_wrapper.pack(fill="x", expand="yes", padx=20, pady=20)  #Places middle_wrapper label frame in window
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

def clear_middle_frame(): #Function that clears the middle wrapper
    for widget in middle_wrapper.winfo_children():
        widget.destroy()

def clear_bottom_frame(): #Function that clears the middle wrapper
    for widget in bottom_wrapper.winfo_children():
        widget.destroy()

def clear_bottom_frame_except_filenamelabel(): #Function that clears the bottom wrapper
    for widget in bottom_wrapper.winfo_children():
        if widget.widgetName != "label" or widget["text"] == "Please enter the delimiter your file uses:" or widget["text"] == "No delimiter chosen." or widget["text"] == "The file type you have chosen is not acceptable.":
            widget.destroy()

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
    BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier", "Name", "Salary"]
    objectChoice = StringVar()
    objectChoice.set("--Business Object--")
    dropdownLabel = Label(middle_wrapper, text="Select the Business Object that corresponds with your file:")
    objectDropdown = OptionMenu(middle_wrapper, objectChoice, *BUSINESSOBJECTS)
    dropdownLabel.pack()
    objectDropdown.pack()
    confirmObjectBTN = Button(middle_wrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: route_configuration(object))
    confirmObjectBTN.pack()

def display_original_dropdown(columns, data): #Function that displays the dropdown to choose the business object
    BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier", "Name", "Salary"]
    objectChoice = StringVar()
    objectChoice.set("--Business Object--")
    dropdownLabel = Label(middle_wrapper, text="Select the Business Object that corresponds with your file:")
    objectDropdown = OptionMenu(middle_wrapper, objectChoice, *BUSINESSOBJECTS)
    dropdownLabel.pack()
    objectDropdown.pack()
    prior_error = False
    confirmObjectBTN = Button(middle_wrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: create_object(columns, data, objectChoice, prior_error))
    confirmObjectBTN.pack()

#=================================EMAIL ADDRESS CONFIGURATION===================================#
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

#=================================STREET ADDRESS CONFIGURATION===================================#
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
        FREQUENCY_OPTIONS = ["1/10", "1/20", "1/50", "1/100"]
        frequency_choice = tk.StringVar()
        frequency_choice.set("--Street Address Line 2 Frequency--")
        frequency_label = tk.Label(middle_wrapper, text="Select how frequent you want to generate address line 2:")
        frequency_dropdown = tk.OptionMenu(middle_wrapper, frequency_choice, *FREQUENCY_OPTIONS)
        frequency_label.pack()
        frequency_dropdown.pack()
        confirm_street_btn = tk.Button(middle_wrapper, text="Confirm Street Line 2 Frequency Choice", padx=10, pady=5, fg="white",
                                    bg="dark blue", command=lambda: set_frequency(object, frequency_choice))
        confirm_street_btn.pack(expand="true")
    else:
        clear_middle_frame()
        FREQUENCY_OPTIONS = ["1/10", "1/20", "1/50", "1/100"]
        frequency_choice = tk.StringVar()
        frequency_error_label = Label(middle_wrapper, text = "No frequency selected. Please select a frequency.", fg = "red")
        frequency_error_label.pack()
        frequency_choice.set("--Street Address Line 2 Frequency--")
        frequency_label = tk.Label(middle_wrapper, text="Select the frequency of which you want :")
        frequency_dropdown = tk.OptionMenu(middle_wrapper, frequency_choice, *FREQUENCY_OPTIONS)
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

#=================================ENGINE FUNCTIONS===================================#        
def generate_data(object): #Function that reads business object choice and directs data to corresponding generate function
    top_label["text"] = "Data has been updated and columns have been reordered. You can export by clicking the 'Export Data' button below"
    export_btn = Button(bottom_wrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: export_data(object))
    export_btn.pack()
    if object.object_choice == "Phone Number":
        generate_phone_number(object)
        reorder_columns(object)
        display_data(object)
    elif object.object_choice == "Email Address":
        generate_email_address(object)
        reorder_columns(object)
        display_data(object)
    elif object.object_choice == "Street Address":
        generate_street_address(object)
        reorder_columns(object)
        display_data(object)
    elif object.object_choice == "National Identifier":
        generate_national_identifier(object)
        reorder_columns(object)
        display_data(object)
    elif object.object_choice == "Name":
        generate_name(object)
        reorder_columns(object)
        display_data(object)
    elif object.object_choice == "Salary":
        generate_salary(object)
        reorder_columns(object)
        display_data(object)

def generate_email_address(object):            #Function that generates email addresses
    object.data[object.target_column] = object.data[object.target_column].apply(lambda x: x.split("@")[0] + "@" + object.domain)

def generate_name(object): #function that calls the method generates within the target column
    for i in object.data.index:
        object.data.at[i, object.target_firstname_column] = return_firstname()
        object.data.at[i, object.target_lastname_column] = return_lastname()

def generate_salary(object):
    for i in object.data.index:
        if i % 2 == 0:
            object.data.at[i, object.target_column] = return_5fig_salary()
        else:
            object.data.at[i, object.target_column] = return_6fig_salary()

def return_5fig_salary():
    return fake.numerify("$9#,###")

def return_6fig_salary():
    return fake.numerify("$1##,###")

def return_firstname(): #returning a fake first name
    return fake.first_name()

def return_lastname(): #returning a fake last name
    return fake.last_name()
   
def generate_street_address(object):  # Function that generates street addresses
    for i in object.data.index:
        object.data.at[i, object.target_column_1] = return_streetaddress(object.street, i)
        if object.frequency == "1/10":
            frequency = 10
            print(i % frequency)
            if i % frequency == 0:
                object.data.at[i, object.target_column_2] = return_streetaddress_line2(i)
        elif object.frequency == "1/20":
            frequency = 20
            if i % frequency == 0:
                object.data.at[i, object.target_column_2] = return_streetaddress_line2(i)
        elif object.frequency == "1/50":
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
    for i in object.data.index:
        if i % 1 == 0:
            object.data.at[i, object.target_column] = return_phone_normal_format() #normal format
    for i in object.data.index:
        if i % 3 == 1:
            object.data.at[i, object.target_column] = return_phone_format_2() #different format
    for i in object.data.index:
        if i % 5 == 1:
            object.data.at[i, object.target_column] = return_phone_format_3() #different format
   
def generate_national_identifier(object):      #Function that generates national identifiers
    for i in object.data.index:
        object.data.at[i, object.target_column] = return_SSN()

def return_SSN(): #Actual Function that generates SSN's
    return fake.ssn()

def return_phone_normal_format(): #Actual Function that generates phone numbers
    return fake.numerify("(###)-###-####")

def return_phone_format_2(): #Actual Function that generates phone numbers
    return fake.numerify("###-###-####")

def return_phone_format_3(): #Actual Function that generates phone numbers
    return fake.numerify("### ### ####")

def main():                                         #Everything within this "main()" Function is the actual application
    open_application()

if __name__ == "__main__": #Checks to make sure the file is being run as a script and not imported into another file. (Basic Python Boilerplate)
    main()