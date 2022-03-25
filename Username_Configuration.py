#=================================IMPORTS===================================#
from tkinter import *
import UI_Operations as UI
import Business_Object as BO

#=================================USERNAME CONFIGURATION===================================#
def select_username(object, self): #Function that prompts user to enter a username generated usernames
    if object.is_username_empty == False:
        UI.clear_middle_frame(self)
        username_choice = StringVar()
        self.username_entry_label = Label(self.middle_wrapper, text = "Please enter the username you want to use for generated data:")
        self.username_entry = Entry(self.middle_wrapper, textvariable = username_choice)
        self.confirm_username_btn = Button(self.middle_wrapper, text="Confirm Username", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: set_username(object, username_choice, self))
        self.username_entry_label.pack()
        self.username_entry.pack()
        self.confirm_username_btn.pack()
    else:
        UI.clear_middle_frame(self)
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
        confirm_username(object, self)

def confirm_username(object, self):
    UI.clear_middle_frame(self)
    self.username_label = Label(self.middle_wrapper, text = f"You entered '{object.username}' as the text to add to the username. Please confirm choice or go back.", padx=10, pady=5,)
    self.confirm_username_choice_button = Button(self.middle_wrapper, text="Confirm Username", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: BO.set_target_column(object, self))
    self.redo_username_button = Button(self.middle_wrapper, text="Edit Username", padx=10, pady=5, fg="white", bg="dark blue", command=lambda: redo_username(object, self))
    self.username_label.pack()
    self.confirm_username_choice_button.pack()
    self.redo_username_button.pack()

def redo_username(object, self):
    delattr(object, "username")
    select_username(object, self)