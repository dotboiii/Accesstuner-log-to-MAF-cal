import csv

def open_csv(selected_log):
    with open(selected_log, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_array = list(csv_reader)
        headers = line_array[0]
        return line_array, headers

def csv_to_list(selected_file):
    with open(selected_file, 'r') as csv_file:
        csv_data = csv.reader(csv_file)
        flat_list = [data for row in csv_data for data in row]
        return flat_list

def search_column(search_item, dataset):
    search_return = dataset.index(search_item)
    return search_return

def column_to_list(selected_log, index):
    with open(selected_log, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header line
        columndata = [row[index] for row in csv_reader if len(row) > index]
    return columndata

def search_all_headers(filename):
    _, headers = open_csv(filename)
    header_index_array = []
    for header_reader in headers:
        search_return = search_column(header_reader, headers)
        header_index = f"{header_reader},{search_return}"
        header_index_array.append(header_index)
    return header_index_array
