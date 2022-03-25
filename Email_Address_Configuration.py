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
        self.domain_entry = Entry(self.middle_wrapper, textvariable = domain_choice)
        self.confirm_domain_btn = Button(self.middle_wrapper, text="Confirm Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_domain(object, domain_choice, self))
        self.domain_entry_label.pack()
        self.domain_entry.pack()
        self.confirm_domain_btn.pack()
    else:
        UI.clear_middle_frame(self)
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
    UI.clear_middle_frame(self)
    self.domain_label = Label(self.middle_wrapper, text = f"You entered '{object.domain}' as the domain. Please confirm choice or go back.", padx=10, pady=5,)
    self.confirm_domain_choice_button = Button(self.middle_wrapper, text="Confirm Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: BO.set_target_column(object, self))
    self.redo_domain_button = Button(self.middle_wrapper, text="Edit Domain Name", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: redo_domain(object, self))
    self.domain_label.pack()
    self.confirm_domain_choice_button.pack()
    self.redo_domain_button.pack()

def redo_domain(object, self):
    delattr(object, "domain")
    select_domain(object, self)