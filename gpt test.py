import csv

logfile = 'C:/Users/boi/Documents/Python projects/Accesstun log tester/datalog6.csv'
header_dictionary_file = 'C:/Users/boi/Documents/Python projects/Accesstun log tester/headerstest.file'
header_blacklist_file = 'C:/Users/boi/Documents/Python projects/Accesstun log tester/headersblacklist.file'

def add_to_dictionary(selected_log):
    line_array, headers = open_log_file(selected_log)
    with open(header_dictionary_file, 'a') as dictionaryfile:
        dictionaryfile.write('\n'.join(headers) + '\n')
    print("Added:", headers)

def dictionary_clean():
    header_dictionary_set = read_file_to_set(header_dictionary_file)
    header_blacklist_set = read_file_to_set(header_blacklist_file)

    header_dictionary_set -= header_blacklist_set

    write_set_to_file(header_dictionary_set, header_dictionary_file)
    remove_blank_lines(header_dictionary_file)

def open_log_file(selected_log):
    with open(selected_log, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_array = list(csv_reader)
        headers = line_array[0]
        return line_array, headers

def read_file_to_set(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    return set(content)

def write_set_to_file(data_set, file_path):
    with open(file_path, 'w') as file:
        file.writelines(data_set)

def remove_blank_lines(file_path):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.writelines(line for line in lines if not line.isspace())

add_to_dictionary(logfile)
dictionary_clean()