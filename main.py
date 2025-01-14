import bpy
import os
import sys
import gc
import json
import pickle

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
from clothing.modifiers import postprocess_top, postprocess_bottom

"""
Load the config file.
"""
config = load_config()

"""
Disable the Blender splash screen at startup.
"""
bpy.context.preferences.view.show_splash = False

"""
Cycle through each clothing type and export the results.
"""
for clothing_config in config["clothing_cycles"]:
    print(f"\033[1;31mProcessing {clothing_config['name']}\033[0m")

    output_base_path = get_relative_path(f"/output/{clothing_config['name']}")

    if not os.path.exists(output_base_path):
        os.makedirs(output_base_path)

    for i in range(clothing_config["cycles"]):
        existing_cycles = [
            d
            for d in os.listdir(output_base_path)
            if os.path.isdir(os.path.join(output_base_path, d))
        ]
        next_index = len(existing_cycles)

        # Create scene
        clear_scene()
        camera = add_camera((0, -34, 10.5), (90, 0, 0))
        light = add_light((90, 0, 0))

        # Create human
        gender, height, weight, z_offset, pose_dict = create_random_smplx_model(
            randomize_pose=config["avatar"]["randomize_pose"],
            color=config["avatar"]["avatar_color"],
        )

        # Add clothing
        if clothing_config["type"] == "top":
            garment, top_obj = append_random_top(clothing_config["folder_path"], gender)

        if clothing_config["type"] == "bottom":
            garment, bottom_obj = append_random_bottom(
                z_offset, 10, 40, clothing_config["folder_path"], gender
            )

        # Bake cloth simulation
        bpy.context.scene.frame_start = 0
        bpy.context.scene.frame_end = 70

        for obj in bpy.data.objects:
            for modifier in obj.modifiers:
                if modifier.type == "CLOTH":
                    modifier.point_cache.frame_start = bpy.context.scene.frame_start
                    modifier.point_cache.frame_end = bpy.context.scene.frame_end

        bpy.ops.ptcache.bake_all(bake=True)

        if clothing_config["type"] == "top":
            postprocess_top(
                top_obj, clothing_config["thickness"], clothing_config["subdivisions"]
            )
        if clothing_config["type"] == "bottom":
            postprocess_bottom(
                bottom_obj,
                clothing_config["thickness"],
                clothing_config["subdivisions"],
            )

        # Output
        if not os.path.exists(get_relative_path("/output")):
            os.makedirs(get_relative_path("/output"))

        if not os.path.exists(output_base_path):
            os.makedirs(output_base_path)

        current_output_path = os.path.join(output_base_path, str(next_index))
        os.makedirs(current_output_path, exist_ok=True)

        if (
            config["output"]["render_avatar"]
            or config["output"]["render_garment"]
            or config["output"]["render_full"]
        ):
            images_path = os.path.join(current_output_path, "images")
            os.makedirs(images_path, exist_ok=True)

            if config["output"]["render_avatar"]:
                render_image(
                    camera=camera,
                    output_path=get_relative_path(
                        f"/output/{clothing_config['name']}/{next_index}/images/avatar.png"
                    ),
                    target_object_name=f"SMPLX-mesh-{gender}",
                )

            if config["output"]["render_garment"]:
                render_image(
                    camera=camera,
                    output_path=get_relative_path(
                        f"/output/{clothing_config['name']}/{next_index}/images/garment.png"
                    ),
                    target_object_name=garment,
                )

            if config["output"]["render_full"]:
                render_image(
                    camera=camera,
                    output_path=get_relative_path(
                        f"/output/{clothing_config['name']}/{next_index}/images/full.png"
                    ),
                    target_object_name=None,
                )

        if (
            config["output"]["export_obj"]
            or config["output"]["export_fbx"]
            or config["output"]["export_glb"]
        ):
            if not os.path.exists(
                get_relative_path(f"/output/{clothing_config['name']}/{next_index}/obj")
            ):
                os.makedirs(
                    get_relative_path(
                        f"/output/{clothing_config['name']}/{next_index}/obj"
                    )
                )

            if config["output"]["export_obj"]:
                export_to_obj(
                    get_relative_path(
                        f"/output/{clothing_config['name']}/{next_index}/obj/garment.obj"
                    )
                )

            if config["output"]["export_fbx"]:
                export_to_fbx(
                    get_relative_path(
                        f"/output/{clothing_config['name']}/{next_index}/obj/garment.fbx"
                    )
                )

            if config["output"]["export_glb"]:
                export_to_glb(
                    get_relative_path(
                        f"/output/{clothing_config['name']}/{next_index}/obj/garment.glb"
                    )
                )

        if config["output"]["save_export_info"]:
            garment_size = garment.split("_")[0]
            garment_name = garment.split("_")[1]
            export_info = {
                "height": height,
                "weight": weight,
                "gender": gender,
                "garment": garment_name,
                "size": garment_size,
            }

            with open(
                get_relative_path(
                    f"/output/{clothing_config['name']}/{next_index}/export_info.json"
                ),
                "w",
            ) as f:
                json.dump(export_info, f)

        if config["output"]["save_pose"]:
            with open(
                get_relative_path(
                    f"/output/{clothing_config['name']}/{next_index}/pose.pkl"
                ),
                "wb",
            ) as f:
                pickle.dump(pose_dict, f)

        # Cleanup
        del camera
        del light
        bpy.ops.outliner.orphans_purge(
            do_recursive=True, do_linked_ids=True, do_local_ids=True
        )
        bpy.ops.ptcache.free_bake_all()
        gc.collect()
