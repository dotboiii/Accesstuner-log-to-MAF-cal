import numpy as np 
import PySimpleGUI as sg
import os
from Mafcal import Generate_Maf_cal
import matplotlib.backends.backend_tkagg
from draw import draw_figure
import pyperclip

# Get the current directory of the Python program
current_directory = os.path.dirname(os.path.abspath(__file__))
# Construct the file path to the 'headers.file' relative to the current directory
headers_file_path = os.path.join(current_directory, 'data', 'headers.file')
# find the stock maf voltage table
Maf_voltage_table = os.path.join(current_directory, 'data', 'MAZDASPE3_STOCK_MAF_V_TABLE.csv')

selected_log = '0'

# Define the layout of the window
layout = [
    [sg.Text("Select Log FIle:"), sg.Input(key="-IN-"), sg.FileBrowse(file_types=(("CSV File", "*.csv"),))],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Button("Generate MAF Calibration")],
    [sg.Button("Copy to clipboard!")],
    [sg.Button("Show Plot")],
    [sg.Text("Formula Generated:"), sg.Text(key="-FORMULA-")],
]

# Create the window with resizable flag set to True
window = sg.Window("Log To MAF alpha 1.0", layout, resizable=True)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        exit() 
    if event == "Generate MAF Calibration":
        try:
            selected_log = values["-IN-"]
        except:
            sg.popup("Please select a log file!")
        try:
            CorrectiveFunction, x_data, y_data, x, y_fit, Maf_Cor_Table, Correcttion_List = Generate_Maf_cal(selected_log, headers_file_path, Maf_voltage_table)
            window["-FORMULA-"].update(CorrectiveFunction)
        except:
            sg.popup("Error occured, please check the log file and try again, if the problem persists across multiple logs please contact the developer.")
    if event == "Show Plot":
        try:
            draw_figure(x_data, y_data, x, y_fit)
        except:
            sg.popup("Internal error, enter in a log first? log may be too long, if else please contact the developer.")
    if event == "Copy to clipboard!":
        
        try:
            for i in range(len(Correcttion_List)):
                if Correcttion_List[i] < 0:
                    Correcttion_List[i] = 0
            Unpack_Clipboard = ",".join(str(x) for x in Correcttion_List)
            pyperclip.copy(Unpack_Clipboard)
        except:
            sg.popup("Unable to copy to the clipboard. Make sure you have generated a MAF calibration first.")