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
import random

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

def create_object(columns, data, objectChoice, prior_error, self):
    object = BusinessObject(data, columns, objectChoice.get(), prior_error)
    if object.object_choice == "Emergency Contact":
        display_emergency_contact_dropdown(object, self)
    else:
        create_columns(object, self)

def create_columns(object, self):
    if object.object_choice == "Street Address":
        object.data["AddressLine1"] = ""
        object.data["AddressLine2"] = ""
        object.data["METADATA"] = "MERGE"
        object.data["PersonAddress"] = "PersonAddress"
        route_configuration(object, self)
    elif object.object_choice == "Phone Number":
        object.data["PhoneNumber"] = ""
        object.data["METADATA"] = "MERGE"
        object.data["PersonPhone"] = "PersonPhone"
        route_configuration(object, self)
    elif object.object_choice == "National Identifier":
        object.data["NationalIdentifierNumber"] = ""
        object.data["METADATA"] = "MERGE"
        object.data["NationalIdentifier"] = "NationalIdentifier"
        route_configuration(object, self)
    elif object.object_choice == "Email Address":
        object.data["METADATA"] = "MERGE"
        object.data["PersonEmail"] = "PersonEmail"
        print(object.data)
        route_configuration(object, self)
    elif object.object_choice == "Name":
        object.data["METADATA"] = "MERGE"
        object.data["PersonName"] = "PersonName"
        object.data["FirstName"] = ""
        object.data["LastName"] = ""
        route_configuration(object, self)
    elif object.object_choice == "Salary":
        object.data["METADATA"] = "MERGE"
        object.data["Salary"] = "Salary"
        object.data["SalaryAmount"] = ""
        route_configuration(object, self)
    elif object.object_choice == "Username":
        object.data["METADATA"] = "MERGE"
        object.data["User"] = "User"
        route_configuration(object, self)

def route_configuration(object, self):
    if object.object_choice == "Street Address":
        setattr(object, "is_street_empty", False)
        select_street_address(object, self)
    elif object.object_choice == "Email Address":
        setattr(object, "domain", "")
        setattr(object, "is_domain_empty", False)
        select_domain(object, self)
    elif object.object_choice == "Username":
        setattr(object, "username", "")
        setattr(object, "is_username_empty", False)
        select_username(object, self)
    else:
        set_target_column(object, self)

def set_target_column(object, self):
    clear_middle_frame(self)
    if object.object_choice == "Street Address":
        setattr(object, "target_column_1", "AddressLine1")
        setattr(object, "target_column_2", "AddressLine2")
    elif object.object_choice == "Phone Number":
        setattr(object, "target_column", "PhoneNumber")
    elif object.object_choice == "National Identifier":
        setattr(object, "target_column", "NationalIdentifier")
    elif object.object_choice == "Email Address":
        setattr(object, "target_column", "EmailAddress")
    elif object.object_choice == "Name": #setting the target firstname and lastname columns
        setattr(object, "target_firstname_column", "FirstName")
        setattr(object, "target_lastname_column", "LastName")
    elif object.object_choice == "Salary": #setting the target firstname and lastname columns
        setattr(object, "target_column", "SalaryAmount")
    elif object.object_choice == "Username":
        setattr(object, "target_username_column", "Username")
    elif object.object_choice == "Emergency Contact Name":  # setting the target firstname and lastname columns
        setattr(object, "target_contact_firstname_column", "FirstName")
        setattr(object, "target_contact_lastname_column", "LastName")
    elif object.object_choice == "Emergency Contact Street Address":
        setattr(object, "target_contact_column_1", "AddressLine1")
        setattr(object, "target_contact_column_2", "AddressLine2")
    elif object.object_choice == "Emergency Contact Phone Number":
        setattr(object, "target_contact_phone_column", "PhoneNumber")
    elif object.object_choice == "Emergency Contact Email Address":
        setattr(object, "target_column", "EmailAddress")
    generate_data(object, self)

