#=================================IMPORTS===================================#
import UI_Operations as UI
import Emergency_Contact_Configuration as EC
import Street_Address_Configuration as SA
import Email_Address_Configuration as EA
import Username_Configuration as UN
import Engine_Functions as EF
#=================================BUSINESS OBJECT===================================#
class BusinessObject:
    def __init__(self, data, prior_error, is_generated):
        self.data = data
        self.prior_error = prior_error
        self.is_generated = is_generated
    def new_attribute(self, attr):
        setattr(self, attr, attr)

def set_object(object, object_choice, self):
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
        route_configuration(object, self)
    elif object.object_choice == "Name":
        print("here")
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
        SA.select_street_address(object, self)
    elif object.object_choice == "Email Address":
        setattr(object, "domain", "")
        setattr(object, "is_domain_empty", False)
        EA.select_domain(object, self)
    elif object.object_choice == "Username":
        setattr(object, "username", "")
        setattr(object, "is_username_empty", False)
        UN.select_username(object, self)
    else:
        set_target_column(object, self)

def set_target_column(object, self):
    UI.clear_middle_frame(self)
    if object.object_choice == "Street Address":
        setattr(object, "target_column_1", "AddressLine1")
        setattr(object, "target_column_2", "AddressLine2")
    elif object.object_choice == "Phone Number":
        setattr(object, "target_column", "PhoneNumber")
    elif object.object_choice == "National Identifier":
        setattr(object, "target_column", "NationalIdentifier")
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