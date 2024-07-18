import re

def extract_coordinates(line):
    # Try to match the regular format (e.g., (123, 456))
    match_regular = re.match(r'\((\d+), (\d+)\)', line)
    if match_regular:
        return tuple(map(int, match_regular.groups()))

    # Try to match the "Start Y" format (e.g., Start Y: 62.533, End Y: 86.304 (8, 304))
    match_start_y = re.match(r'Start Y: (\d+\.\d+), End Y: (\d+\.\d+)( \((\d+), (\d+)\))?(, X)?', line)
    if match_start_y:
        if match_start_y.groups()[2]:  # Check if the line contains group numbers in parentheses
            return tuple(map(float, match_start_y.groups()[3:5])) + (', X' in line,)
        else:
            return tuple(map(float, match_start_y.groups()[0:2])) + (', X' in line,)

    # If no match is found, return None
    return None

def calculate_positions(input_file_path):
    try:
        with open(input_file_path, "r") as input_file:
            lines = [extract_coordinates(line) for line in input_file]

        output_lines = []
        current_start_position = lines[0][0] if lines and len(lines[0]) > 0 else 0
        for coordinates in lines:
            if coordinates and len(coordinates) >= 2:
                start_line, end_line = coordinates[:2]
                chunk_length = end_line - start_line
                current_end_position = current_start_position + chunk_length + 1
                output_lines.append((current_start_position, current_end_position, coordinates[2]))
                current_start_position = current_end_position + 1

        with open(input_file_path, "r") as input_file:
            content = input_file.readlines()

        with open(input_file_path, "w") as output_file:
            for i, (line, positions) in enumerate(zip(content, output_lines), start=1):
                start, end, is_x = positions
                x_marker = ', X' if is_x else ''
                print(f"{line.strip()} {int(start)} {int(end)}{x_marker}", file=output_file)

        return output_lines
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
input_file_path = "rearranged_output.txt"  # Replace with the actual path to your input file
positions = calculate_positions(input_file_path)

# Print or process the calculated positions
for i, (start, end, is_x) in enumerate(positions, start=1):
    x_marker = ', X' if is_x else ''
    print(f"Line {int(i)}: Start position: {int(start)}, End position: {int(end)}{x_marker}")
