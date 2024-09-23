import os
import sys
import shutil

def get_resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource, handling the case where the app
    is run from a bundled executable (PyInstaller) or directly from source.
    
    :param relative_path: The relative path to the resource (file or folder).
    :return: The absolute path to the resource.
    """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def create_directory(path: str) -> bool:
    """
    Create a directory at the specified path if it does not exist.
    
    :param path: The path to the directory to create.
    :return: True if the directory was created, False if it already exists.
    """
    abs_path = get_resource_path(path)
    try:
        os.makedirs(abs_path, exist_ok=True)
        return True
    except OSError as e:
        print(f"Error creating directory {abs_path}: {e}")
        return False

def delete_directory(path: str) -> bool:
    """
    Delete a directory and all its contents at the specified path.
    
    :param path: The path to the directory to delete.
    :return: True if the directory was deleted, False otherwise.
    """
    abs_path = get_resource_path(path)
    try:
        shutil.rmtree(abs_path)
        return True
    except OSError as e:
        print(f"Error deleting directory {abs_path}: {e}")
        return False

def create_file(path: str, content: str = "") -> bool:
    """
    Create a file with the specified content at the given path. If the file
    or its directories don't exist, they are created.
    
    :param path: The path to the file.
    :param content: The content to write to the file.
    :return: True if the file was created, False otherwise.
    """
    abs_path = get_resource_path(path)
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        # Write content to the file
        with open(abs_path, 'w') as file:
            file.write(content)
        return True
    except OSError as e:
        print(f"Error creating file {abs_path}: {e}")
        return False

def delete_file(path: str) -> bool:
    """
    Delete a file at the specified path.
    
    :param path: The path to the file to delete.
    :return: True if the file was deleted, False otherwise.
    """
    abs_path = get_resource_path(path)
    try:
        os.remove(abs_path)
        return True
    except FileNotFoundError:
        print(f"File {abs_path} not found.")
        return False
    except OSError as e:
        print(f"Error deleting file {abs_path}: {e}")
        return False
