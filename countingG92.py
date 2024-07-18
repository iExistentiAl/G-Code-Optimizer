import re

def G92_count(file_path):
    groups = []
    current_group = None
    last_t_value = None
    last_z_value = None

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line_number, line in enumerate(lines, 1):
        if 'G92 E0' in line:
            if current_group:
                current_group['end_line_no'] = line_number - 1
                groups.append(current_group)

            current_group = {'start_line_no': line_number, 'coordinates': [], 'z_level': None}

            # Search for the T value within a specified range of lines around the 'G92 E0' command
            t_in_vicinity = False
            for j in range(max(line_number - 5, 0), min(line_number + 6, len(lines))):
                if lines[j].startswith("T0") or lines[j].startswith("T1"):
                    # Extract the T value from the line
                    t_match = re.search(r'T(\d+)', lines[j])
                    if t_match:
                        current_group['t_value'] = t_match.group(0)  # Include the 'T' value
                    else:
                        current_group['t_value'] = last_t_value
                    t_in_vicinity = True
                    break

            # If the T value is not found in the vicinity, use the last known T value
            if not t_in_vicinity:
                current_group['t_value'] = last_t_value

        elif line.startswith("T0") or line.startswith("T1"):
            last_t_value = line.strip()

        # Store the Z value of the group
        elif current_group:
            if 'Z' in line:
                z_coord = float(re.search(r'Z([\d.]+)', line).group(1))
                if z_coord != last_z_value:
                    current_group['z_level'] = z_coord
                    last_z_value = z_coord

            # Storing the coordinates 
            elif line.startswith('G1 X') and 'Y' in line:
                x_coord = float(re.search(r'X([\d.]+)', line).group(1))
                y_coord = float(re.search(r'Y([\d.]+)', line).group(1))
                current_group['coordinates'].append((x_coord, y_coord))

    if current_group:
        current_group['end_line_no'] = len(lines)
        groups.append(current_group)

    return groups

# if __name__ == "__main__":
#     groups = G92_count("output.txt")

#     for idx, group in enumerate(groups, 1):
#         t_value = group['t_value']
#         coordinates = group['coordinates']
#         z_level = group['z_level'] if group['z_level'] is not None else ''

#         start_line_no = group['start_line_no']
#         end_line_no = group['end_line_no']

#         print(f"{t_value} Group {idx} (Lines {start_line_no}-{end_line_no})" +
#               (f" Start: X {coordinates[0][0]:.3f} Y {coordinates[0][1]:.3f}" if coordinates else "") +
#               (f" End: X {coordinates[-1][0]:.3f} Y {coordinates[-1][1]:.3f}" if coordinates else "") +
#               (f" Z {z_level}" if z_level or z_level else ""))