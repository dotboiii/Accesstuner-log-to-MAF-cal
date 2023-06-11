import csv
import scan
import matplotlib.pyplot as plt
from scan import open_log_file, search_column, column_to_list, search_all_headers
from scipy.optimize import curve_fit

#def curve_fit(x, a, b):
#    return a*np.exp(b*x)
selected_log = 'C:/Users/boi/Documents/Python projects/Accesstun log tester/datalog6.csv'
line_array, headers = open_log_file(selected_log)

header_index_array = search_all_headers(selected_log)
print(header_index_array)