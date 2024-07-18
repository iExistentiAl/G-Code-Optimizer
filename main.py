import sys
import io
import os
from clearence import remove_comments_and_empty_lines, remove_g92_after_t0_t1
from editor import e_line_editor
from temporary import create_file
from countingG92 import G92_count
from optimization import find_lines_with_XY, remove_xy_from_previous_line_in_place
from extrusionrate import update_gcode_with_extrusion
from rearranger import process_rearranged_file, extract_values_and_flip_content, remove_x_from_lines
from owo_flipper import delete_group_lines


# Check if a file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python your_script.py path/to/your/file.gcode")
    sys.exit(1)

input_file_path = sys.argv[1]
output_file_path = "output.txt"
original_stdout = sys.stdout
sys.stdout = io.StringIO()

print("Processing file:", input_file_path)

remove_comments_and_empty_lines(input_file_path, output_file_path)

remove_g92_after_t0_t1(output_file_path)

e_line_editor(output_file_path)


file_path = "rearranged_output.txt"


create_file("1_temp.txt")
groups = G92_count(output_file_path)
captured_output = sys.stdout.getvalue()
temp_file = "1_temp.txt"
input_file = "rearranged_output.txt"
check_file = "output.txt"

with open(temp_file, "w") as f:
    sys.stdout = f
    for idx, group in enumerate(groups, 1):
        t_value = group['t_value']
        coordinates = group['coordinates']
        z_level = group['z_level'] if group['z_level'] is not None else ''

        start_line_no = group['start_line_no']
        end_line_no = group['end_line_no']

        print(f"{t_value} Group {idx} (Lines {start_line_no}-{end_line_no})" +
            (f" Start: X {coordinates[0][0]:.3f} Y {coordinates[0][1]:.3f}" if coordinates else "") +
            (f" End: X {coordinates[-1][0]:.3f} Y {coordinates[-1][1]:.3f}" if coordinates else "") +
            (f" Z {z_level}" if z_level or z_level else ""))

    sys.stdout = original_stdout


input_file_path = "1_temp.txt"
output_file_path = "rearranged_output.txt"
final_outcome_path = "final_outcome.txt"


# Find lines with Z and write to rearranged_output.txt
group_list = find_lines_with_XY(input_file_path, output_file_path)


remove_xy_from_previous_line_in_place(output_file_path)


input_file_path = "rearranged_output.txt"

# reorder_groups(input_file_path) //This function was used when I tried to play around with OWO  
delete_group_lines(input_file_path) 

file_to_check = "rearranged_output.txt"
input_file_path = "output.txt"

extracted_values = extract_values_and_flip_content(file_to_check, input_file_path)
remove_x_from_lines(file_to_check)

# Process rearranged_output.txt and write to final_outcome.txt
for i, group in enumerate(group_list, start=1):
    print(f"Group {i}:")
    for (start_x, end_x, start_y, end_y), line_numbers, group_number, first_start_line in group["start_end_coordinates"]:
        print(f"    Part: {group_number}, Start X: {start_x:.3f}, End X: {end_x:.3f}, Start Y: {start_y:.3f}, End Y: {end_y:.3f} (Lines {', '.join(map(str, line_numbers))})")


# Call process_rearranged_file to copy lines from rearranged_output.txt to final_outcome.txt
process_rearranged_file(output_file_path, check_file, final_outcome_path)

# Recalculate extrusion at the end
with open(final_outcome_path, 'r') as f:
    gcode_lines = f.readlines()

updated_gcode_lines = update_gcode_with_extrusion(gcode_lines)
with open(final_outcome_path, 'w') as f:
    f.writelines(updated_gcode_lines)

if __name__ == "__main__":
    input_file_path = sys.argv[1]
    custom_name = sys.argv[2]
    output_directory = sys.argv[3]

    # Construct the full output file path
    output_file_path = os.path.join(output_directory, custom_name + "_output.gcode")


def create_and_insert_output_file(output_content, output_file_path):
    with open(output_file_path, 'w') as output_file:
        output_file.write(output_content)

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Usage: python your_script.py path/to/your/file.gcode custom_name output_directory")
        sys.exit(1)

    input_file_path = sys.argv[1]
    custom_name = sys.argv[2]
    output_directory = sys.argv[3]


    output_file_path = os.path.join(output_directory, custom_name + ".gcode")

    for i, group in enumerate(group_list, start=1):
        print(f"Group {i}:")
        for (start_x, end_x, start_y, end_y), line_numbers, group_number, first_start_line in group["start_end_coordinates"]:
            print(f"    Part: {group_number}, Start X: {start_x:.3f}, End X: {end_x:.3f}, Start Y: {start_y:.3f}, End Y: {end_y:.3f} (Lines {', '.join(map(str, line_numbers))})")


    with open(final_outcome_path, 'r') as final_outcome_file:
        final_outcome_content = final_outcome_file.read()


    create_and_insert_output_file(final_outcome_content, output_file_path)
    print(f"Output file created: {output_file_path}")
