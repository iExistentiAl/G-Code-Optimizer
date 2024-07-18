import math
import re

# This is a calculation of the Extrusion rate
def calculate_extrusion_rate(w, h, D, L):
    return (4 * w * h * L) / (math.pi * D ** 2)

# This function updates all the extrusion rates in the gcode, so the flipped lines appear properly
def update_gcode_with_extrusion(gcode_lines, w=3, h=1.6, D_T0=3, D_T1=5):
    updated_gcode_lines = []
    total_extrusion = 0
    last_position = None
    current_D = D_T0  # Start with D_T0 by default

    for line in gcode_lines:
        if line.startswith("G1"):
            match = re.search(r'X([\d.]+) Y([\d.]+) E([\d.-]+)', line)
            if match:
                x = float(match.group(1))
                y = float(match.group(2))
                extrusion = abs(float(match.group(3)))  # Convert negative extrusion to positive
                if last_position is not None:
                    distance = math.sqrt((x - last_position[0]) ** 2 + (y - last_position[1]) ** 2)
                    extrusion_rate = calculate_extrusion_rate(w, h, current_D, distance)
                    total_extrusion += extrusion_rate
                line = re.sub(r'E[\d.-]+', f'E{total_extrusion:.5f}', line)
                last_position = (x, y)
        elif line.startswith("G92"):
            total_extrusion = 0  # Reset total extrusion when encountering G92 command
            last_position = None  # Reset last position as well
        elif line.startswith("T0"):
            current_D = D_T0  # Switch to D_T0 when encountering T0
            last_position = None  # Reset last position as well
            total_extrusion = 0
        elif line.startswith("T1"):
            last_position = None  # Reset last position as well
            current_D = D_T1  # Switch to D_T1 when encountering T1
            total_extrusion = 0

        updated_gcode_lines.append(line)

    return updated_gcode_lines