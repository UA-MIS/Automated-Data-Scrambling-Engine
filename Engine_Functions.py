#=================================IMPORTS===================================#
from tkinter import *
import tkinter.ttk as ttk
from tkinter.ttk import Progressbar
import faker as faker
import random
import UI_Operations as UI
import File_Operations as FO
import names

#=================================INITIALIZE FAKER===================================#
fake = faker.Faker()

#=================================ENGINE FUNCTIONS===================================#        
def generate_data(object, self): #Function that reads business object choice and directs data to corresponding generate function, creates export button, reorders columns, and displays new data
    if object.object_choice == "Phone Number":
        generate_phone_number(object, self)
    elif object.object_choice == "Email Address":
        generate_email_address(object, self)
    elif object.object_choice == "Street Address":
        generate_street_address(object, self)
    elif object.object_choice == "National Identifier":
        generate_national_identifier(object, self)
    elif object.object_choice == "Name":
        generate_name(object, self)
    elif object.object_choice == "Salary":
        generate_salary(object, self)
    elif object.object_choice == "Username":
        generate_username(object, self)
    elif object.object_choice == "Emergency Contact Name":
        generate_contact_name(object, self)
    elif object.object_choice == "Emergency Contact Phone Number":
        generate_contact_phone_number(object, self)
    elif object.object_choice == "Emergency Contact Street Address":
        generate_contact_street_address(object, self)
    elif object.object_choice == "Emergency Contact Email Address":
        generate_email_address(object, self)
    self.export_btn = Button(self.bottom_wrapper, text = "Export Data", fg="white", bg="#990000", command=lambda: FO.export_data(object, self))
    self.export_btn.pack(padx=2.5, pady=2.5)
    object.is_generated = True
    FO.reorder_columns(object)
    self.top_label["text"] = "Data has been updated and columns have been reordered. You can export by clicking the 'Export Data' button below."
    UI.display_data(object, self)

def generate_email_address(object, self): #Function that creates email addresses with users domain choice
    self.loading_label = Label(self.top_wrapper, text="Creating Email Addresses...", font=self.small_font)
    self.loading_label.pack()
    self.loading_label.update()
    object.data[object.target_column] = object.data[object.target_column].apply(lambda x: x.split("@")[0] + "@" + object.domain)
    self.loading_label.destroy()

def generate_name(object, self): #Function that generates names based on gender, includes loading bar
    self.loading_label = Label(self.top_wrapper, text="Generating Names...")
    self.loading_label.pack()
    self.progress = Progressbar(self.top_wrapper, orient = HORIZONTAL, length = 100, maximum = 100, style = 'red.Horizontal.TProgressbar', mode = 'determinate')
    self.progress.pack()
    step = round(len(object.data.index)/100)
    for i in object.data.index:
        if object.data.at[i, "Gender"] == "M":
            first = random.choice(names.male_first_names)
            last = random.choice(names.last_names)
            object.data.at[i, object.target_firstname_column] = first
            object.data.at[i, object.target_lastname_column] = last
        elif object.data.at[i, "Gender"] == "F":
            first = random.choice(names.female_first_names)
            last = random.choice(names.last_names)
            object.data.at[i, object.target_firstname_column] = first
            object.data.at[i, object.target_lastname_column] = last
        else:
            x = random.choice([1, 2])
            if x == 1:
                first = random.choice(names.male_first_names)
            else:
                first = random.choice(names.female_first_names)
            last = random.choice(names.last_names)
            object.data.at[i, object.target_firstname_column] = first
            object.data.at[i, object.target_lastname_column] = last    
        if i % step == 0:
            self.progress["value"] += 1
            self.progress.update()
    self.progress.destroy()
    self.loading_label.destroy()

def generate_username(object, self): #Function that creates usernames with users username choice
    self.loading_label = Label(self.top_wrapper, text="Creating Usernames...", font=self.small_font)
    self.loading_label.pack()
    self.loading_label.update()
    object.data[object.target_username_column] = object.data[object.target_username_column].apply(lambda x: x.split("@")[0] + "_" + object.username + "@test.com")
    self.loading_label.destroy()
    

def generate_salary(object, self): #Function that generates salaries based on salary type
    self.loading_label = Label(self.top_wrapper, text="Generating Salaries...", font=self.small_font)
    self.loading_label.pack()
    self.loading_label.update()
    for i in object.data.index:
        if object.data.at[i, 'SalaryBasisName'] == 'Annual Salary':
            object.data.at[i, object.target_column] = return_annual_salary()
        else:
            object.data.at[i, object.target_column] = return_hourly_salary()
    self.loading_label.destroy()

def generate_contact_name(object, self): #Function that generates names based on gender, includes loading bar
    self.loading_label = Label(self.top_wrapper, text="Generating Names...")
    self.loading_label.pack()
    self.progress = Progressbar(self.top_wrapper, orient = HORIZONTAL, length = 100, maximum = 100, style = 'red.Horizontal.TProgressbar', mode = 'determinate')
    self.progress.pack()
    step = round(len(object.data.index)/100)
    for i in object.data.index:
        if object.data.at[i, "Gender"] == "M":
            first = random.choice(names.male_first_names)
            last = random.choice(names.last_names)
            object.data.at[i, object.target_contact_firstname_column] = first
            object.data.at[i, object.target_contact_lastname_column] = last
        elif object.data.at[i, "Gender"] == "F":
            first = random.choice(names.female_first_names)
            last = random.choice(names.last_names)
            object.data.at[i, object.target_contact_firstname_column] = first
            object.data.at[i, object.target_contact_lastname_column] = last
        else:
            x = random.choice([1, 2])
            if x == 1:
                first = random.choice(names.male_first_names)
            else:
                first = random.choice(names.female_first_names)
            last = random.choice(names.last_names)
            object.data.at[i, object.target_contact_firstname_column] = first
            object.data.at[i, object.target_contact_lastname_column] = last    
        if i % step == 0:
            self.progress["value"] += 1
        self.progress.update()
    self.progress.destroy()
    self.loading_label.destroy()

