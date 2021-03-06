#=================================IMPORTS===================================#
from tkinter import *
import tkinter as tk
import UI_Operations as UI
import Business_Object as BO

#=================================STREET ADDRESS CONFIGURATION===================================#
def select_street_address(object, self): #Function that prompts user to enter a street name for generated street addresses
    if object.is_street_empty == False:
        UI.clear_middle_frame(self)
        street_choice = StringVar()
        self.entry_label_street = Label(self.middle_wrapper, text="Please enter the street address you want to use for generated data:")
        self.street_entry = Entry(self.middle_wrapper, textvariable=street_choice)
        self.confirm_street_btn = tk.Button(self.middle_wrapper, text="Confirm Street Name", fg="white", bg="#990000",
                                    command=lambda: set_street_address(object, street_choice, self))
        self.entry_label_street.pack(padx=2.5, pady=2.5)
        self.street_entry.pack(padx=2.5, pady=2.5)
        self.confirm_street_btn.pack(padx=2.5, pady=2.5)
    else:
        UI.clear_middle_frame(self)
        self.empty_street_label = Label(self.middle_wrapper, text = "The street name is empty. Please enter a street name.", fg = "red")
        self.empty_street_label.pack(padx=2.5, pady=2.5)
        street_choice = StringVar()
        self.entry_label_street = Label(self.middle_wrapper, text="Please enter the street address you want to use for generated data:")
        self.street_entry = Entry(self.middle_wrapper, textvariable=street_choice)
        self.confirm_street_btn = tk.Button(self.middle_wrapper, text="Confirm Street Name", fg="white", bg="#990000",
                                    command=lambda: set_street_address(object, street_choice, self))
        self.entry_label_street.pack(padx=2.5, pady=2.5)
        self.street_entry.pack(padx=2.5, pady=2.5)
        self.confirm_street_btn.pack(padx=2.5, pady=2.5)

def set_street_address(object, street_choice, self): #Function that checks if street choice is empty
    if street_choice.get() == "":
        object.is_street_empty = True
        select_street_address(object, self) #Routes back to street selection if empty
    else:
        setattr(object, "street", street_choice.get())
        setattr(object, "frequency_error", False)
        confirm_street(object, self) #Routes to confirm street if not empty

def confirm_street(object, self): #Function that prompts user to confirm or redo street choice
    UI.clear_middle_frame(self)
    self.street_label = Label(self.middle_wrapper, text = f"You entered '{object.street}' as the street name. Please confirm choice or go back.")
    self.confirm_street_choice_button = Button(self.middle_wrapper, text="Confirm Street Name", fg="white", bg="#990000", command=lambda: select_frequency(object, self))
    self.redo_street_button = Button(self.middle_wrapper, text="Edit Street Name", fg="white", bg="#990000", command=lambda: redo_street(object, self))
    self.street_label.pack(padx=2.5, pady=2.5)
    self.confirm_street_choice_button.pack(padx=2.5, pady=2.5)
    self.redo_street_button.pack(padx=2.5, pady=2.5)

def redo_street(object, self): #Function that deletes users street choice and routes them to redo street choice
    delattr(object, "street")
    object.is_street_empty = False
    select_street_address(object, self)

def select_frequency(object, self):  #Function that displays the dropdown to choose the street line 2 frequency
    if object.frequency_error == False:
        UI.clear_middle_frame(self)
        FREQUENCY_OPTIONS = ["1/10", "1/20", "1/50", "1/100"]
        frequency_choice = tk.StringVar()
        frequency_choice.set("--Street Address Line 2 Frequency--")
        self.frequency_label = tk.Label(self.middle_wrapper, text="Select how frequent you want to generate address line 2:")
        self.frequency_dropdown = tk.OptionMenu(self.middle_wrapper, frequency_choice, *FREQUENCY_OPTIONS)
        self.frequency_label.pack(padx=2.5, pady=2.5)
        self.frequency_dropdown.pack(padx=2.5, pady=2.5)
        self.confirm_street_btn = tk.Button(self.middle_wrapper, text="Confirm Street Line 2 Frequency Choice", fg="white",
                                    bg="#990000", command=lambda: set_frequency(object, frequency_choice, self))
        self.confirm_street_btn.pack(expand="true", padx=2.5, pady=2.5)
    else:
        UI.clear_middle_frame(self)
        FREQUENCY_OPTIONS = ["1/10", "1/20", "1/50", "1/100"]
        frequency_choice = tk.StringVar()
        frequency_choice.set("--Street Address Line 2 Frequency--")
        self.frequency_error_label = Label(self.middle_wrapper, text = "No frequency selected. Please select a frequency.", fg = "red")
        self.frequency_error_label.pack(padx=2.5, pady=2.5)
        self.frequency_label = tk.Label(self.middle_wrapper, text="Select the frequency of which you want :")
        self.frequency_dropdown = tk.OptionMenu(self.middle_wrapper, frequency_choice, *FREQUENCY_OPTIONS)
        self.frequency_label.pack(padx=2.5, pady=2.5)
        self.frequency_dropdown.pack(padx=2.5, pady=2.5)
        self.confirm_street_btn = tk.Button(self.middle_wrapper, text="Confirm Street Line 2 Frequency Choice", fg="white",
                                    bg="#990000", command=lambda: set_frequency(object, frequency_choice, self))
        self.confirm_street_btn.pack(expand="true", padx=2.5, pady=2.5)

def set_frequency(object, frequency_choice, self): #Function that checks if frequency is empty
    if frequency_choice.get() == "--Street Address Line 2 Frequency--":
        object.frequency_error = True
        select_frequency(object, self) #Routes back to select frequency if empty
    else:
        setattr(object, "frequency", frequency_choice.get())
        confirm_frequency(object, self) #Routes to confirm frequency if not empty

def confirm_frequency(object, self): #Function that prompts user to confirm or redo frequency choice
    UI.clear_middle_frame(self)
    self.frequency_label = Label(self.middle_wrapper, text = f"You selected '{object.frequency}' as the frequency. Please confirm choice or go back.")
    self.confirm_frequency_choice_button = Button(self.middle_wrapper, text="Confirm Frequency", fg="white", bg="#990000", command=lambda: BO.set_target_column(object, self))
    self.redo_frequency_button = Button(self.middle_wrapper, text="Change Frequency", fg="white", bg="#990000", command=lambda: redo_frequency(object, self))
    self.frequency_label.pack(padx=2.5, pady=2.5)
    self.confirm_frequency_choice_button.pack(padx=2.5, pady=2.5)
    self.redo_frequency_button.pack(padx=2.5, pady=2.5)

def redo_frequency(object, self): #Function that deletes frequency choice and routes to redo frequency choice
    delattr(object, "frequency")
    object.frequency_error = False
    select_frequency(object, self)