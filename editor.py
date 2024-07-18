import re

# This function adds a E0.0 at the end of the line with no E to maintain the logic of the algorithm
def e_line_editor(input_file_path):
    with open(input_file_path, "r+") as file:
        # Read all lines from the file
        lines = file.readlines()

        # Move the file cursor to the beginning
        file.seek(0)

        # Iterate through the lines and modify as needed
        for line in lines:
            if line.startswith("G1") and "X" in line and "Y" in line and "E" not in line:
                # Add E0.0 at the end of the line
                modified_line = re.sub(r'\n', ' E0.0\n', line)
                file.write(modified_line)
            else:
                file.write(line)

        # Truncate the file in case the new content is shorter than the previous content
        file.truncate()