#=================================FILE OPERATIONS===================================#
def add_file(self): #Function that allows user to upload files with different delimiters
    if self.delim_choice.get() == "":
        clear_bottom_frame_except_filenamelabel(self)
        self.delim_choice = StringVar()
        self.no_delimiter_label = Label(self.bottom_wrapper, text = "No delimiter chosen.", fg = "red")
        self.no_delimiter_label.pack()
        self.delim_entry_label = Label(self.bottom_wrapper, text = "Please enter the delimiter your file uses:")
        self.delim_entry = Entry(self.bottom_wrapper, textvariable = self.delim_choice)
        self.delim_confirm_btn = Button(self.bottom_wrapper, text="Confirm Delimiter", command = lambda: add_file(self))
        self.delim_entry_label.pack()
        self.delim_entry.pack()
        self.delim_confirm_btn.pack(padx = 20, pady = 5)
    else:
        if self.delim_choice.get() == ',':
            file_name = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("CSV", "*.csv"), ("all files", "*.*")))
            file_extension = os.path.splitext(file_name)[1]
            if file_extension != ".csv" and file_extension != ".txt" and file_extension != ".dat":
                clear_bottom_frame_except_filenamelabel(self)
                self.not_acceptable_label = Label(self.bottom_wrapper, text="The file type you have chosen is not acceptable.", fg="red")
                self.not_acceptable_label.pack()
                self.chooseCorrectFileBTN = Button(self.bottom_wrapper, text="Choose a New File", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: add_file(self))
                self.chooseCorrectFileBTN.pack(expand="true")
        else:
            file_name = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("DAT", "*.dat"), ("TXT", "*.txt"), ("all files", "*.*")))
            file_extension = os.path.splitext(file_name)[1]
            if file_extension != ".txt" and file_extension != ".dat":
                clear_bottom_frame_except_filenamelabel(self)
                self.not_acceptable_label = Label(self.bottom_wrapper, text="The file type you have chosen is not acceptable.", fg="red", padx=5, pady=5)
                self.not_acceptable_label.pack()
                self.chooseCorrectFileBTN = Button(self.bottom_wrapper, text="Choose a New File", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: add_file(self))
                self.chooseCorrectFileBTN.pack(expand="true")
        data = pd.read_csv(file_name, header=0, sep=self.delim_choice.get())
        self.file_name_label["text"] = file_name
        read_columns(data, self)

def read_columns(data, self): #Function to read columns from csv and create a list of those columns
    columns = list
    columns = data.columns.values
    clear_middle_frame(self)
    clear_bottom_frame_except_filenamelabel(self)
    display_original_data(columns, data, self)

def export_data(object, self): #Function that exports data as pipe delimited .dat file
    savePath = filedialog.asksaveasfile(mode='w', defaultextension=".dat")
    object.data.to_csv(savePath, sep = "|", index = False, line_terminator='\n')
    savePath.flush()
    print(savePath)
    if bool(savePath) == True:
        self.top_label["text"] = "File succesfully exported. Use the 'Convert Exported Data to ZIP' button below to zip your data."
    else:
        self.top_label["text"] = "File failed to export."
    clear_bottom_frame_except_filenamelabel(self)
    self.export_zip_btn = Button(self.bottom_wrapper, text = "Convert Exported Data to ZIP", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: export_zip(savePath, self))
    self.export_zip_btn.pack()
    self.restart_btn = Button(self.bottom_wrapper, text = "Scramble New Business Object", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: restart_app(self))
    self.restart_btn.pack()

