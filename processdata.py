import os
import glob
import struct
import openpyxl
import re

# Define the data structure as a tuple
DATA_STRUCTURE = (
    ('ECU TEMP',2),
    ('Anode 1 Set Voltage', 2),
    ('Anode 1 Voltage', 2),
    ('Anode 1 Current', 2),
    ('Anode 1 Temp', 2),
    ('Heater PPU Temp', 2),
    ('C1 Set Voltage', 2),
    ('C1 Voltage', 2),
    ('C1 Set Current', 2),
    ('C1 Current', 2),
    ('C1 Temp', 2),
    ('H1 PWM', 1),
    ('H2 PWM', 1),
    ('HP Tank Pressure Transducer', 2),
    ('LP Tank Pressure Transducer', 2),
    ('Anode Pressure Transducer', 2),
    ('Cathode Pressure Transducer', 2),
    ('HP Tank Temp', 2),
    ('Driver Circuit Temp', 2),
    ('Anode MFC Temp', 2),
    ('Cathode MFC Temp', 2),
    ('High Pressure Reg Temp', 2),
    ('IEP 1 (HP Tank)', 1),
    ('IEP 2 (LP Tank)', 1),
    ('IEP 3 (MFC1)', 1),
    ('IEP 4 (MFC2)', 1),
    ('Anode MFC', 2),
    ('Cathode MFC', 2),
    ('PMA Switch Valve', 2),
    ('Memory', 2),
    ('Firing Time Set', 2),
    ('Firing Counter 1', 4),
    ('Firing Counter 2', 4),
    ('Error Vector 1', 2),
    ('Error Vector 2', 2),
    ('Ignition Mode', 1),
    ('Tank Indicator', 1),
    ('IEP3 Frequency Parameter', 2),
    ('IEP4 Frequency Parameter', 2),
    ('Heater1 Frequency Setting', 2),
    ('Heater2 Frequency Setting', 2),
    ('SPARE', 2),
    ('SPARE', 1),
    ('SPARE', 1),
    ('SPARE', 2),
    ('CRC', 2)
)

def concatenate_data(binary_data_chunks):
    concatenated_data = []
    for field, num_bytes in DATA_STRUCTURE:
        data = binary_data_chunks[:num_bytes]
        binary_data_chunks = binary_data_chunks[num_bytes:]
        # Combine the bytes and convert to a readable value (e.g., integer, float, etc.)
        joined_data = ''.join(data)
        if num_bytes == 2:
            value = int(joined_data, 16)  # Convert hexadecimal string to integer
        elif num_bytes == 4:
            value = struct.unpack('>f', bytes.fromhex(joined_data))[0]  # Use big-endian byte order
        elif num_bytes == 1:
            value = int(joined_data, 16)  # Convert hexadecimal string to integer
        else:
            # Handle other cases as needed
            value = joined_data
        concatenated_data.append(value)
    return concatenated_data

#extract date and timestamp for data 
def extract_date_time_from_filename(file_name):
    # Regular expression to extract the date and time from the filename
    pattern = r'FTP_(\d{8})_(\d{2})(\d{2})(\d{2}\.\d+)_'
    match = re.match(pattern, file_name)
    if match:
        date_str, hour, minute, second = match.groups()
        # Convert the extracted information into a datetime object
        date_time_str = f"{date_str} {hour}:{minute}:{second}"
        return date_time_str
    else:
        return None
    
#read files for binary data
def process_binary_file(file_path):
    try:
        with open(file_path, 'rb') as binary_file:
            binary_data = binary_file.read()  # Read all bytes in the file
            return binary_data
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

#find datagets by find files with max bytes
def get_files_with_max_bytes(folder_path):
    binary_file_paths = glob.glob(os.path.join(folder_path, '*.bin'))

    max_bytes = 0
    max_bytes_files = []

    for file_path in binary_file_paths:
        file_size = os.path.getsize(file_path)
        if file_size > max_bytes:
            max_bytes = file_size
            max_bytes_files = [file_path]
        elif file_size == max_bytes:
            max_bytes_files.append(file_path)

    return max_bytes_files

#store values in excel
def convert_binary_to_excel(folder_path, output_excel_file):
    max_bytes_files = get_files_with_max_bytes(folder_path)

    if not max_bytes_files:
        print("No binary files found in the folder.")
        return

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    column_names = ['File Name', 'Date', 'Time'] + [field for field, _ in DATA_STRUCTURE]
    sheet.append(column_names)

    for file_path in max_bytes_files:
        binary_data = process_binary_file(file_path)
        if binary_data is not None:
            file_name = os.path.basename(file_path)
            date_time_str = extract_date_time_from_filename(file_name)
            if date_time_str:
                date_str, time_str = date_time_str.split(' ')
                binary_data_hex = binary_data.hex()
                binary_data_chunks = [binary_data_hex[i:i + 2] for i in range(24, len(binary_data_hex), 2)]  # Exclude first 12 chunks (24 bytes)
                concatenated_data = concatenate_data(binary_data_chunks)
                sheet.append([file_name, date_str, time_str] + concatenated_data)


    # Save the data in the Excel workbook
    workbook.save(output_excel_file)

if __name__ == "__main__":
    folder_path_input = input('Enter a folder path: ')# prompt users to enter a file path
    if os.path.exists(folder_path_input):
        folder_path = folder_path_input
    else:
        print('Specified folder path doesnt exist')
    output_excel_file = 'output_data.xlsx'  # Name of the output Excel file
    convert_binary_to_excel(folder_path, output_excel_file)
