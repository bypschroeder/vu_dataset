import bpy
import math
import os
import random
import gc
from pathlib import Path


def clear_scene():
    """
    Clears the current scene of all objects.
    """
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    for collection in bpy.data.collections:
        if collection.name == "Collection":
            bpy.data.collections.remove(collection)


def setup_scene(camera_location, camera_rotation, light_rotation):
    """Sets up the scene with a camera and light.

    Args:
        camera_location (tuple): The location of the camera. Must be a tuple of x, y, and z coordinates.
        camera_rotation (tuple): The rotation of the camera. Must be a tuple of x, y, and z angles in degrees.
        light_rotation (tuple): The rotation of the light. Must be a tuple of x, y, and z angles in degrees.
    """
    c_rotation = tuple(math.radians(angle) for angle in camera_rotation)
    l_rotation = tuple(math.radians(angle) for angle in light_rotation)

    bpy.ops.object.camera_add(location=camera_location, rotation=c_rotation)
    camera = bpy.context.object
    light = bpy.ops.object.light_add(
        type="SUN", radius=10, location=(0, 0, 0), rotation=l_rotation
    )
    light = bpy.context.object

    return camera, light


def apply_all_transforms(obj):
    """Applies all transformations to an object.

    Args:
        obj (bpy.types.Object): The object to apply all transformations to.
    """
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")

    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def scale_obj(obj, scale_factor):
    """Scales an object by a given factor.

    Args:
        obj (bpy.types.Object): The object to scale.
        scale_factor (float): The factor by which to scale the object.
    """
    obj.scale = (scale_factor, scale_factor, scale_factor)

    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")

    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def add_object(filepath, name):
    """Adds an object from a blend file to the current scene.

    Args:
        filepath (str): The path to the blend file.
        name (str): The name of the object to add.

    Raises:
        FileNotFoundError: If the blend file is not found.
        ValueError: If the object is not found.

    Returns:
        bpy.types.Object: The added object.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} not found.")

    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        if name in data_from.objects:
            data_to.objects.append(name)

    obj = bpy.data.objects.get(name)

    if obj:
        bpy.context.collection.objects.link(obj)
        print(f"{name} was appended")
    else:
        raise ValueError(f"Object {name} not found")

    return obj


def set_color(obj, color):
    """Sets the color of an object.

    Args:
        obj (bpy.types.Object): The object to set the color for.
        color (str): The color in Hex format.

    Raises:
        ValueError: If the color is not in Hex format.
    """
    if not color.startswith("#"):
        raise ValueError("Color must be in Hex format")

    if not obj.data.materials:
        mat = bpy.data.materials.new(name="Material")
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]

    if not mat.use_nodes:
        mat.use_nodes = True

    nodes = mat.node_tree.nodes

    bsdf = nodes.get("Principled BSDF")
    if not bsdf:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        output = nodes.get("Material Output")
        if output:
            mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

    color = color.lstrip("#")
    rgb = tuple(int(color[i : i + 2], 16) / 255 for i in (0, 2, 4))
    bsdf.inputs["Base Color"].default_value = (*rgb, 1)


def get_random_blend_file(folder_path):
    """Gets the path of a random blend file from the specified folder_path.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        str: The path to the blend file.
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

def cleanup():
    bpy.ops.outliner.orphans_purge(
        do_recursive=True, do_linked_ids=True, do_local_ids=True
    )
    bpy.ops.ptcache.free_bake_all()
    gc.collect()