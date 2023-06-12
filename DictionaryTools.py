from scan import open_csv
import os

# Get the current directory of the Python program
current_directory = os.path.dirname(os.path.abspath(__file__))
# Construct the file paths relative to the current directory
header_dictionary_file = os.path.join(current_directory, 'data', 'headers.file')
header_blacklist_file = os.path.join(current_directory, 'data', 'headersblacklist.file')

def add_to_dictionary(selected_log):
    _, headers = open_csv(selected_log)
    with open(header_dictionary_file, 'a') as dictionary_file:
        dictionary_file.writelines("%s\n" % new_header for new_header in headers)
        print("Added:", headers)

# Uncomment the following lines if you want to use the `add_to_dictionary` function directly
# selected_log = input('Enter log file name to add dictionaries: ')
# add_to_dictionary(selected_log)

def dictionary_clean():
    # Read the dictionary file and create a set
    with open(header_dictionary_file, 'r') as dictionary_file:
        header_dictionary = set(dictionary_file.readlines())
    
    # Read the blacklist file and create a set
    with open(header_blacklist_file, 'r') as blacklist_file:
        header_blacklist = set(blacklist_file.readlines())
    
    # Remove blacklisted headers from the dictionary set
    header_dictionary -= {item for item in header_dictionary if any(word in item for word in header_blacklist)}
    
    # Rewrite the cleaned dictionary set to the dictionary file
    with open(header_dictionary_file, 'w') as dictionary_file:
        dictionary_file.writelines(rewrite_header for rewrite_header in header_dictionary)
    print("Cleaned header dictionary!")
    
    # Remove any blank lines from the dictionary file
    with open(header_dictionary_file, 'r+') as dictionary_file_clear:
        lines = dictionary_file_clear.readlines()
        dictionary_file_clear.seek(0)
        dictionary_file_clear.writelines(line for line in lines if not line.isspace())
        dictionary_file_clear.truncate()
