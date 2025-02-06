import bpy
import os
import json
import pickle


def export_to_obj(output_path, garment=None, avatar=None):
    """Exports the current scene to an OBJ file.

    Args:
        output_path (str): The path to the output file.
        garment (bpy.types.Object, optional): The garment object to export. Defaults to None.
        avatar (bpy.types.Object, optional): The avatar object to export. Defaults to None.

    Notes:
        Only exports the selected objects which are given as garment or avatar.
    """
    bpy.ops.object.select_all(action="DESELECT")

    if garment is not None:
        garment.select_set(True)

    if avatar is not None:
        avatar.select_set(True)

    bpy.ops.wm.obj_export(
        export_selected_objects=True, filepath=output_path, export_materials=True
    )


def save_export_info(height, weight, gender, garment, size, output_path):
    """Saves the export information to a JSON file.

    Args:
        height (float): The height of the avatar.
        weight (float): The weight of the avatar.
        gender (str): The gender of the avatar.
        garment (str): The name of the garment.
        size (str): The size of the garment.
        output_path (str): The path to the output directory.
    """
    export_info = {
        "height": height,
        "weight": weight,
        "gender": gender,
        "garment": garment,
        "size": size,
    }
    with open(
        os.path.join(output_path, "export_info.json"),
        "w",
    ) as f:
        json.dump(export_info, f)


def save_pose(pose_dict, output_path):
    """Saves the pose to a pickle file.

    Args:
        pose_dict (dict): The pose dictionary.
        output_path (str): The path to the output directory.
    """
    with open(
        os.path.join(output_path, "pose.pkl"),
        "wb",
    ) as f:
        pickle.dump(pose_dict, f)