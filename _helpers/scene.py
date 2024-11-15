import bpy
import math

def clear_scene():
    """
    Clears the current scene of all objects.
    """
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    for collection in bpy.data.collections:
        if collection.name == "Collection":
            bpy.data.collections.remove(collection)

def add_camera(location, rotation):
    """
    Adds a camera to the scene.

    :param location: The location of the camera.
    :type location: tuple
    :param rotation: The rotation of the camera.
    :type rotation: tuple
    :return: The camera object.
    :rtype: bpy.types.Object
    """
    bpy.ops.object.camera_add(location=location)

    camera = bpy.context.object

    r = tuple(math.radians(angle) for angle in rotation)

    camera.rotation_euler = r

    return camera

def add_light(rotation):
    """
    Adds a light to the scene.

    :param rotation: The rotation of the light.
    :type rotation: tuple
    :return: The light object.
    :rtype: bpy.types.Object
    """
    bpy.ops.object.light_add(type='SUN', radius=10, location=(0, 0, 0))

    light = bpy.context.object

    r = tuple(math.radians(angle) for angle in rotation)

    light.rotation_euler = r