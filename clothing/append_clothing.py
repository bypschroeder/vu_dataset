import bpy
import os
import random
from pathlib import Path

from clothing.modifiers import set_cloth_material, shrink_waistband

# Map the clothing base names to the clothing materials
clothing_material_map = {
    "T-Shirt": "t-shirt",
    "Sweater": "sweater",
    "Hoodie": "hoodie",
    "Pants": "pants",
    "Shorts": "shorts",
}

def append_object(filepath, object_name):
    """
    Appends an object from a blend file to the current scene.

    :param filepath: The path to the blend file.
    :type filepath: str
    :param object_name: The name of the object to append.
    :type object_name: str
    :return: The appended object.
    :rtype: bpy.types.Object
    """
    with bpy.data.libraries.load(filepath=filepath, link=False) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects.append(object_name)
    
    obj = bpy.data.objects.get(object_name)

    if obj:
        bpy.context.collection.objects.link(obj)
        obj.select_set(True)

        print(f"{object_name} was appended")
    else:
        print(f"{object_name} could not be found")

    return obj

def get_random_blend_file(folder_path):
    """
    Returns a random blend file from the specified folder.

    :param folder_path: The path to the folder.
    :type folder_path: str
    :return: The path to the blend file.
    :rtype: str
    """

    blend_files = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, file)) and file.endswith(".blend")
    ]

    if not blend_files:
        print("No blend files found")
        return None
    
    base_dir = Path(__file__).parent.parent
    file = random.choice(blend_files)

    return os.path.join(base_dir, file)

def get_object_name_from_filepath(filepath):
    """
    Returns the name of the object from the filepath.

    :param filepath: The path to the blend file.
    :type filepath: str
    :return: The name of the object.
    :rtype: str
    """
    filename_with_extension = os.path.basename(filepath)

    object_name = os.path.splitext(filename_with_extension)

    return object_name[0]

def append_random_top(folder_path, gender):
    """
    Appends a random top to the scene.
    """
    top_path = get_random_blend_file(f"{folder_path}/{gender}")

    if top_path:
        top_obj = append_object(top_path, get_object_name_from_filepath(top_path))
        top_base_name = top_obj.name.split("_", 1)[-1]
        if top_base_name in clothing_material_map:
            set_cloth_material(top_obj, clothing_material_map[top_base_name])

        garment_name = os.path.basename(top_path).split(".")[0]
        return garment_name, top_obj

def append_random_bottom(z_offset, frame_start, frame_end, folder_path, gender):
    """
    Appends a random bottom to the scene.
    """
    bottom_path = get_random_blend_file(f"{folder_path}/{gender}")

    if bottom_path:
        bottom_obj = append_object(bottom_path, get_object_name_from_filepath(bottom_path))

        shrink_waistband(bottom_obj, bpy.data.objects[f"SMPLX-mesh-{gender}"])

        bottom_obj.keyframe_insert(data_path="location", frame=frame_start, index=2)

        bottom_obj.location.z += z_offset
        bottom_obj.keyframe_insert(data_path="location", frame=frame_end, index=2)

        bottom_base_name = bottom_obj.name.split("_", 1)[-1]
        if bottom_base_name in clothing_material_map:
            set_cloth_material(bottom_obj, clothing_material_map[bottom_base_name])

        garment_name = os.path.basename(bottom_path).split(".")[0]
        return garment_name, bottom_obj