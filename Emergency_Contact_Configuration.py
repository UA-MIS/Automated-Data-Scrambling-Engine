#=================================IMPORTS===================================#
from tkinter import *
import UI_Operations as UI
import Street_Address_Configuration as SA
import Email_Address_Configuration as EA
import Business_Object as BO

#=================================EMERGENCY CONTACT CONFIGURATION===================================#
def display_emergency_contact_dropdown(object, self): #Function that displays the dropdown to choose the emergency contact business object
    if object.prior_error == False:
        UI.clear_middle_frame(self)
        EMERGENCYCONTACTOBJECTS = ["Emergency Contact Name", "Emergency Contact Phone Number", "Emergency Contact Street Address", "Emergency Contact Email Address"]
        contact_object_choice = StringVar()
        contact_object_choice.set("--Emergency Contact Business Object--")
        self.contactDropdownLabel = Label(self.middle_wrapper, text="Select the Emergency Contact Business Object that corresponds with your file:")
        self.contactObjectDropdown = OptionMenu(self.middle_wrapper, contact_object_choice, *EMERGENCYCONTACTOBJECTS)
        self.contactDropdownLabel.pack(padx=2.5, pady=2.5)
        self.contactObjectDropdown.pack(padx=2.5, pady=2.5)
        self.confirmContactObjectBTN = Button(self.middle_wrapper, text="Confirm Emergency Contact Business Object Choice", fg="white", bg="#990000", command=lambda: check_emergency_contact_columns(object, self, contact_object_choice))
        self.confirmContactObjectBTN.pack(padx=2.5, pady=2.5)
    else:
        UI.clear_middle_frame(self)
        EMERGENCYCONTACTOBJECTS = ["Emergency Contact Name", "Emergency Contact Phone Number", "Emergency Contact Street Address", "Emergency Contact Email Address"]
        contact_object_choice = StringVar()
        contact_object_choice.set("--Emergency Contact Business Object--")
        self.error_label = Label(self.middle_wrapper, text="You did not select a business object or the business object you selected does not correspond with your file.\n Please select the correct business object from the dropdown below.", fg="red")
        self.contactDropdownLabel = Label(self.middle_wrapper, text="Select the Emergency Contact Business Object that corresponds with your file:")
        self.contactObjectDropdown = OptionMenu(self.middle_wrapper, contact_object_choice, *EMERGENCYCONTACTOBJECTS)
        self.error_label.pack()
        self.contactDropdownLabel.pack(padx=2.5, pady=2.5)
        self.contactObjectDropdown.pack(padx=2.5, pady=2.5)
        self.confirmContactObjectBTN = Button(self.middle_wrapper, text="Confirm Emergency Contact Business Object Choice", fg="white", bg="#990000", command=lambda: check_emergency_contact_columns(object, self, contact_object_choice))
        self.confirmContactObjectBTN.pack(padx=2.5, pady=2.5)

def check_emergency_contact_columns(object, self, contact_object_choice):
    if contact_object_choice.get() == "Emergency Contact Street Address":
        if 'AddressLine3' in object.data.columns:
            set_emergency_contact_object(object, contact_object_choice.get(), self)
        else:
            setattr(object, "prior_error", True)
            UI.clear_middle_frame(self)
            display_emergency_contact_dropdown(object, self)
    elif contact_object_choice.get() == "Emergency Contact Email Address":
        if 'EmailType' in object.data.columns:
            set_emergency_contact_object(object, contact_object_choice.get(), self)
        else:
            setattr(object, "prior_error", True)
            UI.clear_middle_frame(self)
            display_emergency_contact_dropdown(object, self)
    elif contact_object_choice.get() == "Emergency Contact Phone Number":
        if 'PhoneType' in object.data.columns:
            set_emergency_contact_object(object, contact_object_choice.get(), self)
        else:
            setattr(object, "prior_error", True)
            UI.clear_middle_frame(self)
            display_emergency_contact_dropdown(object, self)
    elif contact_object_choice.get() == "Emergency Contact Name":
        if 'Gender' in object.data.columns:
            set_emergency_contact_object(object, contact_object_choice.get(), self)
        else:
            setattr(object, "prior_error", True)
            UI.clear_middle_frame(self)
            display_emergency_contact_dropdown(object, self)
    else:
        setattr(object, "prior_error", True)
        UI.clear_middle_frame(self)
        display_emergency_contact_dropdown(object, self)

def set_emergency_contact_object(object, contact_object_choice, self): #Function that checks if user selected an emergency contact business object, sets the emergency contact business object choice, and routes to create_columns for emergency contacts
        setattr(object, "object_choice", contact_object_choice)
        create_emergency_contact_columns(object, self)

def create_emergency_contact_columns(object, self): #Function that creates the needed columns for each emergency contact business object
    if object.object_choice == "Emergency Contact Name":
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

def route_emergency_contact_configuration(object, self): #Function that either routes to corresponding configuration or to set_target_column if there is no configuration needed
    if object.object_choice == "Emergency Contact Street Address":
        setattr(object, "is_street_empty", False)
        SA.select_street_address(object, self)
    elif object.object_choice == "Emergency Contact Email Address":
        setattr(object, "domain", "")
        setattr(object, "is_domain_empty", False)
        EA.select_domain(object, self)
    else:
        BO.set_target_column(object, self)