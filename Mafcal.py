import csv
import numpy as numpy 
from scipy.optimize import curve_fit
from scan import open_csv, search_column, column_to_list, csv_to_list

def exponential_func(x, a, b, c):
    return a * numpy.exp(-b * x) + c

def Generate_Maf_cal(selected_log, headers_file_path, Maf_voltage_table):
    _, headers = open_csv(selected_log)
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
    MAFV = list(map(float, column_to_list(selected_log, MAFVI)))
    MAF = list(map(float, column_to_list(selected_log, MAFI)))
    STFT = list(map(float, column_to_list(selected_log, STFTI)))
    LTFT = list(map(float, column_to_list(selected_log, LTFTI)))

    FT_Combine = [sum(x)*0.01 for x in zip(STFT, LTFT)]
    MAF_COR = [sum(x) for x in zip(FT_Combine, MAF)]

    # curve fit
    x_data = numpy.array(MAFV)
    y_data = numpy.array(MAF_COR)
    popt, _ = curve_fit(exponential_func, x_data, y_data)
    a_opt, b_opt, c_opt = popt
    x = numpy.linspace(0, 5, 100)
    y_fit = exponential_func(x, a_opt, b_opt, c_opt)
    
    # Multiply data by corrected curve and return Correction_List
    CorrectiveFunction = f"y = {a_opt} * exp(-{b_opt} * x) + {c_opt}"
    print(CorrectiveFunction)
    a_opt_float, b_opt_float, c_opt_float = map(float, (a_opt, b_opt, c_opt))
    Volt_list_float = list(map(float, csv_to_list(Maf_voltage_table)))
    Correction_List = [a_opt_float * numpy.exp(-b_opt_float * x) + c_opt_float for x in Volt_list_float]
    print(Correction_List)

    Maf_Cor_Table = [] # This is empty??? probably unused
    return CorrectiveFunction, x_data, y_data, x, y_fit, Maf_Cor_Table, Correction_List