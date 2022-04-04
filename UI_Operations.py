#=================================IMPORTS===================================#
from tkinter import *
from tkinter import ttk
import numpy as np
import UI_Operations as UI
import File_Operations as FO
import Business_Object as BO

#=================================UI OPERATIONS===================================#
class Application(object): #Application class
    def __init__(self, event=None):
        self.root = Tk()
        self.title_font = ("Calibri", 20, "bold")
        self.large_font = ("Calibri", 15, "bold")
        self.small_font = ("Calibri", 10, "bold")
        self.s = ttk.Style()
        self.s.theme_use('clam')
        self.s.configure("red.Horizontal.TProgressbar", foreground='#990000', background='#990000')

        self.title_text = Label(self.root, text="Welcome to the Automated Data Scrambling Engine!", font=self.title_font) #Creates text that appears at top of application
        self.top_wrapper = LabelFrame(self.root, text="Preview")                                    #Creates preview Section
        self.middle_wrapper = LabelFrame(self.root, text="Configuration")                           #Creates configure Section
        self.bottom_wrapper = LabelFrame(self.root, text="Current File")                            #Creates select File section
        self.file_name_label = Label(self.bottom_wrapper, text="No file selected", name = "file_name_label")                    #Creates text for selected file name
        self.top_label = Label(self.top_wrapper, text="View preview of data here:", font=self.small_font)                  #Creates text for top label
        self.tv1 = ttk.Treeview(self.top_wrapper)                                                   #Creates treeview for previewing data
        self.delim_choice = StringVar()
        self.delim_entry_label = Label(self.bottom_wrapper, text = "Please enter the delimiter your file uses:")
        self.delim_entry = Entry(self.bottom_wrapper, textvariable = self.delim_choice)
        self.delim_confirm_btn = Button(self.bottom_wrapper, text="Confirm Delimiter", fg="white", bg="#990000", command = lambda: FO.add_file(self))
        self.treescrolly = Scrollbar(self.tv1, orient="vertical", command=self.tv1.yview)            #Updates the y-axis view of the widget
        self.treescrollx = Scrollbar(self.tv1, orient="horizontal", command=self.tv1.xview)          #Updates the x-axis view of the widget
        self.tv1.configure(xscrollcommand=self.treescrollx.set, yscrollcommand=self.treescrolly.set)    #Assigns the scrollbars to the Treeview
    
    

        self.title_text.pack(fill="x", padx=2.5, pady=2.5)      #Places title text widget in window
        self.top_wrapper.pack(fill="both", expand="yes", padx=20, pady=20)     #Places top_wrapper label frame in window
        self.middle_wrapper.pack(fill="x", expand="yes", padx=20, pady=20)  #Places middle_wrapper label frame in window
        self.bottom_wrapper.pack(fill="x", padx=20, pady=20)  #Places bottom_wrapper label frame in window
        self.file_name_label.pack(padx=2.5, pady=2.5)                                             #Places fileName Label in bottom_wrapper frame
        self.top_label.pack(padx=2.5, pady=2.5)                                                  #Places top label in top wrapper frame          
        self.tv1.pack(fill="both", expand="yes", padx=20, pady=20)            #Places treeview in top_wrapper frame
        self.treescrollx.pack(side="bottom", fill="x")                        #Makes the scrollbar fill the x axis of the Treeview widget
        self.treescrolly.pack(side="right", fill="y")                         #Makes the scrollbar fill the y axis of the Treeview widget
        self.delim_entry_label.pack(padx=2.5, pady=2.5)
        self.delim_entry.pack(padx=2.5, pady=2.5)
        self.delim_confirm_btn.pack(padx=2.5, pady=2.5)


        self.root.title("Automated Data Scrambling Engine")  #Sets window title to the name of our project
        self.root.geometry("800x700")                        #Sets window size to 800x700 pixels
        self.root.mainloop()                                 #Keeps window open and running

def restart_app(self): #Function that restarts application
    self.root.destroy()
    app = Application()

def clear_middle_frame(self): #Function that clears the middle frame
    for widget in self.middle_wrapper.winfo_children():
        widget.destroy()

def clear_bottom_frame(self): #Function that clears the bottom frame
    for widget in self.bottom_wrapper.winfo_children():
        widget.destroy()

def clear_bottom_frame_except_filenamelabel(self): #Function that clears the bottom frame except for file name label
    for widget in self.bottom_wrapper.winfo_children():
        if widget.widgetName != "label" or widget["text"] == "Please enter the delimiter your file uses:" or widget["text"] == "No delimiter chosen." or widget["text"] == "The file type you have chosen is not acceptable.":
            widget.destroy()

def display_data(object, self): #Function that displays csv data in the preview
    clear_data(self)
    object.columns = object.data.columns.values
    data_without_NaN = object.data.replace(np.nan, '', regex=True)
    self.tv1["columns"] = object.columns
    self.tv1["show"] = "headings"
    for column in self.tv1["columns"]:
        self.tv1.heading(column, text=column)
    df_rows = data_without_NaN.to_numpy().tolist()
    count = 0
    for row in df_rows:
        if count < 20:
            self.tv1.insert("", "end", values=row)
            count += 1
    if object.is_generated == False:
        display_dropdown(object, self)
    else:
        clear_middle_frame(self)

def clear_data(self): #Function that clears the preview so that it can be repopulated
    self.tv1.delete(*self.tv1.get_children())

def display_dropdown(object, self): #Function that displays the dropdown to choose the business object
    if object.prior_error == False:
        objectChoice = StringVar()
        objectChoice.set("--Business Object--")
        self.dropdownLabel = Label(self.middle_wrapper, text="Select the Business Object that corresponds with your file:")
        self.objectDropdown = OptionMenu(self.middle_wrapper, objectChoice, *BO.BUSINESSOBJECTS)
        self.dropdownLabel.pack(padx=2.5, pady=2.5)
        self.objectDropdown.pack(padx=2.5, pady=2.5)
        self.confirmObjectBTN = Button(self.middle_wrapper, text="Confirm Business Object Choice", fg="white", bg="#990000", command=lambda: BO.set_object(object, objectChoice, self))
        self.confirmObjectBTN.pack(padx=2.5, pady=2.5)
    else:
        objectChoice = StringVar()
        objectChoice.set("--Business Object--")
        self.error_label = Label(self.middle_wrapper, text="You did not select a business object. Please select one from the dropdown below.", fg="red")
        self.dropdownLabel = Label(self.middle_wrapper, text="Select the Business Object that corresponds with your file:")
        self.objectDropdown = OptionMenu(self.middle_wrapper, objectChoice, *BO.BUSINESSOBJECTS)
        self.error_label.pack(padx=2.5, pady=2.5)
        self.dropdownLabel.pack(padx=2.5, pady=2.5)
        self.objectDropdown.pack(padx=2.5, pady=2.5)
        self.confirmObjectBTN = Button(self.middle_wrapper, text="Confirm Business Object Choice", fg="white", bg="#990000", command=lambda: BO.set_object(object, objectChoice, self))
        self.confirmObjectBTN.pack(padx=2.5, pady=2.5)