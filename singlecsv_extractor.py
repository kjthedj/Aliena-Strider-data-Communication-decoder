import os
import glob
import openpyxl
import re

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

def process_binary_file(file_path):
    try:
        with open(file_path, 'rb') as binary_file:
            binary_data = binary_file.read()  # Read all bytes in the file
            return binary_data.hex()  # Return the binary data as a hexadecimal string
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

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

def convert_binary_to_excel(folder_path, output_excel_file):
    max_bytes_files = get_files_with_max_bytes(folder_path)

    if not max_bytes_files:
        print("No binary files found in the folder.")
        return

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(['File Name', 'Date', 'Time', 'Binary Data (Hexadecimal)'])

    for file_path in max_bytes_files:
        binary_data_hex = process_binary_file(file_path)
        if binary_data_hex is not None:
            file_name = os.path.basename(file_path)
            date_time_str = extract_date_time_from_filename(file_name)
            if date_time_str:
                date_str, time_str = date_time_str.split(' ')
                sheet.append([file_name, date_str, time_str, binary_data_hex])

    # Save the data in the Excel workbook
    workbook.save(output_excel_file)

if __name__ == "__main__":
    folder_path = 'succesfuldataget'  # Replace 'your_folder_path' with the actual path of the folder containing binary files.
    output_excel_file = 'output_data6.xlsx'  # Name of the output Excel file
    convert_binary_to_excel(folder_path, output_excel_file)
