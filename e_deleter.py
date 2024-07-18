import re

def process_file(file_path):
    # Read the entire file into memory
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Modify the lines as needed
    for i in range(len(lines)):
        # Use regular expression to remove "E.0" and its following numbers
        lines[i] = re.sub(r'E0\.0\d*', 'E0.0', lines[i])

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
