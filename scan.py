import csv

#opens the log file, returns the entire file and only the headers as two objects.
def open_csv(selected_log):
    with open(selected_log, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_array = []
        for csvdata in csv_reader:
            line_array.append(csvdata)
        headers = line_array[0]
        return line_array, headers
    
def csv_to_list(selected_file):
    csv_list = []
    flat_list = []
    with open(selected_file, 'r') as csv_file:
        csv_data = csv.reader(csv_file)
        for row in csv_data:
            csv_list.append(row)
        for sublist in csv_list:
            flat_list.extend(sublist)
        return flat_list

#Searches for an item in an array, input the string and which array to search, returns the index.
def search_column(search_item = '', dataset = []):
    search_return = dataset.index(search_item)
    return search_return

def column_to_list(selected_log, index):
    columndata = []
    with open(selected_log, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader) #skips header line
        
        for row in csv_reader:
            if len(row) > index:
                columndata.append(row[index])
    return columndata

def search_all_headers(filename):
    line_array, headers = open_csv(filename)
    with open(filename, 'r') as header_dictionary_file:
        header_dictionary = csv.reader(header_dictionary_file)
    header_index_array = []
    #loop searches for which index each header is, references dictionary file to know what to find.
    #each dictonary file read is a list with the string in the index 1, ignores index 0.
    for header_dictionary in enumerate(headers):
        header_reader = header_dictionary[1]
        search_return = search_column(header_reader, headers)
        #print(search_return, header_reader) #debug
        header_index = '%s,%s' % (header_reader, search_return)
        header_index_array.append(header_index)
    return header_index_array