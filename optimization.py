import re
import math

# This function is going through a 1_temp file, and rearranges it based on their start and end coordinates
def find_lines_with_XY(input_file_path, output_file_path=None):
    group_list = []
    current_group = None
    is_group = False
    first_start_line = None
    last_part_was_flipped = False  # Track if the last part was marked as "XY" (XY is a mark that the line was flipped)

    with open(input_file_path, "r") as input_file:
        # Iterate through all lines
        for i, line in enumerate(input_file, start=1):  # Start counting line numbers from 1
            # Extracting line numbers from the input line (handling ranges)
            line_numbers_str = (line.split("Lines ")[1].split(")")[0]) if "Lines" in line else None
            line_numbers = [int(num) for num in line_numbers_str.replace('-', ',').split(',')] if line_numbers_str else None

            group_number = int(line.split("Group ")[1].split(" ")[0]) if "Group" in line else None
            t_value = int(re.search(r'T(\d+)', line).group(1)) if re.search(r'T(\d+)', line) else None
            z_value = float(re.search(r'Z\s*([\d.]+)', line).group(1)) if "Z" in line else None
            
            # Check if the line contains "Z"
            if "Z" in line:
                is_group = True
                if current_group:
                    group_list.append(current_group)
                if "Start: X" in line:
                    start_x_match = re.search(r'X\s*([\d.]+)', line)
                    end_x_match = re.search(r'End: X\s*([\d.]+)', line)
                    start_x = float(start_x_match.group(1))
                    end_x = float(end_x_match.group(1))
                    start_y_match = re.search(r'Y\s*([\d.]+)', line)
                    end_y_match = re.search(r'End:\s*X\s*[\d.]+\s*Y\s*([\d.]+)', line)
                    start_y = float(start_y_match.group(1))
                    end_y = float(end_y_match.group(1)) if end_y_match else start_y
                else:
                    start_x = end_x = start_y = end_y = None
                if first_start_line is None:
                    first_start_line = int(line.split("Lines ")[1].split("-")[0]) if "Lines" in line else None
                current_group = {"line_numbers": line_numbers, "t_value": t_value, "z_value": z_value, "start_end_coordinates": [((start_x, end_x, start_y, end_y), line_numbers, group_number, first_start_line)]}
                last_part_was_flipped = False  # Reset the flag for each new group
            
            elif is_group and ("X" not in line and "Y" not in line):
                is_group = False
                if current_group["line_numbers"]:
                    group_list.append(current_group)
                current_group = {"line_numbers": [], "t_value": None, "z_value": None, "start_end_coordinates": []}
            
            elif is_group and ("Start: X" in line and "End: X" in line) or ("Start: Y" in line and "End: Y" in line):
                start_x_match = re.search(r'X\s*([\d.]+)', line)
                end_x_match = re.search(r'End: X\s*([\d.]+)', line)
                start_x = float(start_x_match.group(1))
                end_x = float(end_x_match.group(1))
                start_y_match = re.search(r'Y\s*([\d.]+)', line)
                end_y_match = re.search(r'End:\s*X\s*[\d.]+\s*Y\s*([\d.]+)', line)
                start_y = float(start_y_match.group(1))
                end_y = float(end_y_match.group(1)) if end_y_match else start_y
                
                # Check if the last part was marked as "XY"
                if not last_part_was_flipped:
                    current_group["start_end_coordinates"].append(((start_x, end_x, start_y, end_y), line_numbers, group_number, first_start_line))
                    if "XY" in line_numbers:
                        last_part_was_flipped = True
                else:
                    last_part_was_flipped = False

        # Adding the last group if any
        if current_group and current_group["line_numbers"]:
            group_list.append(current_group)

    # Rearranging lines within each group based on the proximity of End X and End Y to the Start X and Start Y of the next part
    for group in group_list:
        if len(group["start_end_coordinates"]) > 1:
            sorted_parts = [group["start_end_coordinates"][0]]  # Start with the first part
            for i in range(len(group["start_end_coordinates"]) - 1):
                current_start_x, current_end_x, current_start_y, current_end_y = sorted_parts[-1][0]

                # Finding the closest part based on Euclidean distance to both the current End X, End Y, Start X, and Start Y
                next_part = min(
                    (part for part in group["start_end_coordinates"] if part not in sorted_parts),
                    key=lambda x: min(
                        math.dist((current_end_x, current_end_y), (x[0][0], x[0][2])),
                        math.dist((current_end_x, current_end_y), (x[0][1], x[0][3])),
                        math.dist((current_start_x, current_start_y), (x[0][0], x[0][2])),
                        math.dist((current_start_x, current_start_y), (x[0][1], x[0][3]))
                    )
                )

                # Marking the part that is closest to the end and start values
                if (
                    math.dist((current_end_x, current_end_y), (next_part[0][1], next_part[0][3])) <
                    math.dist((current_end_x, current_end_y), (next_part[0][0], next_part[0][2]))
                ):
                    next_part[1].append("XY")

                sorted_parts.append(next_part)

            # Replacing the unsorted parts with the rearranged parts
            group["start_end_coordinates"] = sorted_parts

    # Preparing the output content
    output_content = []
    for i, group in enumerate(group_list, start=1):
        group_output = []
        group_output.append(f"Group {i}, T{group['t_value']}, Z{group['z_value']}:")
        for (start_x, end_x, start_y, end_y), line_numbers, group_number, first_start_line in group["start_end_coordinates"]:
            # Adjusting coordinates for flipped parts
            if "XY" in line_numbers:
                start_x, end_x, start_y, end_y = end_x, start_x, end_y, start_y

            if first_start_line is not None:
                group_output.append(f"Start X: {start_x:.3f}, End X: {end_x:.3f}, Start Y: {start_y:.3f}, End Y: {end_y:.3f} ({', '.join(map(str, line_numbers))})")
                # Updating first_start_line for the next iteration
                first_start_line += len(group["start_end_coordinates"])
            else:
                group_output.append(f"Start X: {start_x:.3f}, End X: {end_x:.3f}, Start Y: {start_y:.3f}, End Y: {end_y:.3f} ({', '.join(map(str, line_numbers))})")

        output_content.extend(group_output)

    # Saving to the output file if provided
    if output_file_path:
        with open(output_file_path, "w") as output_file:
            output_file.write('\n'.join(output_content))

    return group_list

# This function was made just to make the optimization work properly
def remove_xy_from_previous_line_in_place(file_path):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)

        previous_line_had_xy = False

        for line in lines:
            if previous_line_had_xy and "XY" in line:
                line = line.replace(", XY", "")
            file.write(line)

            # Updating the variable for the next iteration
            previous_line_had_xy = "XY" in line

        file.truncate()

if __name__ == "__main__":
    input_file_path = "1_temp.txt"
    output_file_path = "rearranged_output.txt"
    find_lines_with_XY(input_file_path, output_file_path)
    remove_xy_from_previous_line_in_place(output_file_path)
