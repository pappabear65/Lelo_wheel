
##############
## circular buffer based on file size
##############


import os

# Define the file and the maximum file size (in bytes)
FILENAME = "data.csv"
MAX_FILE_SIZE = 1024  # Maximum file size in bytes (1KB in this example)

# Initialize the file if it doesn't exist
if FILENAME not in os.listdir():
    with open(FILENAME, "w") as f:
        f.write("Index,Data\n")  # CSV headers

# Function to get the current file size
def get_file_size(filename):
    return os.stat(filename)[6]

# Function to read all lines except header
def read_data_lines(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return lines[0], lines[1:]  # Return header and data separately

# Function to overwrite the file in a circular way based on file size
def write_entry_to_csv(data):
    # Get the current file size
    file_size = get_file_size(FILENAME)
    
    # If the file size exceeds the maximum, start overwriting from the beginning
    if file_size >= MAX_FILE_SIZE:
        header, data_lines = read_data_lines(FILENAME)
        
        # Start overwriting the oldest data (line 1 after the header)
        data_lines.append(f"{len(data_lines)},{data}\n")
        # Write the updated data back to the file
        with open(FILENAME, "w") as f:
            f.write(header)  # Write the header back
            # Write updated lines, removing the oldest line
            f.writelines(data_lines[-(len(data_lines)-1):])  # Keep the last entries, removing the first

    else:
        # If file size is within the limit, append the data
        with open(FILENAME, "a") as f:
            # Add the new data
            num_entries = len(read_data_lines(FILENAME)[1])  # Count existing entries
            f.write(f"{num_entries},{data}\n")

# Example Usage
data_to_log = "SensorData"  # Replace with your data source
write_entry_to_csv(data_to_log)



##############
## circular buffer based on number of entries
##############

import os

# Define the file and the buffer size (in number of entries)
FILENAME = "data.csv"
MAX_ENTRIES = 100  # Maximum number of lines allowed in the CSV file

# Initialize the file if it doesn't exist
if not FILENAME in os.listdir():
    with open(FILENAME, "w") as f:
        f.write("Index,Data\n")  # CSV headers

# Function to count current number of entries in the CSV
def count_entries_in_file(filename):
    with open(filename, "r") as f:
        return len(f.readlines()) - 1  # Exclude header

# Function to overwrite the file in a circular way
def write_entry_to_csv(data):
    # Check the current number of entries
    num_entries = count_entries_in_file(FILENAME)
    
    # If the file is full, overwrite from the beginning
    if num_entries >= MAX_ENTRIES:
        overwrite_index = (num_entries % MAX_ENTRIES) + 1  # +1 to skip header
        temp_filename = "temp.csv"
        
        # Copy contents except the old entry
        with open(FILENAME, "r") as f, open(temp_filename, "w") as temp_f:
            lines = f.readlines()
            # Write the header
            temp_f.write(lines[0])
            # Write the data replacing the old entry
            for i in range(1, len(lines)):
                if i == overwrite_index:
                    temp_f.write(f"{overwrite_index},{data}\n")
                else:
                    temp_f.write(lines[i])

        # Replace the old file with the updated one
        os.remove(FILENAME)
        os.rename(temp_filename, FILENAME)
    else:
        # If the file is not full, append the data
        with open(FILENAME, "a") as f:
            f.write(f"{num_entries},{data}\n")

# Example Usage
data_to_log = 123  # Replace with your data source
write_entry_to_csv(data_to_log)
