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
        self.contactDropdownLabel.pack()
        self.contactObjectDropdown.pack()
        self.confirmContactObjectBTN = Button(self.middle_wrapper, text="Confirm Emergency Contact Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_emergency_contact_object(object, self, contact_object_choice))
        self.confirmContactObjectBTN.pack()
    else:
        UI.clear_middle_frame(self)
        EMERGENCYCONTACTOBJECTS = ["Emergency Contact Name", "Emergency Contact Phone Number", "Emergency Contact Street Address", "Emergency Contact Email Address"]
        contact_object_choice = StringVar()
        contact_object_choice.set("--Emergency Contact Business Object--")
        self.error_label = Label(self.middle_wrapper, text="You did not select a business object. Please select one from the dropdown below.", fg="red")
        self.contactDropdownLabel = Label(self.middle_wrapper, text="Select the Emergency Contact Business Object that corresponds with your file:")
        self.contactObjectDropdown = OptionMenu(self.middle_wrapper, contact_object_choice, *EMERGENCYCONTACTOBJECTS)
        self.error_label.pack()
        self.contactDropdownLabel.pack()
        self.contactObjectDropdown.pack()
        self.confirmContactObjectBTN = Button(self.middle_wrapper, text="Confirm Emergency Contact Business Object Choice", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_emergency_contact_object(object, self, contact_object_choice))
        self.confirmContactObjectBTN.pack()

def set_emergency_contact_object(object, self, contact_object_choice):
    if contact_object_choice.get() == "--Emergency Contact Business Object--":
        setattr(object, "prior_error", True)
        UI.clear_middle_frame(self)
        display_emergency_contact_dropdown(object, self)
    else:
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
        SA.select_street_address(object, self)
    elif object.object_choice == "Emergency Contact Email Address":
        setattr(object, "domain", "")
        setattr(object, "is_domain_empty", False)
        EA.select_domain(object, self)
    else:
        BO.set_target_column(object, self)