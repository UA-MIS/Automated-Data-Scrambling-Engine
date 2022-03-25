#=================================IMPORTS===================================#
from tkinter import *
import faker as faker
import random
import UI_Operations as UI
import File_Operations as FO

#=================================INITIALIZE FAKER===================================#
fake = faker.Faker()

#=================================ENGINE FUNCTIONS===================================#        
def generate_data(object, self): #Function that reads business object choice and directs data to corresponding generate function
    self.top_label["text"] = "Data has been updated and columns have been reordered. You can export by clicking the 'Export Data' button below"
    self.export_btn = Button(self.bottom_wrapper, text = "Export Data", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: FO.export_data(object, self))
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
    elif object.object_choice == "Username":
        generate_username(object)
    elif object.object_choice == "Emergency Contact Name":
        generate_contact_name(object)
    elif object.object_choice == "Emergency Contact Phone Number":
        generate_contact_phone_number(object)
    elif object.object_choice == "Emergency Contact Street Address":
        generate_contact_street_address(object)
    elif object.object_choice == "Emergency Contact Email Address":
        generate_email_address(object)
    object.is_generated = True
    FO.reorder_columns(object)
    UI.display_data(object, self)

def generate_email_address(object):            #Function that generates email addresses
    object.data[object.target_column] = object.data[object.target_column].apply(lambda x: x.split("@")[0] + "@" + object.domain)

def generate_name(object): #function that calls the method generates within the target column
    for i in object.data.index:
        if object.data.at[i, "Gender"] == "M":
            x = return_male_name()
            first = x.split(" ")[0]
            last = x.split(" ")[1]
            object.data.at[i, object.target_firstname_column] = first
            object.data.at[i, object.target_lastname_column] = last
        elif object.data.at[i, "Gender"] == "F":
            x = return_female_name()
            first = x.split(" ")[0]
            last = x.split(" ")[1]
            object.data.at[i, object.target_firstname_column] = first
            object.data.at[i, object.target_lastname_column] = last
        else:
            x = return_undecided_name()
            first = x.split(" ")[0]
            last = x.split(" ")[1]
            object.data.at[i, object.target_firstname_column] = first
            object.data.at[i, object.target_lastname_column] = last

def return_male_name():
    return fake.name_male()

def return_female_name():
    return fake.name_female()

def return_undecided_name():
    return fake.name_nonbinary()

def generate_username(object):
    object.data[object.target_username_column] = object.data[object.target_username_column].apply(lambda x: x.split("@")[0] + "_" + object.username + "@test.com")

def generate_salary(object):
    for i in object.data.index:
        if object.data.at[i, 'SalaryBasisName'] == 'Annual Salary':
            object.data.at[i, object.target_column] = return_annual_salary()
        else:
            object.data.at[i, object.target_column] = return_hourly_salary()

def generate_contact_name(object): #function that calls the method generates within the target column
    for i in object.data.index:
        if object.data.at[i, "Gender"] == "M":
            x = return_male_name()
            first = x.split(" ")[0]
            last = x.split(" ")[1]
            object.data.at[i, object.target_contact_firstname_column] = first
            object.data.at[i, object.target_contact_lastname_column] = last
        elif object.data.at[i, "Gender"] == "F":
            x = return_female_name()
            first = x.split(" ")[0]
            last = x.split(" ")[1]
            object.data.at[i, object.target_contact_firstname_column] = first
            object.data.at[i, object.target_contact_lastname_column] = last
        else:
            x = return_undecided_name()
            first = x.split(" ")[0]
            last = x.split(" ")[1]
            object.data.at[i, object.target_contact_firstname_column] = first
            object.data.at[i, object.target_contact_lastname_column] = last

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