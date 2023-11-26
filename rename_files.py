import os
def rename_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.php'):  # What to change
            name, ext = os.path.splitext(filename)
            new_name = name + '.txt'  # With what to change
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
            print(f"Renamed '{filename}' to '{new_name}'")

directory_path = os.path.dirname(os.path.abspath(__file__))
rename_files(directory_path)
