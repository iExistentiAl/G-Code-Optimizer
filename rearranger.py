import re

# Using the information from an output file, going through original gcode and rebuilding it in a new file
def extract_values_and_flip_content(file_to_check, input_file_path):
    # Extract values from the first file
    with open(file_to_check, 'r') as file:
        lines = file.readlines()

    start_lines = []
    end_lines = []

    for line in lines:
        if 'X' in line:
            # Extracting the last two integers from the parentheses
            match = re.search(r'(\d+),\s*(\d+)\s*,\s*X', line)
            if match:
                value1, value2 = map(int, match.groups())
                start_lines.append(value1)
                end_lines.append(value2)

    if not start_lines or not end_lines:
        print("No lines with 'X' found in the file.")
        return

    print("Start Line Values:", start_lines)
    print("End Line Values:", end_lines)

    # Flip content in the second file based on extracted values
    for start_line_value, end_line_value in zip(start_lines, end_lines):
        flip_content_between_lines(input_file_path, start_line_value, end_line_value)    

# Flipping the groups which have to be flipped, they are marked with XY in the output file
def flip_content_between_lines(input_file_path, start_line, end_line):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # Subtracting 1 to convert line number to list index
    start_index = start_line 
    end_index = end_line - 1

    # Ensure start and end indices are within the range of the file
    if 0 <= start_index < len(lines) and 0 <= end_index < len(lines):
        # Identify lines with E values and their positions
        e_lines = [(index, re.search(r'E\d*\.\d+', line)) for index, line in enumerate(lines[start_index:end_index + 1], start=start_index) if re.search(r'E\d*\.\d+', line)]

        # Flip the content between the start and end lines
        lines[start_index:end_index + 1] = reversed(lines[start_index:end_index + 1])

        # Insert the E values back at their original positions
        for index, match in e_lines:
            if match:
                e_value = match.group()
                lines[index] = re.sub(r'E\d*\.\d+', e_value, lines[index])

        # Write the modified content back to the file
        with open(input_file_path, 'w') as file:
            file.writelines(lines)
        print(f"Flipped content between lines {start_line} and {end_line}, keeping E values in place.")
    else:
        print("Invalid start or end line values. Skipping.")

file_to_check = "rearranged_output.txt"


# Removing XY completely, because the lines were flipped already and there is no need for them no more
def remove_x_from_lines(file_to_check):
    with open(file_to_check, 'r') as file:
        lines = file.readlines()

    # Remove ", X" from each line
    modified_lines = [line.replace(', XY', '') for line in lines]

    # Write the modified content back to the original file
    with open(file_to_check, 'w') as file:
        file.writelines(modified_lines)


# Copying the groups with this function, based on the end and start lines
def copy_lines_between(file_path, start_line, end_line):
    lines = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if start_line <= line_number <= end_line:
                lines.append(line.strip())
    return lines

# Pasting them into a new file
def paste_lines_into_file(lines, output_file_path):
    with open(output_file_path, 'a') as output_file:
        for line in lines:
            output_file.write(line + '\n')


# Basically finishing the build of the file, adding at the very top important Gcode part and at the end as well
def process_rearranged_file(rearranged_file_path, input_file_path, output_file_path):
    starting_G = "G28 ; home all axes\nG1 Z5 f5000; lift nozzle\nG21 ; set units to millimeters\nG90 ; use absolute coordinates\nM82 ; use absolute distances for extrusion"
    ending_G = "M107\nG28 Z0 ; home Z axis\nG28 X0  ; home X axis\nM84     ; disable motors\n"
    # Truncate the final outcome file
    with open(output_file_path, 'w'):
        pass
    
    with open(output_file_path, 'a') as output_file:
        output_file.write(starting_G)

    with open(rearranged_file_path, 'r') as rearranged_file:
        for line in rearranged_file:
            # Extract start and end values from the parentheses
            values = [val.strip() for val in line.split('(')[1].split(')')[0].split(',')]
            start_line, end_line = map(int, values)

            lines_to_copy = copy_lines_between(input_file_path, start_line, end_line)
            paste_lines_into_file(lines_to_copy, output_file_path)
    
    with open(output_file_path, 'a') as output_file:
        output_file.write(ending_G)

file_to_check = "rearranged_output.txt"
input_file_path = "output.txt"
extract_values_and_flip_content(file_to_check, input_file_path)



