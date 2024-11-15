import bpy
import os
import sys
import gc

"""
Adds the necessary subdirectories to the system path so Blender can find the scripts.
"""
def add_subdirs_to_sys_path(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if os.path.basename(dirpath) == "__pycache__":
            continue  
        sys.path.append(dirpath)

script_dir = os.path.dirname(os.path.abspath(__file__))
add_subdirs_to_sys_path(script_dir)

from config.config_loader import load_config
from _helpers.scene import clear_scene, add_camera, add_light
from _helpers.export import export_to_obj, export_to_fbx, export_to_glb
from _helpers.path import get_relative_path
from _helpers.render import render_image
from smpl.import_smpl import create_random_smplx_model
from clothing.append_clothing import append_random_top, append_random_bottom

"""
Load the config file.
"""
config = load_config()

"""
Disable the Blender splash screen at startup.
"""
bpy.context.preferences.view.show_splash = False

"""
Loop for creating a random smplx model and simulating clothing for each cycle.
"""
for i in range(config["cycles"]):
    # Create scene
    clear_scene()
    if config["scene"]["place_camera"]:
        if config["scene"]["randomize_camera"]:
            camera = add_camera((0, 0, 0), (0, 0, 0))
        else:
            camera = add_camera((0, -60, 10), (90, 0, 0))
    if config["scene"]["place_light"]:
        if config["scene"]["randomize_light"]:
            light = add_light((0, 0, 0))
        else:
            light = add_light((90, 0, 0))

    # Create human
    gender, height, weight, z_offset = create_random_smplx_model(randomize_pose=config["human"]["randomize_pose"])

    # Add clothing
    if config["clothing"]["add_top"]:
        append_random_top()
    
    if config["clothing"]["add_bottom"]:
        append_random_bottom(z_offset=z_offset, frame_start=10, frame_end=40)

    # Bake cloth simulation
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 60

    for obj in bpy.data.objects:
        for modifier in obj.modifiers:
            if modifier.type == 'CLOTH': 
                modifier.point_cache.frame_start = bpy.context.scene.frame_start
                modifier.point_cache.frame_end = bpy.context.scene.frame_end

    bpy.ops.ptcache.bake_all(bake=True)

    # Export
    if config["export"]["export_obj"]:
        export_to_obj(get_relative_path(f"/output/export_obj/{i}.obj")) # change export path to config
    
    if config["export"]["export_fbx"]:
        export_to_fbx(get_relative_path(f"/output/export_fbx/{i}.fbx")) # change export path to config
        
    if config["export"]["export_glb"]:
        export_to_glb(get_relative_path(f"/output/export_glb/{i}.glb")) # change export path to config

    # Render
    if config["render"]["render_image"]:
        render_image(camera, get_relative_path(f"/output/render_images/{i}.png")) # change export path to config
    
    # Cleanup
    del camera
    del light
    bpy.ops.outliner.orphans_purge(do_recursive=True, do_linked_ids=True, do_local_ids=True)
    bpy.ops.ptcache.free_bake_all()
    gc.collect()