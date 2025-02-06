import bpy
import random
import bmesh


def import_smplx_model(gender="male"):
    """Imports the SMPLX model in the given gender.

    Args:
        gender (str, optional): The gender of the model. Defaults to "male".

    Raises:
        ValueError: If the gender is not "male" or "female".
        ValueError: If the smplx addon is not installed.

    Returns:
        bpy.types.Object: The armature object.
        bpy.types.Object: The mesh object.
    """
    if gender not in ["male", "female"]:
        raise ValueError("Invalid gender")

    if "smplx_blender_addon" not in bpy.context.preferences.addons:
        raise ValueError("Please install smplx addon")

    bpy.ops.object.select_all(action="DESELECT")
    bpy.data.window_managers["WinMan"].smplx_tool.smplx_gender = gender
    bpy.ops.scene.smplx_add_gender()

    bpy.ops.object.select_all(action="DESELECT")
    armature = bpy.data.objects.get(f"SMPLX-{gender}")
    mesh = bpy.data.objects.get(f"SMPLX-mesh-{gender}")

    return armature, mesh


def load_pose(path):
    """Loads a pose file into the SMPLX model.

    Args:
        path (str): The path to the pose file. Must be .pkl.
    """
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.smplx_load_pose(filepath=path)


def set_height_weight(height, weight, gender):
    """Sets the height and weight of the SMPLX model.

    Args:
        height (float): The height of the model in meters.
        weight (float): The weight of the model in kilograms.
        gender (str): The gender of the model. Must be "male" or "female".
    """
    bpy.data.window_managers["WinMan"].smplx_tool.smplx_height = height
    bpy.data.window_managers["WinMan"].smplx_tool.smplx_weight = weight

    bpy.ops.object.select_all(action="DESELECT")
    mesh = bpy.data.objects.get(f"SMPLX-mesh-{gender}")
    mesh.select_set(True)
    bpy.context.view_layer.objects.active = mesh

    bpy.ops.object.smplx_measurements_to_shape()
    bpy.ops.object.smplx_snap_ground_plane()


def get_random_gender():
    """Returns a random gender.

    Returns:
        str: The random gender.
    """
    genders = ["male", "female"]

    return random.choice(genders)


def get_random_height(gender):
    """Returns a random height for the SMPLX model.

    Args:
        gender (str): The gender of the model. Must be "male" or "female".

    Returns:
        float: The random height in meters.

    Notes:
        The height is based on the gender of the model.
    """
    if gender == "female":
        height = random.triangular(1.4, 1.65, 2.0)
    else:
        height = random.triangular(1.5, 1.8, 2.2)

    return round(height, 2)


def get_random_weight(height):
    """Returns a random weight for the SMPLX model.

    Args:
        height (float): The height of the model in meters.

    Returns:
        float: The random weight in kilograms.

    Notes:
        The weight is based on the height of the model.
    """
    mean_weight = 22 * (height**2)
    std_dev = 15

    weight = random.gauss(mean_weight, std_dev)

    min_weight = 18 * (height**2)
    max_weight = 30 * (height**2)

    if random.random() < 0.2:
        weight += random.uniform(20, 50)

    weight = max(min_weight, min(weight, max_weight + 20))

    return round(weight, 2)


def set_keyframe_bones(armature, frame):
    """Sets a keyframe for the location and rotation of each bone of the armature to the given frame.

    Args:
        armature (bpy.types.Object): The armature object.
        frame (int): The frame to set the keyframes at.
    """
    for bone in armature.pose.bones:
        bone.keyframe_insert(data_path="location", frame=frame)
        bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)


def set_keyframe_location(obj, frame):
    """Sets a keyframe for the location of an object to the given frame.

    Args:
        obj (bpy.types.Object): The object to set the keyframe for.
        frame (int): The frame to set the keyframe at.
    """
    bpy.ops.object.smplx_snap_ground_plane()
    obj.keyframe_insert(data_path="location", frame=frame)


def set_keyframe_shape_keys(obj, frame):
    """Sets keyframes of all shape keys of an object to the given frame.

    Args:
        obj (bpy.types.Object): The object to set the keyframes for.
        frame (int): The frame to set the keyframes at.
    """
    if not obj.data.shape_keys:
        print(f"Mesh {obj} has no shape keys")
        return

    for shape_key in obj.data.shape_keys.key_blocks:
        shape_key.keyframe_insert(data_path="value", frame=frame)


# https://projects.blender.org/extensions/print3d_toolbox
def bmesh_copy_from_object(
    obj, transform=True, triangulate=True, apply_modifiers=False
):
    """Copies the mesh data from an object to a bmesh.

    Args:
        obj (bpy.types.Object): The object to copy the mesh data from.
        transform (bool, optional): Whether to apply the object's transformation matrix to the bmesh. Defaults to True.
        triangulate (bool, optional): Whether to triangulate the bmesh. Defaults to True.
        apply_modifiers (bool, optional): Whether to apply the object's modifiers to the bmesh. Defaults to False.

    Returns:
        _type_: _description_
    """
    assert obj.type == "MESH"

    if apply_modifiers and obj.modifiers:
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        me = obj_eval.to_mesh()
        bm = bmesh.new()
        bm.from_mesh(me)
        obj_eval.to_mesh_clear()
    else:
        me = obj.data
        if obj.mode == "EDIT":
            bm_orig = bmesh.from_edit_mesh(me)
            bm = bm_orig.copy()
        else:
            bm = bmesh.new()
            bm.from_mesh(me)

    if transform:
        matrix = obj.matrix_world.copy()
        if not matrix.is_identity:
            bm.transform(matrix)
            # Update normals if the matrix has no rotation.
            matrix.translation.zero()
            if not matrix.is_identity:
                bm.normal_update()

    if triangulate:
        bmesh.ops.triangulate(bm, faces=bm.faces)

    return bm


def bmesh_check_self_intersect_object(obj):
    """Checks if an object has self-intersections in its mesh.

    Args:
        obj (bpy.types.Object): The object to check.

    Returns:
        array.array: An array of indices of the faces that have self-intersections.
    """
    import array
    import mathutils

    if not obj.data.polygons:
        return array.array("i", ())

    bm = bmesh_copy_from_object(obj, transform=False, triangulate=False)
    tree = mathutils.bvhtree.BVHTree.FromBMesh(bm, epsilon=0.00001)
    overlap = tree.overlap(tree)
    faces_error = {i for i_pair in overlap for i in i_pair}

    return array.array("i", faces_error)
