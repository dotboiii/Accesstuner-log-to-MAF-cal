import PySimpleGUI as gui
import os
from mafcal import Generate_Maf_cal
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
    [gui.Text("Select Log FIle:"), gui.Input(key="-IN-"), gui.FileBrowse(file_types=(("CSV File", "*.csv"),))],
    [gui.Canvas(key="-CANVAS-")],
    [gui.Button("Generate MAF Calibration")],
    [gui.Button("Copy to clipboard!")],
    [gui.Button("Show Plot")],
    [gui.Text("Formula Generated:"), gui.Text(key="-FORMULA-")],
]

# Create the window with resizable flag set to True
window = gui.Window("Log To MAF alpha 1.0", layout, resizable=True)

while True:
    event, values = window.read()
    if event == gui.WINDOW_CLOSED:
        exit() 
    if event == "Generate MAF Calibration":
        if values["-IN-"] == '':
            gui.popup("Please select a log file!")
        else:
            selected_log = values["-IN-"]
            try:
                CorrectiveFunction, x_data, y_data, x, y_fit, Maf_Cor_Table, Correction_List = Generate_Maf_cal(selected_log, headers_file_path, Maf_voltage_table)
                window["-FORMULA-"].update(CorrectiveFunction)
            except:
                gui.popup("Error occured, please check the log file and try again, if the problem persists across multiple logs please contact the developer.")
    if event == "Show Plot":
        try:
            draw_figure(x_data, y_data, x, y_fit)
        except:
            gui.popup("Internal error, enter in a log first? log may be too long, if else please contact the developer.")
    if event == "Copy to clipboard!":
        
        try:
            for i in range(len(Correction_List)):
                if Correction_List[i] < 0:
                    Correction_List[i] = 0
            Unpack_Clipboard = ",".join(str(x) for x in Correction_List)
            pyperclip.copy(Unpack_Clipboard)
        except:
            gui.popup("Unable to copy to the clipboard. Make sure you have generated a MAF calibration first.")