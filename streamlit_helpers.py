import os


def get_directories(dir_name):
    # Get list of all directories in the given directory
    return [f.path for f in os.scandir(dir_name) if f.is_dir()]


def get_png_files(dir_name):
    # Get list of all files in the given directory
    files = os.listdir(dir_name)
    # Filter out all PNG files
    png_files = [f for f in files if f.endswith(".png")]
    return png_files