def export_zip(name_path, self):                                    #function to export the data as a compressed zip file
    savePath = filedialog.askopenfile(mode='r')     #this is setting the savePath variable to a read only portion of the file dialog selection
    path = savePath.name                            #the next two lines make it to where the zip is saved wherever the application is on the machine
    the_path = str(name_path).split(".dat")[0]
    the_path = the_path.split("name='")[1]
    the_path = the_path + ".zip"
    zipFile = zipfile.ZipFile(os.path.basename(the_path), 'w')
    zipFile.write(path, os.path.basename(path), compress_type = zipfile.ZIP_DEFLATED)         #this is the type of zip written, and can be changed if need be
    zipFile.close()
    if bool(savePath) == True:
        self.top_label["text"] = "File succesfully zipped. Your zipped data is located in the same location you have this app."
    else:
        self.top_label["text"] = "File failed to export."

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
    elif object.object_choice == "Salary":
        correct_order = ["METADATA", "Salary", "SourceSystemID", "SourceSystemOwner", "DateFrom", "DateTo", "SalaryBasisName", "SalaryAmount"]
        object.data = object.data[correct_order]
    elif object.object_choice == "Username":
        correct_order = ["METADATA", "User", "SourceSystemID", "SourceSystemOwner", "Username"]
        object.data = object.data[correct_order]
    elif object.object_choice == "Emergency Contact Name":
        correct_order = ["METADATA", "ContactName", "SourceSystemID", "SourceSystemOwner", "EffectiveStartDate", "EffectiveEndDate", "NameType", "LegislationCode", "FirstName", "LastName"]
        object.data = object.data[correct_order]
    elif object.object_choice == "Emergency Contact Phone Number":
        correct_order = ["METADATA", "ContactPhone", "SourceSystemID", "SourceSystemOwner", "DateFrom", "DateTo", "PhoneType", "PrimaryFlag", "PhoneNumber"]
        object.data = object.data[correct_order]
    elif object.object_choice == "Emergency Contact Street Address":
        correct_order = ["METADATA", "ContactAddress", "SourceSystemID", "SourceSystemOwner", "EffectiveStartDate", "EffectiveEndDate", "AddressType", "PrimaryFlag", "AddressLine1", "AddressLine2", "AddressLine3", "AddressLine4",  "Country", "PostalCode", "Region1", "Region2", "Region3", "TownOrCity"]
        object.data = object.data[correct_order]
    elif object.object_choice == "Emergency Contact Email Address":
        correct_order = ["METADATA", "ContactEmail", "SourceSystemID", "SourceSystemOwner", "DateFrom", "DateTo", "EmailType", "PrimaryFlag", "EmailAddress"]
        object.data = object.data[correct_order]

#=================================UI OPERATIONS===================================#
class Application(object):
    def __init__(self, event=None):
        self.root = Tk()
        self.title_font = ("Calibri", 20, "bold")
        self.small_font = ("Calibri", 10, "bold")

        self.title_text = Label(self.root, text="Welcome to the Automated Data Scrambling Engine!", font=self.title_font) #Creates text that appears at top of application
        self.top_wrapper = LabelFrame(self.root, text="Preview")                                    #Creates preview Section
        self.middle_wrapper = LabelFrame(self.root, text="Configuration")                           #Creates configure Section
        self.bottom_wrapper = LabelFrame(self.root, text="Current File")                            #Creates select File section
        self.file_name_label = Label(self.bottom_wrapper, text="No file selected", name = "file_name_label")                    #Creates text for selected file name
        self.top_label = Label(self.top_wrapper, text="View preview of data here:", font=self.small_font)                  #Creates text for top label
        self.tv1 = ttk.Treeview(self.top_wrapper)                                                   #Creates treeview for previewing data
        self.delim_choice = StringVar()
        self.delim_entry_label = Label(self.bottom_wrapper, text = "Please enter the delimiter your file uses:")
        self.delim_entry = Entry(self.bottom_wrapper, textvariable = self.delim_choice)
        self.delim_confirm_btn = Button(self.bottom_wrapper, text="Confirm Delimiter", command = lambda: add_file(self))
        self.treescrolly = Scrollbar(self.tv1, orient="vertical", command=self.tv1.yview)            #Updates the y-axis view of the widget
        self.treescrollx = Scrollbar(self.tv1, orient="horizontal", command=self.tv1.xview)          #Updates the x-axis view of the widget
        self.tv1.configure(xscrollcommand=self.treescrollx.set, yscrollcommand=self.treescrolly.set)    #Assigns the scrollbars to the Treeview
    
    

        self.title_text.pack(fill="x", padx=5, pady=5)      #Places title text widget in window
        self.top_wrapper.pack(fill="both", expand="yes", padx=20, pady=20)     #Places top_wrapper label frame in window
        self.middle_wrapper.pack(fill="x", expand="yes", padx=20, pady=20)  #Places middle_wrapper label frame in window
        self.bottom_wrapper.pack(fill="x", padx=20, pady=20)  #Places bottom_wrapper label frame in window
        self.file_name_label.pack()                                             #Places fileName Label in bottom_wrapper frame
        self.top_label.pack()                                                  #Places top label in top wrapper frame          
        self.tv1.pack(fill="both", expand="yes", padx=20, pady=20)            #Places treeview in top_wrapper frame
        self.treescrollx.pack(side="bottom", fill="x")                        #Makes the scrollbar fill the x axis of the Treeview widget
        self.treescrolly.pack(side="right", fill="y")                         #Makes the scrollbar fill the y axis of the Treeview widget
        self.delim_entry_label.pack()
        self.delim_entry.pack()
        self.delim_confirm_btn.pack(padx = 20, pady = 5)


        self.root.title("Automated Data Scrambling Engine")  #Sets window title to the name of our project
        self.root.geometry("800x700")                        #Sets window size to 800x700 pixels
        self.root.mainloop()                                 #Keeps window open and running

