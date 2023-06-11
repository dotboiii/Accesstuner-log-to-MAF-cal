import csv
import scan
from scan import open_log_file, search_column

logfile = 'C:/VS code/Python projects/Accesstun log tester/datalog6.csv'
header_dictionary_file = 'C:/VS code/Python projects/Accesstun log tester/headers.file'
headeer_blacklist_file = 'C:/VS code/Python projects/Accesstun log tester/headersblacklist.file'

def add_to_dictionary(selected_log):
    line_array, headers = open_log_file(selected_log)
    with open(header_dictionary_file, 'a') as dictionaryfile:
        for newheader in headers:
            dictionaryfile.write("%s\n" % newheader)
        print("Added: ", headers)
        dictionaryfile.close()
        
#selected_log = input('Enter log file name to add dictionaries: ')
#add_to_dictionary(selected_log)

def dictionary_clean():
    #opens the dictionary file, converts it to a set
    with open(header_dictionary_file, 'r') as dictionaryfile:
        header_dictionary = dictionaryfile.readlines()
        header_dictionary_set = set(header_dictionary)
    #reads the blacklist file, converts to a set
    with open(headeer_blacklist_file, 'r') as dictionaryblacklist:
        header_blacklist = dictionaryblacklist.readlines()
        header_blacklist_set = set(header_blacklist)
    #compares the dictionary set to the blacklist set. Searches the dictionary and removes matches
    header_dictionary_set_copy = header_dictionary_set.copy()
    for word in header_blacklist_set:
        for item in header_dictionary_set_copy:
            if word in item:
                header_dictionary_set.remove(item)
    #re-writes the dicitonary file with the new cleaned set
    with open(header_dictionary_file, 'w') as dictionaryfile:
        for rewrite_header in header_dictionary_set:
            dictionaryfile.write("%s" % rewrite_header)
        print("Cleaned header dictionary!")
    #cleans any blank newlines out of the dictionary file
    with open(header_dictionary_file, 'r+') as dictionaryfileclear:    
        for line in dictionaryfileclear:
            if not line.isspace():
                dictionaryfileclear.write(line)


add_to_dictionary(logfile)
dictionary_clean()
    