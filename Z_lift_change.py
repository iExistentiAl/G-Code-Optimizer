# from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

# class GCodeInputDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle('Input Values')
        
#         layout = QVBoxLayout()
        
#         self.z_height_label = QLabel('Enter Z Height:')
#         self.z_height_input = QLineEdit()
#         layout.addWidget(self.z_height_label)
#         layout.addWidget(self.z_height_input)
        
#         self.subtract_value_label = QLabel('Enter Value to Subtract:')
#         self.subtract_value_input = QLineEdit()
#         layout.addWidget(self.subtract_value_label)
#         layout.addWidget(self.subtract_value_input)
        
#         self.confirm_button = QPushButton('Confirm')
#         self.confirm_button.clicked.connect(self.accept)
#         layout.addWidget(self.confirm_button)
        
#         self.setLayout(layout)

def insert_gcode_above_tool_change(file_path, initial_z_height, subtract_value):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        
        z_height = initial_z_height  # Initialize the Z height counter
        insert_below_t1 = False  # Flag to indicate if the line should be inserted below T1
        T0_ongoing = True

        for line in lines:
            if line.startswith("T0"):
                file.write(f"G1 Z{z_height} F18000\n")  # Insert the G-code line below the tool change
                z_height += initial_z_height  # Increment the Z height counter
                insert_below_t1 = False  # Reset the flag
                file.write(line)  # Write the T0 line
                T0_ongoing = True
            elif line.startswith("T1"):
                file.write(line)  # Write the T1 line
                insert_below_t1 = True  # Set the flag to insert below T1
        
            elif "G1" in line:  # Check for G1 command
                if insert_below_t1:
                    file.write(line)  # Write the G1 line
                    if T0_ongoing:  # For even iterations, subtract the value
                        file.write(f"G1 Z{z_height - subtract_value} F18000\n")
                        z_height -= subtract_value
                        T0_ongoing = False
                    else:
                        file.write(f"G1 Z{z_height} F18000\n")
                    z_height += initial_z_height  # Increment the Z height counter
                    insert_below_t1 = False  # Reset the flag
                else:
                    file.write(line)  # Write the original G1 line
            else:
                file.write(line)  # Write other lines
        
        file.truncate()


def remove_g1_z_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Filter out lines that contain "G1" and "Z"
    filtered_lines = [line for line in lines if "G1" not in line or "Z" not in line or "F18000" not in line]

    # Reopen the file for writing and overwrite its content
    with open(file_path, 'w') as file:
        file.writelines(filtered_lines)

def write_tool_change(file_path):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        
        prev_tool = None
        layer_change_encountered = False  # Flag to track if layer change is encountered
        lines_after_layer_change = 0  # Counter for lines after layer change
        
        for i, line in enumerate(lines):
            if line.startswith("T0") or line.startswith("T1"):
                prev_tool = line.strip()  # Update the previous tool value
                file.write(line)  # Write the T0 or T1 line
            elif ";LAYER_CHANGE" in line:
                layer_change_encountered = True
                lines_after_layer_change = 0  # Reset the counter
                file.write(line)  # Write the line containing ;LAYER_CHANGE
            elif layer_change_encountered:
                if lines_after_layer_change == 1:  # Check if it's the second line after layer change
                    # Check if there's no T0 or T1 in the vicinity
                    t_in_vicinity = False
                    for j in range(max(i - 7, 0), min(i + 8, len(lines))):
                        if lines[j].startswith("T0") or lines[j].startswith("T1"):
                            t_in_vicinity = True
                            break
                    if not t_in_vicinity:
                        # Write the tool change line after the second line following ;LAYER_CHANGE
                        if prev_tool:
                            file.write(prev_tool + '\n')
                        else:
                            file.write("T0\n")
                        layer_change_encountered = False  # Reset the flag
                elif lines_after_layer_change > 1:  # Check if it's beyond the second line after layer change
                    # Reset the flag if there's a T0 or T1 command within the vicinity
                    for j in range(max(i - 7, 0), min(i + 8, len(lines))):
                        if lines[j].startswith("T0") or lines[j].startswith("T1"):
                            layer_change_encountered = False
                            break
                lines_after_layer_change += 1  # Increment the counter
                file.write(line)  # Write the line after ;LAYER_CHANGE
            else:
                file.write(line)  # Write other lines
        
        file.truncate()




def remove_consecutive_duplicates_inplace(file_path):
    # Read the file and store its contents
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)

        # Initialize a variable to store the previous line
        prev_line = None

        # Iterate through the lines and remove consecutive duplicate lines
        for line in lines:
            if line != prev_line:  # Check if the current line is different from the previous one
                file.write(line)  # Write the line if it's different
            prev_line = line  # Update the previous line
        
        file.truncate()

# Example usage:



if __name__ == "__main__":
    input_file_path = "XP_Weight_check_95gms.gcode"
    # remove_g1_z_lines(input_file_path)
    # write_tool_change(input_file_path)
    # remove_consecutive_duplicates_inplace(input_file_path)
    # insert_gcode_above_tool_change(input_file_path)