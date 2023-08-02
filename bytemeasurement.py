import os
import glob

def read_binary_files_in_folder(folder_path):
    # Step 1: Use glob to get the list of binary files in the folder
    binary_file_paths = glob.glob(os.path.join(folder_path, '*.bin'))

    for file_path in binary_file_paths:
        try:
            # Step 3: Read the binary data from each file
            with open(file_path, 'rb') as binary_file:
                binary_data = binary_file.read()

                # Process the binary data here (optional)
                # For example, you can manipulate the binary data or extract information from it.

                # Replace the print statement with your processing logic
                print(f"Reading {file_path}: {len(binary_data)} bytes read.")
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")

# Replace 'your_folder_path' with the actual path of the folder containing binary files.
folder_path = 'succesfuldataget'
read_binary_files_in_folder(folder_path)
