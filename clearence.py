import re  

# Removing all the comments from the file, except layer change
def remove_comments_and_empty_lines(file, output_file):
    with open(file, "r") as file:
        lines = file.readlines()

    # Skip the lines which are ;LAYER_CHANGE
    filtered_lines = [line for line in lines if not (line.startswith(";") and not line.startswith(";LAYER_CHANGE")) and line.strip()]

    with open(output_file, "w") as file:
        file.writelines(filtered_lines)

# Deleting G92 after every T0 or T1, to make the logic of the algorithm simpler
def remove_g92_after_t0_t1(input_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    t0_t1_flag = False

    for i, line in enumerate(lines):
        if 'T0' in line or 'T1' in line:
            t0_t1_flag = True
        elif 'G92 E0' in line and t0_t1_flag:
            del lines[i]
        elif 'G92 E0' not in line:
            t0_t1_flag = False

    with open(input_file_path, 'w') as file:
        file.writelines(lines)

# If you want to use the functions, you can call them here
if __name__ == "__main__":
    input_file_path = "XP_Weight_check_95gms.gcode"
    output_file_path = "output.txt"
    remove_comments_and_empty_lines(input_file_path, output_file_path)
    remove_g92_after_t0_t1(input_file_path)

    print("Cleaned")