#=================================IMPORTS===================================#
from tkinter import *
from tkinter import filedialog
import pandas as pd
import zipfile
import os.path
import UI_Operations as UI
import Business_Object as BO

#=================================FILE OPERATIONS===================================#
def add_file(self): #Function that allows user to upload files with different delimiters
    if self.delim_choice.get() == "":
        UI.clear_bottom_frame_except_filenamelabel(self)
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
                UI.clear_bottom_frame_except_filenamelabel(self)
                self.not_acceptable_label = Label(self.bottom_wrapper, text="The file type you have chosen is not acceptable.", fg="red")
                self.not_acceptable_label.pack()
                self.choose_correct_file_btn = Button(self.bottom_wrapper, text="Choose a New File", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: add_file(self))
                self.choose_correct_file_btn.pack(expand="true")
        else:
            file_name = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("DAT", "*.dat"), ("TXT", "*.txt"), ("all files", "*.*")))
            file_extension = os.path.splitext(file_name)[1]
            if file_extension != ".txt" and file_extension != ".dat":
                UI.clear_bottom_frame_except_filenamelabel(self)
                self.not_acceptable_label = Label(self.bottom_wrapper, text="The file type you have chosen is not acceptable.", fg="red", padx=5, pady=5)
                self.not_acceptable_label.pack()
                self.choose_correct_file_btn = Button(self.bottom_wrapper, text="Choose a New File", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: add_file(self))
                self.choose_correct_file_btn.pack(expand="true")
        data = pd.read_csv(file_name, header=0, sep=self.delim_choice.get())
        self.file_name_label["text"] = file_name
        prior_error = False
        is_generated = False
        object = BO.BusinessObject(data, prior_error, is_generated)
        read_columns(object, self)

def read_columns(object, self): #Function to read columns from csv and create a list of those columns
    object.columns = list
    object.columns = object.data.columns.values
    UI.clear_middle_frame(self)
    UI.clear_bottom_frame_except_filenamelabel(self)
    UI.display_data(object, self)

def export_data(object, self): #Function that exports data as pipe delimited .dat file
    savePath = filedialog.asksaveasfile(mode='w', defaultextension=".dat")
    object.data.to_csv(savePath, sep = "|", index = False, line_terminator='\n')
    savePath.flush()
    if bool(savePath) == True:
        self.top_label["text"] = "File succesfully exported. Use the 'Convert Exported Data to ZIP' button below to zip your data."
    else:
        self.top_label["text"] = "File failed to export."
    UI.clear_bottom_frame_except_filenamelabel(self)
    self.export_zip_btn = Button(self.bottom_wrapper, text = "Convert Exported Data to ZIP", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: export_zip(savePath, self))
    self.export_zip_btn.pack()
    self.restart_btn = Button(self.bottom_wrapper, text = "Scramble New Business Object", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: UI.restart_app(self))
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
        object.data = object.data.drop('Gender', 1)
        correct_order = ["METADATA", "PersonName", "SourceSystemID", "SourceSystemOwner", "EffectiveStartDate", "EffectiveEndDate", "NameType", "LegislationCode", "FirstName", "LastName"]
        object.data = object.data[correct_order]
    elif object.object_choice == "Salary":
        correct_order = ["METADATA", "Salary", "SourceSystemID", "SourceSystemOwner", "DateFrom", "DateTo", "SalaryBasisName", "SalaryAmount"]
        object.data = object.data[correct_order]
    elif object.object_choice == "Username":
        correct_order = ["METADATA", "User", "SourceSystemID", "SourceSystemOwner", "Username"]
        object.data = object.data[correct_order]
    elif object.object_choice == "Emergency Contact Name":
        object.data = object.data.drop('Gender', 1)
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