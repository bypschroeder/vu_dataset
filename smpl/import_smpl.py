import bpy
import random
import os

from _helpers.path import get_relative_path
from smpl.create_pose import generate_random_pose
from clothing.modifiers import add_collision_modifier

def import_smplx_model(gender="neutral"):
    """
    Imports the SMPLX model into the scene.

    :param gender: The gender of the model to import.
    :type gender: str
    """

    if gender not in ['neutral', 'male', 'female']:
        raise ValueError("Invalid gender")
    
    if "smplx_blender_addon" not in bpy.context.preferences.addons:
        raise ValueError("Please install smplx addon") 
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.window_managers["WinMan"].smplx_tool.smplx_gender = gender
    bpy.ops.scene.smplx_add_gender()

    bpy.ops.object.select_all(action='DESELECT')
    armature = bpy.data.objects.get(f"SMPLX-{gender}")
    armature.select_set(True)

    bpy.context.view_layer.objects.active = armature
    
    armature.scale = (10, 10, 10) 

def load_pose(path):
    """
    Loads a pose file into the SMPLX model.

    :param path: The path to the pose file.
    :type path: str
    """

    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.smplx_load_pose(filepath=path)

def set_height_weight(height, weight, gender):
    """
    Sets the height and weight of the SMPLX model.

    :param height: The height of the model.
    :type height: float
    :param weight: The weight of the model.
    :type weight: float
    :param gender: The gender of the model.
    :type gender: str
    """

    bpy.data.window_managers["WinMan"].smplx_tool.smplx_height = height
    bpy.data.window_managers["WinMan"].smplx_tool.smplx_weight = weight

    bpy.ops.object.select_all(action="DESELECT")
    mesh = bpy.data.objects.get(f"SMPLX-mesh-{gender}")
    mesh.select_set(True)
    bpy.context.view_layer.objects.active = mesh
    
    bpy.ops.object.smplx_measurements_to_shape()
    bpy.ops.object.smplx_snap_ground_plane()

    add_collision_modifier(mesh)

def get_random_gender():
    """
    Returns a random gender.

    :return: The random gender.
    :rtype: str
    """

    genders = ["neutral", "male", "female"]

    return random.choice(genders)

def get_random_height(gender):
    """
    Returns a random height for the SMPLX model.

    :param gender: The gender of the model.
    :type gender: str
    :return: The random height.
    :rtype: float
    """

    if gender == "female":
        height = random.triangular(1.4, 1.75, 2.0)
    else:
        height = random.uniform(1.5, 2.2)

    return round(height, 2)

def get_random_weight(height):
    """
    Returns a random weight for the SMPLX model.

    :param height: The height of the model.
    :type height: float
    :return: The random weight.
    :rtype: float
    """

    mean_weight = 22 * (height ** 2)
    std_dev = 5

    weight = random.gauss(mean_weight, std_dev)

    weight = max(40.0, min(weight, 110.0))

    return round(weight, 2)

def set_keyframe_bones(armature, frame):
    """
    Sets a keyframe for the location and rotation of each bone of the armature to the given frame.

    :param armature: The name of the armature.
    :type armature: str
    :param frame: The frame to set the keyframes at.
    :type frame: int
    """
    armature = bpy.data.objects.get(armature)

    if armature is None or armature.type != 'ARMATURE':
        print("Armature not found")
        return

    for bone in armature.pose.bones:
        bone.keyframe_insert(data_path="location", frame=frame)
        bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)


def set_keyframe_armature_location(armature, frame):
    """
    Sets a keyframe for the location of the armature to the given frame.

    :param armature: The name of the armature.
    :type armature: str
    :param frame: The frame to set the keyframe at.
    :type frame: int
    """
    
    armature = bpy.data.objects.get(armature)

    if armature is None or armature.type != 'ARMATURE':
        print("Armature not found")
        return

    bpy.ops.object.smplx_snap_ground_plane()
    armature.keyframe_insert(data_path="location", frame=frame)

def set_keyframe_shape_keys(mesh_name, frame):
    """
    Sets keyframes of all shape keys of the mesh to the given frame.

    :param mesh_name: The name of the mesh.
    :type mesh_name: str
    :param frame: The frame to set the keyframes at.
    :type frame: int
    """

    mesh = bpy.data.objects.get(mesh_name)

    if not mesh:
        print(f"Mesh {mesh_name} not found")
        return
    
    if not mesh.data.shape_keys:
        print(f"Mesh {mesh_name} has no shape keys")
        return
    
    for shape_key in mesh.data.shape_keys.key_blocks:
        shape_key.keyframe_insert(data_path="value", frame=frame)

def create_random_smplx_model(randomize_pose="true"):
    """
    Creates a random smplx_model with a random gender, height, weight and pose. Also sets the keyframes for the animation.

    :param randomize_pose: Whether to randomize the pose or not.
    :type randomize_pose: boolean
    :return: gender, height, weight
    :rtype: string, float, float
    """
    gender = "male" # get_random_gender()
    height = get_random_height(gender)
    weight = get_random_weight(height)
    print(f"Height: {height}, Weight: {weight}")

    import_smplx_model(gender)

    bpy.ops.object.smplx_snap_ground_plane()

    start_frame = 10

    end_frame = 40

    set_keyframe_bones(f"SMPLX-{gender}", start_frame)
    set_keyframe_armature_location(f"SMPLX-{gender}", start_frame)
    set_keyframe_shape_keys(f"SMPLX-mesh-{gender}", start_frame)
    
    if randomize_pose:
        pose_path = generate_random_pose(get_relative_path("/smpl/random_pose.pkl"))
        load_pose(pose_path)
        print("Loaded pose")

        set_keyframe_bones(f"SMPLX-{gender}", end_frame)
        bpy.context.scene.frame_set(end_frame)
        set_height_weight(height, weight, gender)
        set_keyframe_shape_keys(f"SMPLX-mesh-{gender}", end_frame)
        set_keyframe_armature_location(f"SMPLX-{gender}", end_frame)

    armature = bpy.data.objects[f"SMPLX-{gender}"]
    fcurves = armature.animation_data.action.fcurves

    z_offset = None
    for fcurve in fcurves:
        if fcurve.data_path == "location" and fcurve.array_index == 2:  # Z-axis location
            keyframe_points = fcurve.keyframe_points
            z_start = keyframe_points[0].co[1]  # Z value at the start keyframe
            z_end = keyframe_points[1].co[1]    # Z value at the end keyframe
            z_offset = z_end - z_start
            break

    if z_offset is None:
        raise ValueError("Z-offset could not be calculated. Ensure keyframes are properly set.")

    return gender, height, weight, z_offset