import bpy

def export_to_obj(filepath):
    """
    Exports the current scene to an OBJ file.

    :param filepath: The path to the output file.
    :type filepath: str
    """
    bpy.ops.object.select_all(action='DESELECT')

    prefixes = ("XS_", "S_", "M_", "L_", "XL_", "XXL_")

    for obj in bpy.data.objects:
        if obj.type == "MESH" and obj.name.startswith(prefixes):
            obj.select_set(True)

    bpy.ops.wm.obj_export(export_selected_objects=True, filepath=filepath)

def export_to_fbx(filepath):
    """
    Exports the current scene to an FBX file.

    :param filepath: The path to the output file.
    :type filepath: str
    """
    bpy.ops.object.select_all(action='DESELECT')

    for obj in bpy.data.objects:
        if obj.type == "MESH" or obj.type == "ARMATURE":
            obj.select_set(True)

    bpy.ops.export_scene.fbx(filepath=filepath)

def export_to_glb(filepath):
    """
    Exports the current scene to an GLB file.

    :param filepath: The path to the output file.
    :type filepath: str
    """
    bpy.ops.object.select_all(action='DESELECT')

    for obj in bpy.data.objects:
        if obj.type == "MESH" or obj.type == "ARMATURE":
            obj.select_set(True)

    bpy.ops.export_scene.gltf(filepath=filepath)