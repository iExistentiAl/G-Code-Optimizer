# W = 3 mm 
# d = 3 mm orange , 1 mm white
# length of the lines
# layer height = 1.6


import re
import math

def calculate_extrusion_rate(w, h, D, L):
    return (4 * w * h * L) / (math.pi * D ** 2)

def update_gcode(input_file, output_file, w=3, h=1.6, D=5):
    with open(input_file, 'r') as f:
        gcode_lines = f.readlines()

    updated_gcode_lines = []
    total_extrusion = 0
    last_position = None

    for line in gcode_lines:
        if line.startswith("G1"):
            match = re.search(r'X([\d.]+) Y([\d.]+) E([\d.-]+)', line)
            if match:
                x = float(match.group(1))
                y = float(match.group(2))
                extrusion = abs(float(match.group(3)))  # Convert negative extrusion to positive
                if last_position is not None:
                    distance = math.sqrt((x - last_position[0]) ** 2 + (y - last_position[1]) ** 2)
                    extrusion_rate = calculate_extrusion_rate(w, h, D, distance)
                    total_extrusion += extrusion_rate
                    print(f"Distance: {distance}, Extrusion Rate: {extrusion_rate}, Total Extrusion: {total_extrusion}")
                line = re.sub(r'E[\d.-]+', f'E{total_extrusion:.5f}', line)
                last_position = (x, y)

        updated_gcode_lines.append(line)

    with open(output_file, 'w') as f:
        f.writelines(updated_gcode_lines)

# Example usage
input_file = 'extrusionRateTry.txt'
output_file = 'output.gcode'
update_gcode(input_file, output_file)



