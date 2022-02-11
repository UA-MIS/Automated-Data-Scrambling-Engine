# this file will generate random addresses for the client
from faker import Faker
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import numpy as np

faker = Faker()

def generate_addresses(data):
    for i in range(len(data.index)):
        print(faker.street_address())

def generate_address():
    for i in range(200):
        print(faker.street_address())

generate_address()