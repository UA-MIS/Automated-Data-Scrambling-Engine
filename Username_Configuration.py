#=================================IMPORTS===================================#
from tkinter import *
import UI_Operations as UI
import Business_Object as BO

#=================================USERNAME CONFIGURATION===================================#
def select_username(object, self): #Function that prompts user to enter a username for generated usernames
    if object.is_username_empty == False:
        UI.clear_middle_frame(self)
        username_choice = StringVar()
        self.username_entry_label = Label(self.middle_wrapper, text = "Please enter the text you want to add for generated data:")
        self.example_wrapper = Frame(self.middle_wrapper)
        example = object.data.at[0, 'Username']
        self.example_label = Label(self.example_wrapper, text="Example: " + example.split("@")[0] + "_")
        self.username_entry = Entry(self.example_wrapper, textvariable = username_choice)
        self.example_label_2 = Label(self.example_wrapper, text="@" + example.split("@")[1])
        self.confirm_username_btn = Button(self.middle_wrapper, text="Confirm Username", fg="white", bg="#990000", command=lambda: set_username(object, username_choice, self))
        self.username_entry_label.pack(padx=2.5, pady=2.5)
        self.example_wrapper.pack(padx=2.5, pady=2.5)
        self.example_label.pack(side="left", padx=2.5, pady=2.5)
        self.username_entry.pack(side="left", padx=2.5, pady=2.5)
        self.example_label_2.pack(side="left", padx=2.5, pady=2.5)
        self.confirm_username_btn.pack(padx=2.5, pady=2.5)
    else:
        UI.clear_middle_frame(self)
        self.empty_username_label = Label(self.middle_wrapper, text = "The text is empty.", fg = "red")
        self.empty_username_label.pack(padx=2.5, pady=2.5)
        username_choice = StringVar()
        self.username_entry_label = Label(self.middle_wrapper, text = "Please enter the text you want to add for generated data:")
        self.example_wrapper = Frame(self.middle_wrapper)
        example = object.data.at[0, 'Username']
        self.example_label = Label(self.example_wrapper, text="Example: " + example.split("@")[0] + "_")
        self.username_entry = Entry(self.example_wrapper, textvariable = username_choice)
        self.example_label_2 = Label(self.example_wrapper, text="@" + example.split("@")[1])
        self.confirm_username_btn = Button(self.middle_wrapper, text="Confirm Username", fg="white", bg="#990000", command=lambda: set_username(object, username_choice, self))
        self.username_entry_label.pack(padx=2.5, pady=2.5)
        self.example_wrapper.pack(padx=2.5, pady=2.5)
        self.example_label.pack(side="left", padx=2.5, pady=2.5)
        self.username_entry.pack(side="left", padx=2.5, pady=2.5)
        self.example_label_2.pack(side="left", padx=2.5, pady=2.5)
        self.confirm_username_btn.pack(padx=2.5, pady=2.5)

def set_username(object, username_choice, self): #Function that checks if username entry is empty
    if username_choice.get() == "":
        object.is_username_empty = True
        select_username(object, self) #Routes back to select username if empty
    else:
        setattr(object, "username", username_choice.get())
        confirm_username(object, self) #Routes to confirm_username if not empty

def confirm_username(object, self): #Function that prompts user to confirm or redo their username choice
    UI.clear_middle_frame(self)
    self.username_label = Label(self.middle_wrapper, text = f"You entered '{object.username}' as the text to add to the username. Please confirm choice or go back.", padx=10, pady=2.5,)
    self.confirm_username_choice_button = Button(self.middle_wrapper, text="Confirm Username", fg="white", bg="#990000", command=lambda: BO.set_target_column(object, self))
    self.redo_username_button = Button(self.middle_wrapper, text="Edit Username", fg="white", bg="#990000", command=lambda: redo_username(object, self))
    self.username_label.pack(padx=2.5, pady=2.5)
    self.confirm_username_choice_button.pack(padx=2.5, pady=2.5)
    self.redo_username_button.pack(padx=2.5, pady=2.5)

def redo_username(object, self): #Function that deletes username choice and routes user to redo username choice
    delattr(object, "username")
    select_username(object, self)