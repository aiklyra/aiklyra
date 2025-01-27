import os
from functools import reduce  # Import reduce from functools

def get_directory_structure(rootdir):
    """Returns a nested dictionary that represents the folder structure of rootdir."""
    structure = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], structure)
        parent[folders[-1]] = subdir
    return structure

def write_structure_to_file(file, structure, indent=0):
    """Writes the directory structure to the file."""
    for key, value in structure.items():
        file.write(' ' * indent + str(key) + '\n')
        if isinstance(value, dict):
            write_structure_to_file(file, value, indent + 4)

def write_file_contents(file, rootdir):
    """Writes the contents of all .py files in rootdir to the file."""
    for path, _, files in os.walk(rootdir):
        for name in files:
            if name.endswith('.py'):
                file_path = os.path.join(path, name)
                file.write(f'\nContents of {file_path}:\n')
                with open(file_path, 'r') as f:
                    file.write(f.read())
                file.write('\n')

def main(dir1, dir2, output_file):
    with open(output_file, 'w') as file:
        # Write the structure of the first directory
        file.write(f'Structure of {dir1}:\n')
        structure1 = get_directory_structure(dir1)
        write_structure_to_file(file, structure1)
        
        # Write the structure of the second directory
        file.write(f'\nStructure of {dir2}:\n')
        structure2 = get_directory_structure(dir2)
        write_structure_to_file(file, structure2)
        
        # Write the contents of .py files from the first directory
        file.write(f'\nContents of .py files in {dir1}:\n')
        write_file_contents(file, dir1)
        
        # Write the contents of .py files from the second directory
        file.write(f'\nContents of .py files in {dir2}:\n')
        write_file_contents(file, dir2)

if __name__ == "__main__":
    dir1 = 'aiklyra'
    dir2 = 'tests'
    output_file = 'output.txt'
    main(dir1, dir2, output_file)