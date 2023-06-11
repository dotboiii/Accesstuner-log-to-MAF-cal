import csv
import scan
import numpy as np 
import matplotlib.pyplot as plt 
import math
from scipy.optimize import curve_fit
import PySimpleGUI as sg
from scan import open_log_file, search_column, column_to_list


#Creating GUI





#running the open function to return the array of headers
selected_log = 'C:/VS code/Python projects/Accesstun log tester/log.csv'
line_array, headers = open_log_file(selected_log)

#opens the dictionary file, dictionary must contain all headers in txt seperated by newline.
with open('C:/VS code/Python projects/Accesstun log tester/headers.file', 'r') as header_dictionary_file:
    header_dictionary = csv.reader(header_dictionary_file)
    #loop searches for which index each header is, references dictionary file to know what to find.
    #each dictonary file read is a list with the string in the index 1, ignores index 0.
    #index_dictionary = {}
    for header_dictionary in enumerate(headers):
        header_reader = header_dictionary[1]
        search_return = search_column(header_reader, headers)
        print(search_return, header_reader)
        #index_dictionary [header_reader]=search_return
        #Partial string search to gather the index for MAFV MAF STFT and LTFT in the file
        if 'MAF V' in header_reader:
            MAFVI = search_return
        if 'Mass A' in header_reader:
            MAFI = search_return
        if 'Short T' in header_reader:
            STFTI = search_return
        if 'Long T' in header_reader:
            LTFTI = search_return

#grabbing lists for each data type, converting list to floating point numbers
MAFV = [float (i) for i in column_to_list(selected_log, MAFVI)]
MAF = [float (i) for i in column_to_list(selected_log, MAFI)]
STFT = [float (i) for i in column_to_list(selected_log, STFTI)]
LTFT = [float (i) for i in column_to_list(selected_log, LTFTI)]

#combining two data types by addition Fuel trims
FT_Combine = [sum(x)*0.01 for x in zip(STFT, LTFT)]

#applying fuel trim correction factors to the lists
##MAFV_COR = [sum(x) for x in zip(FT_Combine, MAFV)]
MAF_COR = [sum(x) for x in zip(FT_Combine, MAF)]

#curve fitting:

# Define the function to fit
def exponential_func(x, a, b, c):
    return a * np.exp(-b * x) + c

# Generate example data
x_data = np.array(MAFV)  # Replace with your actual x data
y_data = np.array(MAF_COR)  # Replace with your actual y data

# Perform curve fitting
popt, pcov = curve_fit(exponential_func, x_data, y_data)

# Extract the optimized parameters
a_opt, b_opt, c_opt = popt

# Generate x values for plotting
x = np.linspace(0, 5, 100)  # Adjust the range and number of points as needed

# Calculate the corresponding y values using the optimized parameters
y_fit = exponential_func(x, a_opt, b_opt, c_opt)

print(f"y = {a_opt} * exp(-{b_opt} * x) + {c_opt}")

# Plot the original data points and the fitted curve
plt.scatter(x_data, y_data, color='red', label='Data Points')
#plt.scatter(MAFV,MAF, color='purple', label='Original')
plt.plot(x, y_fit, 'b-', label='Fitted Curve')

# Set the labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Curve Fitting with Fitted Curve')

# Display the legend
plt.legend()

# Show the plot
plt.show()

