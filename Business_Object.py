#=================================IMPORTS===================================#
import UI_Operations as UI
import Emergency_Contact_Configuration as EC
import Street_Address_Configuration as SA
import Email_Address_Configuration as EA
import Username_Configuration as UN
import Engine_Functions as EF
#=================================BUSINESS OBJECT===================================#

BUSINESSOBJECTS = ["Street Address", "Email Address", "Phone Number", "National Identifier", "Name", "Salary", "Username", "Emergency Contact"]

class BusinessObject: #Business Object class that is used throughout the application
    def __init__(self, data, prior_error, is_generated):
        self.data = data
        self.prior_error = prior_error
        self.is_generated = is_generated
    def new_attribute(self, attr): #Method to set attributes for business object
        setattr(self, attr, attr)

def set_object(object, object_choice, self): #Function that checks if user selected a business object, sets the business object choice, routes emergency contact objects to emergency contact dropdown, and routes all other objects to create_columns Function
    if object_choice.get() == "--Business Object--":
        setattr(object, "prior_error", True)
        UI.clear_middle_frame(self)
        UI.display_dropdown(object, self)
    else:
        setattr(object, "object_choice", object_choice.get())
        setattr(object, "prior_error", False)
        if object.object_choice == "Emergency Contact":
            EC.display_emergency_contact_dropdown(object, self)
        else:
            create_columns(object, self)

def create_columns(object, self): #Function that creates the needed columns for each non-emergency contact business object
    if object.object_choice == "Street Address":
        object.data["AddressLine1"] = ""
        object.data["AddressLine2"] = ""
        object.data["METADATA"] = "MERGE"
        object.data["PersonAddress"] = "PersonAddress"
    elif object.object_choice == "Phone Number":
        object.data["PhoneNumber"] = ""
        object.data["METADATA"] = "MERGE"
        object.data["PersonPhone"] = "PersonPhone"
    elif object.object_choice == "National Identifier":
        object.data["NationalIdentifierNumber"] = ""
        object.data["METADATA"] = "MERGE"
        object.data["NationalIdentifier"] = "NationalIdentifier"
    elif object.object_choice == "Email Address":
        object.data["METADATA"] = "MERGE"
        object.data["PersonEmail"] = "PersonEmail"
    elif object.object_choice == "Name":
        object.data["METADATA"] = "MERGE"
        object.data["PersonName"] = "PersonName"
        object.data["FirstName"] = ""
        object.data["LastName"] = ""
    elif object.object_choice == "Salary":
        object.data["METADATA"] = "MERGE"
        object.data["Salary"] = "Salary"
        object.data["SalaryAmount"] = ""
    elif object.object_choice == "Username":
        object.data["METADATA"] = "MERGE"
        object.data["User"] = "User"
    route_configuration(object, self)

def route_configuration(object, self): #Function that either routes to corresponding configuration or to set_target_column if there is no configuration needed
    if object.object_choice == "Street Address":
        setattr(object, "street", "")
        setattr(object, "is_street_empty", False)
        SA.select_street_address(object, self) #Routes street address business object to street address configuration
    elif object.object_choice == "Email Address":
        setattr(object, "domain", "")
        setattr(object, "is_domain_empty", False)
        EA.select_domain(object, self) #Routes email address business object to email address configuration
    elif object.object_choice == "Username":
        setattr(object, "username", "")
        setattr(object, "is_username_empty", False) #Routes username business object to username configuration
        UN.select_username(object, self)
    else:
        set_target_column(object, self)

def set_target_column(object, self): #Function that sets the target column(s) for each business object
    UI.clear_middle_frame(self)
    if object.object_choice == "Street Address":
        setattr(object, "target_column_1", "AddressLine1")
        setattr(object, "target_column_2", "AddressLine2")
    elif object.object_choice == "Phone Number":
        setattr(object, "target_column", "PhoneNumber")
    elif object.object_choice == "National Identifier":
        setattr(object, "target_column", "NationalIdentifierNumber")
    elif object.object_choice == "Email Address":
        setattr(object, "target_column", "EmailAddress")
    elif object.object_choice == "Name":
        setattr(object, "target_firstname_column", "FirstName")
        setattr(object, "target_lastname_column", "LastName")
    elif object.object_choice == "Salary":
        setattr(object, "target_column", "SalaryAmount")
    elif object.object_choice == "Username":
        setattr(object, "target_username_column", "Username")
    elif object.object_choice == "Emergency Contact Name":
        setattr(object, "target_contact_firstname_column", "FirstName")
        setattr(object, "target_contact_lastname_column", "LastName")
    elif object.object_choice == "Emergency Contact Street Address":
        setattr(object, "target_contact_column_1", "AddressLine1")
        setattr(object, "target_contact_column_2", "AddressLine2")
    elif object.object_choice == "Emergency Contact Phone Number":
        setattr(object, "target_contact_phone_column", "PhoneNumber")
    elif object.object_choice == "Emergency Contact Email Address":
        setattr(object, "target_column", "EmailAddress")
    EF.generate_data(object, self)