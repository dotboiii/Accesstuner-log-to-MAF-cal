import csv
import numpy as np 
from scipy.optimize import curve_fit
from scan import open_csv, search_column, column_to_list, csv_to_list
import math

def Generate_Maf_cal(selected_log, headers_file_path, Maf_voltage_table):
    do_not_use, headers = open_csv(selected_log)
    #opens the dictionary file, dictionary must contain all headers in txt seperated by newline.
    with open(headers_file_path, 'r') as header_dictionary_file:
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
    popt, do_not_use = curve_fit(exponential_func, x_data, y_data)

    # Extract the optimized parameters
    a_opt, b_opt, c_opt = popt

    # Generate x values for plotting
    x = np.linspace(0, 5, 100)  # Adjust the range and number of points as needed

    # Calculate the corresponding y values using the optimized parameters
    y_fit = exponential_func(x, a_opt, b_opt, c_opt)

    Maf_Cor_Table = []
    print(f"y = {a_opt} * exp(-{b_opt} * x) + {c_opt}")
    CorrectiveFunction = f"y = {a_opt} * exp(-{b_opt} * x) + {c_opt}"
    
    a_opt_float = float(a_opt)
    b_opt_float = float(b_opt) 
    c_opt_float = float(c_opt)

    Volt_list = csv_to_list(Maf_voltage_table)
    print(Volt_list)
    
    Volt_list_float = []
    for string in Volt_list:
        Volt_list_float.append(float(string))
    
    Correction_List = [a_opt_float * math.exp(-b_opt_float * x) + c_opt_float for x in Volt_list_float]
    print(Correction_List)

        
    return CorrectiveFunction, x_data, y_data, x, y_fit, Maf_Cor_Table, Correction_List