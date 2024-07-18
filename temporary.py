import os

# Creating a temporary file, to do all the actions through it
def create_file(file_name):
    file_path = os.path.join(file_name)

    # Create an empty file
    with open(file_path, 'w') as new_file:
        pass  # This line is optional, you can write something to the file if needed

    print(f"File '{file_name}' created!")

# You can use this to delete it right after all the actions were done and temporary file is not needed
# But I didnt use it, because did a lot of debugging
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} deleted successfully.")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


