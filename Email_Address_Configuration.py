#=================================IMPORTS===================================#
from tkinter import *
import UI_Operations as UI
import Business_Object as BO

#=================================EMAIL ADDRESS CONFIGURATION===================================#
def select_domain(object, self): #Function that prompts user to enter a domain for generated email addresses
    if object.is_domain_empty == False:
        UI.clear_middle_frame(self)
        domain_choice = StringVar()
        self.domain_entry_label = Label(self.middle_wrapper, text = "Please enter the domain you want to use for generated data:")
        self.example_wrapper = Frame(self.middle_wrapper)
        example = object.data.at[0, 'EmailAddress']
        self.example_label = Label(self.example_wrapper, text = 'Example: ' + example.split("@")[0] + '@')
        self.domain_entry = Entry(self.example_wrapper, textvariable = domain_choice)
        self.confirm_domain_btn = Button(self.middle_wrapper, text="Confirm Domain Name", fg="white", bg="#990000", command=lambda: set_domain(object, domain_choice, self))
        self.domain_entry_label.pack(padx=2.5, pady=2.5)
        self.example_wrapper.pack(padx=2.5, pady=2.5)
        self.example_label.pack(side="left", padx=2.5, pady=2.5)
        self.domain_entry.pack(side="left", padx=2.5, pady=2.5)
        self.confirm_domain_btn.pack(padx=2.5, pady=2.5)
    else:
        UI.clear_middle_frame(self)
        self.empty_domain_label = Label(self.middle_wrapper, text = "The domain is empty. Please enter a domain.", fg = "red")
        self.empty_domain_label.pack(padx=2.5, pady=2.5)
        domain_choice = StringVar()
        self.domain_entry_label = Label(self.middle_wrapper, text = "Please enter the domain you want to use for generated data:")
        self.example_wrapper = Frame(self.middle_wrapper)
        example = object.data.at[1, 'EmailAddress']
        self.example_label = Label(self.example_wrapper, text = 'Example: ' + example.split("@")[0] + '@')
        self.domain_entry = Entry(self.example_wrapper, textvariable = domain_choice)
        self.confirm_domain_btn = Button(self.middle_wrapper, text="Confirm Domain Name", fg="white", bg="#990000", command=lambda: set_domain(object, domain_choice, self))
        self.domain_entry_label.pack(padx=2.5, pady=2.5)
        self.example_wrapper.pack(padx=2.5, pady=2.5)
        self.example_label.pack(side="left", padx=2.5, pady=2.5)
        self.domain_entry.pack(side="left", padx=2.5, pady=2.5)
        self.confirm_domain_btn.pack(padx=2.5, pady=2.5)
    
def set_domain(object, domain_choice, self): #Function that checks to make sure domain isnt empty
    if domain_choice.get() == "": #If empty, redo domain entry with error message
        object.is_domain_empty = True
        select_domain(object, self)
    else: #If not, set the domain attribute to whatever they entered
        setattr(object, "domain", domain_choice.get())
        confirm_domain(object, self)

def confirm_domain(object, self): #Function that asks user if they want to confirm the domain they entered, or go back and re-enter
    UI.clear_middle_frame(self)
    self.domain_label = Label(self.middle_wrapper, text = f"You entered '{object.domain}' as the domain. Please confirm choice or go back.")
    self.confirm_domain_choice_button = Button(self.middle_wrapper, text="Confirm Domain Name", fg="white", bg="#990000", command=lambda: BO.set_target_column(object, self))
    self.redo_domain_button = Button(self.middle_wrapper, text="Edit Domain Name", fg="white", bg="#990000", command=lambda: redo_domain(object, self))
    self.domain_label.pack(padx=2.5, pady=2.5)
    self.confirm_domain_choice_button.pack(padx=2.5, pady=2.5)
    self.redo_domain_button.pack(padx=2.5, pady=2.5)

def redo_domain(object, self): #Function that deletes domain attribute and routes to select_domain
    delattr(object, "domain")
    object.is_domain_empty = False
    select_domain(object, self)