def generate_contact_phone_number(object, self): #Function that generates phone numbers for emergency contact
    self.loading_label = Label(self.top_wrapper, text="Generating Phone Numbers...")
    self.loading_label.pack()
    self.progress = Progressbar(self.top_wrapper, orient = HORIZONTAL, length = 100, maximum = 100, style = 'red.Horizontal.TProgressbar', mode = 'determinate')
    self.progress.pack()
    step = round(len(object.data.index)/100)
    for i in object.data.index:
        if i % 1 == 0:
            object.data.at[i, object.target_contact_phone_column] = return_phone_normal_format() #normal format
        if i % 3 == 1:
            object.data.at[i, object.target_contact_phone_column] = return_phone_format_2() #different format
        if i % 5 == 1:
            object.data.at[i, object.target_contact_phone_column] = return_phone_format_3() #different format
        if i % step == 0:
            self.progress["value"] += 1
            self.progress.update()
    self.progress.destroy()
    self.loading_label.destroy()

def generate_contact_street_address(object, self): #Function that generates street addresses for emergency contact using users street choice and frequency choice
    self.loading_label = Label(self.top_wrapper, text="Generating Street Addresses...")
    self.loading_label.pack()
    self.progress = Progressbar(self.top_wrapper, orient = HORIZONTAL, length = 100, maximum = 100, style = 'red.Horizontal.TProgressbar', mode = 'determinate')
    self.progress.pack()
    step = round(len(object.data.index)/100)
    for i in object.data.index:
        object.data.at[i, object.target_contact_column_1] = return_streetaddress(object.street, i)
        if object.frequency == "1/10":
            frequency = 10
            if i % frequency == 0:
                object.data.at[i, object.target_contact_column_2] = return_streetaddress_line2(i)
        elif object.frequency == "1/20":
            frequency = 20
            if i % frequency == 0:
                object.data.at[i, object.target_contact_column_2] = return_streetaddress_line2(i)
        elif object.frequency == "1/50":
            frequency = 50
            if i % frequency == 0:
                object.data.at[i, object.target_contact_column_2] = return_streetaddress_line2(i)
        else:
            frequency = 100
            if i % frequency == 0:
                object.data.at[i, object.target_contact_column_2] = return_streetaddress_line2(i)
        if i % step == 0:
            self.progress["value"] += 1
            self.progress.update()
    self.progress.destroy()
    self.loading_label.destroy()

def return_streetaddress(street_choice, i): #Function that returns street addresses based on users choice
    x = str(i + 110)
    return x + " " + street_choice

def return_streetaddress_line2(i): #Function that returns street address line 2's
    x = str(i + 11)
    return "Unit " + x

def return_annual_salary(): #Function that returns an annual salary
    x = random.randrange(65000, 200000)
    return x

def return_hourly_salary(): #Function that returns an hourly salary
    x = random.randrange(10, 40)
    return x
   
def generate_street_address(object, self):  #Function that generates street addresses using users street choice and frequency choice
    self.loading_label = Label(self.top_wrapper, text="Generating Street Addresses...")
    self.loading_label.pack()
    self.progress = Progressbar(self.top_wrapper, orient = HORIZONTAL, length = 100, maximum = 100, style = 'red.Horizontal.TProgressbar', mode = 'determinate')
    self.progress.pack()
    step = round(len(object.data.index)/100)
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
        if i % step == 0:
            self.progress["value"] += 1
            self.progress.update()
    self.progress.destroy()
    self.loading_label.destroy()

def generate_phone_number(object, self): #Function that generates phone numbers with different formats
    self.loading_label = Label(self.top_wrapper, text="Generating Phone Numbers...")
    self.loading_label.pack()
    self.progress = Progressbar(self.top_wrapper, orient = HORIZONTAL, length = 100, maximum = 100, style = 'red.Horizontal.TProgressbar', mode = 'determinate')
    self.progress.pack()
    step = round(len(object.data.index)/100)
    for i in object.data.index:
        if i % 1 == 0:
            object.data.at[i, object.target_column] = return_phone_normal_format()
        if i % 3 == 1:
            object.data.at[i, object.target_column] = return_phone_format_2()
        if i % 5 == 1:
            object.data.at[i, object.target_column] = return_phone_format_3()
        if i % step == 0:
            self.progress["value"] += 1
            self.progress.update()
            print(self.progress["value"])
    self.progress.destroy()
    self.loading_label.destroy()
   
def generate_national_identifier(object, self): #Function that generates national identifiers
    self.loading_label = Label(self.top_wrapper, text="Generating Phone Numbers...")
    self.loading_label.pack()
    self.progress = Progressbar(self.top_wrapper, orient = HORIZONTAL, length = 100, maximum = 100, style = 'red.Horizontal.TProgressbar', mode = 'determinate')
    self.progress.pack()
    step = round(len(object.data.index)/100)
    for i in object.data.index:
        object.data.at[i, object.target_column] = return_SSN()
        if i % step == 0:
            self.progress["value"] += 1
            self.progress.update()
    self.progress.destroy()
    self.loading_label.destroy()

def return_SSN(): #Function that returns social security numbers
    return fake.ssn()

def return_phone_normal_format(): #Function that generates phone numbers in normal format
    return fake.numerify("(###)-###-####")

def return_phone_format_2(): #Function that generates phone numbers without parenthesis
    return fake.numerify("###-###-####")

def return_phone_format_3(): #Function that generates phone numbers without parenthesis and hyphens
    return fake.numerify("### ### ####")