def restart_app(self):
    self.root.destroy()
    app = Application()

def clear_middle_frame(self): #Function that clears the middle wrapper
    for widget in self.middle_wrapper.winfo_children():
        widget.destroy()

def clear_bottom_frame(self): #Function that clears the middle wrapper
    for widget in self.bottom_wrapper.winfo_children():
        widget.destroy()

def clear_bottom_frame_except_filenamelabel(self): #Function that clears the bottom wrapper
    for widget in self.bottom_wrapper.winfo_children():
        if widget.widgetName != "label" or widget["text"] == "Please enter the delimiter your file uses:" or widget["text"] == "No delimiter chosen." or widget["text"] == "The file type you have chosen is not acceptable.":
            widget.destroy()

def display_original_data(columns, data, self): #Function that displays csv data in the preview
    clear_data(self)
    data_without_NaN = data.replace(np.nan, '', regex=True)
    self.tv1["columns"] = columns
    self.tv1["show"] = "headings"
    for column in self.tv1["columns"]:
        self.tv1.heading(column, text=column)
    df_rows = data_without_NaN.to_numpy().tolist()
    count = 0
    for row in df_rows:
        if count < 20:
            self.tv1.insert("", "end", values=row)
            count += 1
    display_original_dropdown(columns, data, self)

def display_data(object, self): #Function that displays csv data in the preview
    clear_data(self)
    object.columns = object.data.columns.values
    data_without_NaN = object.data.replace(np.nan, '', regex=True)
    self.tv1["columns"] = object.columns
    self.tv1["show"] = "headings"
    for column in self.tv1["columns"]:
        self.tv1.heading(column, text=column)
    df_rows = data_without_NaN.to_numpy().tolist()
    count = 0
    for row in df_rows:
        if count < 20:
            self.tv1.insert("", "end", values=row)
            count += 1
    display_dropdown(object, self)

def clear_data(self): #Function that clears the preview so that it can be repopulated
    self.tv1.delete(*self.tv1.get_children())

def display_dropdown(object, self): #Function that displays the dropdown to choose the business object
    BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier", "Name", "Salary", "Username", "Emergency Contact"]
    objectChoice = StringVar()
    objectChoice.set("--Business Object--")
    self.dropdownLabel = Label(self.middle_wrapper, text="Select the Business Object that corresponds with your file:")
    self.objectDropdown = OptionMenu(self.middle_wrapper, objectChoice, *BUSINESSOBJECTS)
    self.dropdownLabel.pack()
    self.objectDropdown.pack()
    self.confirmObjectBTN = Button(self.middle_wrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: route_configuration(object, self))
    self.confirmObjectBTN.pack()

