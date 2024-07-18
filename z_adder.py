temp_file = "1_temp.txt"

def z_adder():
    with open(temp_file, 'r') as file:
        lines = file.readlines()

    previous_t_value = None
    updated_lines = []

    for line in lines:
        if line.startswith('T'):
            current_t_value = line.split(' ')[0]
            if previous_t_value == 'T0' and current_t_value == 'T1':
                updated_lines[-1] = updated_lines[-2].strip() + f' Z 1.5\n'  # Add Z at the end of the line above
            elif previous_t_value == 'T1' and current_t_value == 'T0':
                updated_lines[-1] = updated_lines[-2].strip() + f' Z 1.5\n'  # Add Z at the end of the line above

            previous_t_value = current_t_value

        updated_lines.append(line)

    with open(temp_file, 'w') as file:
        file.writelines(updated_lines)

# Example usage:
z_adder()
