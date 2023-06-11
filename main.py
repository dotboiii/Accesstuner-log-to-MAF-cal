import csv
import scan
import numpy as np 
import matplotlib.pyplot as plt 
import math
from scipy.optimize import curve_fit
import PySimpleGUI as sg
from scan import open_log_file, search_column, column_to_list
import data
import os
from Mafcal import Generate_Maf_cal

# Get the current directory of the Python program
current_directory = os.path.dirname(os.path.abspath(__file__))
# Construct the file path to the 'headers.file' relative to the current directory
headers_file_path = os.path.join(current_directory, 'data', 'headers.file')

selected_log = '0'

# Define the layout of the window
layout = [
    [sg.Text("Select Log FIle:"), sg.Input(key="-IN-"), sg.FileBrowse(file_types=(("CSV File", "*.csv"),))],
    [sg.Exit(), sg.Button("OK")],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Button("Generate MAF Calibration")],
    [sg.Button("Exit")],
]

# Create the window with resizable flag set to True
window = sg.Window("Log To MAF indev-0.1", layout, resizable=True)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "OK":
        selected_log = values["-IN-"]

    if event == "Exit" or event == sg.WINDOW_CLOSED:
        exit()
    if event == "Generate MAF Calibration":
        Generate_Maf_cal(selected_log, headers_file_path)