def display_original_dropdown(columns, data, self): #Function that displays the dropdown to choose the business object
    BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier", "Name", "Salary", "Username", "Emergency Contact"]
    objectChoice = StringVar()
    objectChoice.set("--Business Object--")
    self.dropdownLabel = Label(self.middle_wrapper, text="Select the Business Object that corresponds with your file:")
    self.objectDropdown = OptionMenu(self.middle_wrapper, objectChoice, *BUSINESSOBJECTS)
    self.dropdownLabel.pack()
    self.objectDropdown.pack()
    prior_error = False
    self.confirmObjectBTN = Button(self.middle_wrapper, text="Confirm Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: create_object(columns, data, objectChoice, prior_error, self))
    self.confirmObjectBTN.pack()

#=================================EMERGENCY CONTACT CONFIGURATION===================================#
def display_emergency_contact_dropdown(object, self): #Function that displays the dropdown to choose the emergency contact business object
    clear_middle_frame(self)
    EMERGENCYCONTACTOBJECTS = ["Emergency Contact Name", "Emergency Contact Phone Number", "Emergency Contact Street Address", "Emergency Contact Email Address"]
    contactObjectChoice = StringVar()
    contactObjectChoice.set("--Emergency Contact Business Object--")
    self.contactDropdownLabel = Label(self.middle_wrapper, text="Select the Emergency Contact Business Object that corresponds with your file:")
    self.contactObjectDropdown = OptionMenu(self.middle_wrapper, contactObjectChoice, *EMERGENCYCONTACTOBJECTS)
    self.contactDropdownLabel.pack()
    self.contactObjectDropdown.pack()
    self.confirmContactObjectBTN = Button(self.middle_wrapper, text="Confirm Emergency Contact Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_emergency_contact_object(object, self, contactObjectChoice))
    self.confirmContactObjectBTN.pack()

def set_emergency_contact_object(object, self, contact_object_choice):
    setattr(object, "object_choice", contact_object_choice.get())
    create_emergency_contact_columns(object, self)

def create_emergency_contact_columns(object, self):
    if object.object_choice == "Emergency Contact Name":  # adding in emergency contact methods to the pre-existing methods
        object.data["METADATA"] = "MERGE"
        object.data["ContactName"] = "ContactName"
        object.data["FirstName"] = ""
        object.data["LastName"] = ""
    elif object.object_choice == "Emergency Contact Phone Number":
        object.data["PhoneNumber"] = ""
        object.data["METADATA"] = "MERGE"
        object.data["ContactPhone"] = "ContactPhone"
    elif object.object_choice == "Emergency Contact Street Address":
        object.data["AddressLine1"] = ""
        object.data["AddressLine2"] = ""
        object.data["METADATA"] = "MERGE"
        object.data["ContactAddress"] = "ContactAddress"
    elif object.object_choice == "Emergency Contact Email Address":
        object.data["METADATA"] = "MERGE"
        object.data["ContactEmail"] = "ContactEmail"
    route_emergency_contact_configuration(object, self)

def route_emergency_contact_configuration(object, self):
    if object.object_choice == "Emergency Contact Street Address":
        setattr(object, "is_street_empty", False)
        select_street_address(object, self)
    elif object.object_choice == "Emergency Contact Email Address":
        setattr(object, "domain", "")
        setattr(object, "is_domain_empty", False)
        select_domain(object, self)
    else:
        set_target_column(object, self)

#=================================EMAIL ADDRESS CONFIGURATION===================================#
def select_domain(object, self): #Function that prompts user to enter a domain for generated email addresses
    if object.is_domain_empty == False:
        clear_middle_frame(self)
        domain_choice = StringVar()
        self.domain_entry_label = Label(self.middle_wrapper, text = "Please enter the domain you want to use for generated data:")
        self.domain_entry = Entry(self.middle_wrapper, textvariable = domain_choice)
        self.confirm_domain_btn = Button(self.middle_wrapper, text="Confirm Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_domain(object, domain_choice, self))
        self.domain_entry_label.pack()
        self.domain_entry.pack()
        self.confirm_domain_btn.pack()
    else:
        clear_middle_frame(self)
        self.empty_domain_label = Label(self.middle_wrapper, text = "The domain is empty. Please enter a domain.", fg = "red")
        self.empty_domain_label.pack()
        domain_choice = StringVar()
        self.domain_entry_label = Label(self.middle_wrapper, text = "Please enter the domain you want to use for generated data:")
        self.domain_entry = Entry(self.middle_wrapper, textvariable = domain_choice)
        self.confirm_domain_btn = Button(self.middle_wrapper, text="Confirm Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_domain(object, domain_choice, self))
        self.domain_entry_label.pack()
        self.domain_entry.pack()
        self.confirm_domain_btn.pack()
    
def set_domain(object, domain_choice, self):
    if domain_choice.get() == "":
        object.is_domain_empty = True
        select_domain(object, self)
    else:
        setattr(object, "domain", domain_choice.get())
        confirm_domain(object, self)

def confirm_domain(object, self):
    clear_middle_frame(self)
    self.domain_label = Label(self.middle_wrapper, text = f"You entered '{object.domain}' as the domain. Please confirm choice or go back.", padx=10, pady=5,)
    self.confirm_domain_choice_button = Button(self.middle_wrapper, text="Confirm Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_target_column(object, self))
    self.redo_domain_button = Button(self.middle_wrapper, text="Edit Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: redo_domain(object, self))
    self.domain_label.pack()
    self.confirm_domain_choice_button.pack()
    self.redo_domain_button.pack()

def redo_domain(object, self):
    delattr(object, "domain")
    select_domain(object, self)

#=================================USERNAME CONFIGURATION===================================#
def select_username(object, self): #Function that prompts user to enter a username generated usernames
    if object.is_username_empty == False:
        clear_middle_frame(self)
        username_choice = StringVar()
        self.username_entry_label = Label(self.middle_wrapper, text = "Please enter the username you want to use for generated data:")
        self.username_entry = Entry(self.middle_wrapper, textvariable = username_choice)
        self.confirm_username_btn = Button(self.middle_wrapper, text="Confirm Username", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_username(object, username_choice, self))
        self.username_entry_label.pack()
        self.username_entry.pack()
        self.confirm_username_btn.pack()
    else:
        clear_middle_frame(self)
        self.empty_username_label = Label(self.middle_wrapper, text = "The username is empty. Please enter a username.", fg = "red")
        self.empty_username_label.pack()
        username_choice = StringVar()
        self.username_entry_label = Label(self.middle_wrapper, text = "Please enter the username you want to use for generated data:")
        self.username_entry = Entry(self.middle_wrapper, textvariable = username_choice)
        self.confirm_username_btn = Button(self.middle_wrapper, text="Confirm Username", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_username(object, username_choice, self))
        self.username_entry_label.pack()
        self.username_entry.pack()
        self.confirm_username_btn.pack()

def set_username(object, username_choice, self):
    if username_choice.get() == "":
        object.is_username_empty = True
        select_username(object, self)
    else:
        setattr(object, "username", username_choice.get())
        set_target_column(object, self)

def confirm_username(object, self):
    clear_middle_frame(self)
    self.domain_label = Label(self.middle_wrapper, text = f"You entered '{object.domain}' as the domain. Please confirm choice or go back.", padx=10, pady=5,)
    self.confirm_domain_choice_button = Button(self.middle_wrapper, text="Confirm Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_target_column(object, self))
    self.redo_domain_button = Button(self.middle_wrapper, text="Edit Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: redo_domain(object, self))
    self.domain_label.pack()
    self.confirm_domain_choice_button.pack()
    self.redo_domain_button.pack()

def redo_domain(object, self):
    delattr(object, "domain")
    select_domain(object, self)

#=================================STREET ADDRESS CONFIGURATION===================================#
def select_street_address(object, self): #Function that prompts user to enter a street name for generated street addresses
    if object.is_street_empty == False:
        clear_middle_frame(self)
        street_choice = StringVar()
        self.entry_label_street = Label(self.middle_wrapper, text="Please enter the street address you want to use for generated data:")
        self.street_entry = Entry(self.middle_wrapper, textvariable=street_choice)
        self.confirm_street_btn = tk.Button(self.middle_wrapper, text="Confirm Street Name", padx=10, pady=5, fg="white", bg="dark blue",
                                    command=lambda: set_street_address(object, street_choice, self))
        self.entry_label_street.pack()
        self.street_entry.pack()
        self.confirm_street_btn.pack()
    else:
        clear_middle_frame(self)
        self.empty_street_label = Label(self.middle_wrapper, text = "The street name is empty. Please enter a street name.", fg = "red")
        self.empty_street_label.pack()
        street_choice = StringVar()
        self.entry_label_street = Label(self.middle_wrapper, text="Please enter the street address you want to use for generated data:")
        self.street_entry = Entry(self.middle_wrapper, textvariable=street_choice)
        self.confirm_street_btn = tk.Button(self.middle_wrapper, text="Confirm Street Name", padx=10, pady=5, fg="white", bg="dark blue",
                                    command=lambda: set_street_address(object, street_choice, self))
        self.entry_label_street.pack()
        self.street_entry.pack()
        self.confirm_street_btn.pack()

def set_street_address(object, street_choice, self):
    if street_choice.get() == "":
        object.is_street_empty = True
        select_street_address(object, self)
    else:
        setattr(object, "street", street_choice.get())
        setattr(object, "frequency_error", False)
        confirm_street(object, self)

def confirm_street(object, self):
    clear_middle_frame(self)
    self.street_label = Label(self.middle_wrapper, text = f"You entered '{object.street}' as the street name. Please confirm choice or go back.", padx=10, pady=5,)
    self.confirm_street_choice_button = Button(self.middle_wrapper, text="Confirm Street Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: select_frequency(object, self))
    self.redo_street_button = Button(self.middle_wrapper, text="Edit Street Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: redo_street(object, self))
    self.street_label.pack()
    self.confirm_street_choice_button.pack()
    self.redo_street_button.pack()

def redo_street(object, self):
    delattr(object, "street")
    select_street_address(object, self)

def select_frequency(object, self):  # Function that displays the dropdown to choose the street line 2 frequency
    if object.frequency_error == False:
        clear_middle_frame(self)
        FREQUENCY_OPTIONS = ["1/10", "1/20", "1/50", "1/100"]
        frequency_choice = tk.StringVar()
        frequency_choice.set("--Street Address Line 2 Frequency--")
        self.frequency_label = tk.Label(self.middle_wrapper, text="Select how frequent you want to generate address line 2:")
        self.frequency_dropdown = tk.OptionMenu(self.middle_wrapper, frequency_choice, *FREQUENCY_OPTIONS)
        self.frequency_label.pack()
        self.frequency_dropdown.pack()
        self.confirm_street_btn = tk.Button(self.middle_wrapper, text="Confirm Street Line 2 Frequency Choice", padx=10, pady=5, fg="white",
                                    bg="dark blue", command=lambda: set_frequency(object, frequency_choice, self))
        self.confirm_street_btn.pack(expand="true")
    else:
        clear_middle_frame(self)
        FREQUENCY_OPTIONS = ["1/10", "1/20", "1/50", "1/100"]
        frequency_choice = tk.StringVar()
        frequency_choice.set("--Street Address Line 2 Frequency--")
        self.frequency_error_label = Label(self.middle_wrapper, text = "No frequency selected. Please select a frequency.", fg = "red")
        self.frequency_error_label.pack()
        self.frequency_label = tk.Label(self.middle_wrapper, text="Select the frequency of which you want :")
        self.frequency_dropdown = tk.OptionMenu(self.middle_wrapper, frequency_choice, *FREQUENCY_OPTIONS)
        self.frequency_label.pack()
        self.frequency_dropdown.pack()
        self.confirm_street_btn = tk.Button(self.middle_wrapper, text="Confirm Street Line 2 Frequency Choice", padx=10, pady=5, fg="white",
                                    bg="dark blue", command=lambda: set_frequency(object, frequency_choice, self))
        self.confirm_street_btn.pack(expand="true")

def set_frequency(object, frequency_choice, self):
    if frequency_choice.get() == "--Street Address Line 2 Frequency--":
        object.frequency_error = True
        select_frequency(object, self)
    else:
        setattr(object, "frequency", frequency_choice.get())
        confirm_frequency(object, self)

def confirm_frequency(object, self):
    clear_middle_frame(self)
    self.frequency_label = Label(self.middle_wrapper, text = f"You selected '{object.frequency}' as the frequency. Please confirm choice or go back.", padx=10, pady=5,)
    self.confirm_frequency_choice_button = Button(self.middle_wrapper, text="Confirm Frequency", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_target_column(object, self))
    self.redo_frequency_button = Button(self.middle_wrapper, text="Change Frequency", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: redo_frequency(object, self))
    self.frequency_label.pack()
    self.confirm_frequency_choice_button.pack()
    self.redo_frequency_button.pack()

def redo_frequency(object, self):
    delattr(object, "frequency")
    select_frequency(object, self)

#=================================ENGINE FUNCTIONS===================================#        
def generate_data(object, self): #Function that reads business object choice and directs data to corresponding generate function
    self.top_label["text"] = "Data has been updated and columns have been reordered. You can export by clicking the 'Export Data' button below"
    self.export_btn = Button(self.bottom_wrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: export_data(object, self))
    self.export_btn.pack()
    if object.object_choice == "Phone Number":
        generate_phone_number(object)
    elif object.object_choice == "Email Address":
        generate_email_address(object)
    elif object.object_choice == "Street Address":
        generate_street_address(object)
    elif object.object_choice == "National Identifier":
        generate_national_identifier(object)
    elif object.object_choice == "Name":
        generate_name(object)
    elif object.object_choice == "Salary":
        generate_salary(object)
    elif object.object_choice == "Emergency Contact Name":
        generate_contact_name(object)
    elif object.object_choice == "Emergency Contact Phone Number":
        generate_contact_phone_number(object)
    elif object.object_choice == "Emergency Contact Street Address":
        generate_contact_street_address(object)
    elif object.object_choice == "Emergency Contact Email Address":
        generate_email_address(object)
    reorder_columns(object)
    display_data(object, self)

def generate_email_address(object):            #Function that generates email addresses
    object.data[object.target_column] = object.data[object.target_column].apply(lambda x: x.split("@")[0] + "@" + object.domain)

def generate_name(object): #function that calls the method generates within the target column
    for i in object.data.index:
        object.data.at[i, object.target_firstname_column] = return_firstname()
        object.data.at[i, object.target_lastname_column] = return_lastname()

def generate_salary(object):
    for i in object.data.index:
        if object.data.at[i, 'SalaryBasisName'] == 'Annual Salary':
            object.data.at[i, object.target_column] = return_annual_salary()
        else:
            object.data.at[i, object.target_column] = return_hourly_salary()

def generate_contact_name(object): #function that calls the method generates within the target column for emergency contact
    for i in object.data.index:
        object.data.at[i, object.target_contact_firstname_column] = return_firstname()
        object.data.at[i, object.target_contact_lastname_column] = return_lastname()

def generate_contact_name(object): #function that calls the method generates within the target column for emergency contact
    for i in object.data.index:
        object.data.at[i, object.target_contact_firstname_column] = return_firstname()
        object.data.at[i, object.target_contact_lastname_column] = return_lastname()

#adding in the generation method for emergency contact phone number
def generate_contact_phone_number(object):
    for i in object.data.index:
        if i % 1 == 0:
            object.data.at[i, object.target_contact_phone_column] = return_phone_normal_format() #normal format
    for i in object.data.index:
        if i % 3 == 1:
            object.data.at[i, object.target_contact_phone_column] = return_phone_format_2() #different format
    for i in object.data.index:
        if i % 5 == 1:
            object.data.at[i, object.target_contact_phone_column] = return_phone_format_3() #different format

#adding in the generation method for emergency contact street address
def generate_contact_street_address(object):
    for i in object.data.index:
        object.data.at[i, object.target_contact_column_1] = return_contact_streetaddress(object.street, i)
        if object.frequency == "1/10":
            frequency = 10
            print(i % frequency)
            if i % frequency == 0:
                object.data.at[i, object.target_contact_column_2] = return_contact_streetaddress_line2(i)
        elif object.frequency == "1/20":
            frequency = 20
            if i % frequency == 0:
                object.data.at[i, object.target_contact_column_2] = return_contact_streetaddress_line2(i)
        elif object.frequency == "1/50":
            frequency = 50
            if i % frequency == 0:
                object.data.at[i, object.target_contact_column_2] = return_contact_streetaddress_line2(i)
        else:
            frequency = 100
            if i % frequency == 0:
                object.data.at[i, object.target_contact_column_2] = return_contact_streetaddress_line2(i)

def return_contact_streetaddress(street_choice, i):
    x = str(i + 110)
    return x + " " + street_choice  # for each piece of data, create an address with their street name and incremented


def return_contact_streetaddress_line2(i):  # this method will generate the line 2 data in the column if divisible by the frequency choice
    x = str(i + 11)
    return "Unit " + x

def return_annual_salary():
    x = random.randrange(65000, 200000)
    return x

def return_hourly_salary():
    x = random.randrange(10, 40)
    return x

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
    app = Application()

if __name__ == "__main__": #Checks to make sure the file is being run as a script and not imported into another file. (Basic Python Boilerplate)
    main()