import sys
import os

def get_relative_path(relative_path):
    """
    Returns the absolute path to a file relative to the project base directory.

    :param relative_path: The relative path to the file.
    :type relative_path: str
    :return: The absolute path to the file.
    :rtype: str
    """
    project_base_dir = os.path.dirname(os.path.abspath(__file__)) 
    project_base_dir = os.path.abspath(os.path.join(project_base_dir, "..")) 

    return os.path.join(project_base_dir, *relative_path.split('/'))