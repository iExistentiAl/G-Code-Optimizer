# This file is what Ive tried to do, but didnt achieve the right result
# Here Im trying to rearrange the groups so the print will be OWOWOWOWO
# O - Orange W - White 
# But this didnt work out, and needs more time and debugging, but maybe you will be able to solve it
# So far it rearranges groups in a right way, but when its time to insert all the groups into the final file, it just prints nothing for some reason

# Reorders groups T1 T0 T1 T0
def reorder_groups(input_file_path):
    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()

    # Extracting groups from the file
    groups = []
    current_group = None
    for line in lines:
        if line.startswith("Group"):
            if current_group:
                groups.append(current_group)
            current_group = {"header": line.strip(), "Start X": []}
        elif line.startswith("Start X"):
            current_group["Start X"].append(line.strip())

    if current_group:
        groups.append(current_group)

    # Separate groups into T0 and T1 groups
    t0_groups = [group for group in groups if group["header"].split(", ")[1] == "T0"]
    t1_groups = [group for group in groups if group["header"].split(", ")[1] == "T1"]

    # Reorder groups to alternate between T0 and T1
    reordered_groups = []
    for t0_group, t1_group in zip(t0_groups, t1_groups):
        reordered_groups.append(t0_group)
        reordered_groups.append(t1_group)

    # If there are remaining groups, append them at the end
    if len(t0_groups) > len(t1_groups):
        reordered_groups.extend(t0_groups[len(t1_groups):])
    elif len(t1_groups) > len(t0_groups):
        reordered_groups.extend(t1_groups[len(t0_groups):])

    # Writing the reordered groups back to the file
    with open(input_file_path, 'w') as output_file:
        for group in reordered_groups:
            output_file.write(group["header"] + ":\n")
            if group["Start X"]:  # Check if there are values to append
                for part in group["Start X"]:
                    output_file.write("" + part + "\n")

    print("Reordering Groups")


# Deletes Group lines, to allow another algorithm to work
def delete_group_lines(input_file_path):
    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()

    # Filter out lines starting with "Group"
    filtered_lines = [line for line in lines if not line.strip().startswith("Group ")]

    # Write the filtered lines back to the file
    with open(input_file_path, 'w') as output_file:
        output_file.writelines(filtered_lines)


if __name__ == "__main__":
    input_file_path = "rearranged_output.txt"
    reorder_groups(input_file_path)
    delete_group_lines(input_file_path)

    
    