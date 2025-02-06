import bpy
import os
import sys
import math


# Adds the necessary subdirectories to the system path so Blender can find the scripts.
def add_subdirs_to_sys_path(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if os.path.basename(dirpath) == "__pycache__":
            continue
        sys.path.append(dirpath)


script_dir = os.path.dirname(os.path.abspath(__file__))
add_subdirs_to_sys_path(script_dir)

from config.config_loader import load_config, load_garment_configs
from _helpers.ArgumentParserForBlender import ArgumentParserForBlender
from _helpers.scene import (
    clear_scene,
    setup_scene,
    scale_obj,
    add_object,
    set_color,
    get_random_blend_file,
    apply_all_transforms,
    cleanup,
)
from _helpers.export import export_to_obj, save_export_info, save_pose
from _helpers.render import render_image
from smpl.import_smpl import (
    import_smplx_model,
    get_random_gender,
    get_random_height,
    get_random_weight,
    set_keyframe_bones,
    set_keyframe_location,
    set_keyframe_shape_keys,
    load_pose,
    bmesh_check_self_intersect_object,
    set_height_weight,
)
from smpl.generate_pose import generate_random_pose
from clothing.fit_garment import (
    set_cloth,
    bake_cloth,
    create_proxy,
    apply_deform,
    bind_deform,
    post_process,
)
from clothing.modifiers import add_collision

# Parse arguments
parser = ArgumentParserForBlender()
parser.add_argument(
    "--iterations",
    type=int,
    default=1,
    help="The number of iterations to run for each garment.",
)
parser.add_argument(
    "--garments",
    type=str,
    nargs="+",
    help="Specify one or more garments to use. If not specified all garments will be processed.",
)
parser.add_argument(
    "--gender",
    type=str,
    default="male",
    help="The gender of the avatar. If not specified, a random gender will be used.",
)
parser.add_argument("--output_path", type=str, help="The output path for the results.")

args = parser.parse_args()
iterations = args.iterations
garments = args.garments
gender = args.gender
output_path = args.output_path

# Load configs
config = load_config(os.path.abspath("./config/config.json"))
garment_configs = load_garment_configs(os.path.abspath("./config/garments"), garments)

# Disable the Blender splash screen at startup.
bpy.context.preferences.view.show_splash = False

for garment_type, garment_config in garment_configs.items():
    print(f"\033[1;31mProcessing {garment_type}\033[0m")

    # Create base output directory
    output_base_path = os.path.join(os.path.abspath(output_path), garment_type)
    os.makedirs(output_base_path, exist_ok=True)

    for i in range(iterations):
        # Get next iteration index
        existing_iterations = [
            d
            for d in os.listdir(output_base_path)
            if os.path.isdir(os.path.join(output_base_path, d))
        ]
        next_index = len(existing_iterations)

        # Create scene
        clear_scene()
        camera, light = setup_scene(
            camera_location=tuple(config["scene"]["front"]["camera_location"]),
            camera_rotation=tuple(config["scene"]["front"]["camera_rotation"]),
            light_rotation=tuple(config["scene"]["light_rotation"]),
        )

        # Get random height, weight, gender
        if not gender:
            gender = get_random_gender()
        height = get_random_height(gender)
        weight = get_random_weight(height)
        print(f"Gender: {gender}, Height: {height}, Weight: {weight}")

        # Import SMPLX model
        armature, mesh = import_smplx_model(gender)

        # Scale up for better simulation
        scale_obj(armature, 10)

        # Set color
        set_color(mesh, config["avatar"]["color"])

        bpy.ops.object.smplx_snap_ground_plane()

        # Set keyframes
        set_keyframe_bones(armature, config["animation"]["start_frame"] + 5)
        set_keyframe_location(armature, config["animation"]["start_frame"] + 5)
        set_keyframe_shape_keys(mesh, config["animation"]["start_frame"] + 5)

        # Load pose and check for self-intersections
        while True:
            pose_path, pose_dict = generate_random_pose(
                os.path.abspath("./smpl/random_pose.pkl")
            )
            load_pose(pose_path)

            depsgraph = bpy.context.evaluated_depsgraph_get()
            obj_eval = mesh.evaluated_get(depsgraph)

            intersect = bmesh_check_self_intersect_object(obj_eval)
            print(len(intersect))

            if len(intersect) <= 600:
                break

        # Set Keyframes
        set_keyframe_bones(armature, config["animation"]["end_frame"])
        bpy.context.scene.frame_set(config["animation"]["end_frame"])
        set_height_weight(height, weight, gender) # Apply height and weight to mesh
        set_keyframe_shape_keys(mesh, config["animation"]["end_frame"])
        set_keyframe_location(armature, config["animation"]["end_frame"])

        # Only for bottoms relevant
        z_offset = None
        for fcurve in armature.animation_data.action.fcurves:
            if fcurve.data_path == "location" and fcurve.array_index == 2:  # Z-axis
                keyframe_points = fcurve.keyframe_points
                z_start = keyframe_points[0].co[1]
                z_end = keyframe_points[1].co[1]
                z_offset = z_end - z_start
                break

        if z_offset is None:
            raise ValueError(
                "Z-offset could not be calculated. Ensure keyframes are properly set."
            )

        # Add collision for avatar
        add_collision(mesh, thickness_inner=0.001, thickness_outer=0.001)

        # Add clothing
        garment_path = get_random_blend_file(
            os.path.join(os.path.abspath(garment_config["folder_path"]), gender)
        )
        garment_name = os.path.basename(garment_path).split(".")[0]
        garment = add_object(
            garment_path,
            garment_name,
        )
        # Scale up for better simulation
        scale_obj(garment, 10)
        apply_all_transforms(garment)

        # Set color
        set_color(garment, config["garment"]["color"])

        # Create proxy and add cloth simulation
        if garment_config["decimation_ratio"] < 1.0:
            proxy = create_proxy(garment, garment_config["decimation_ratio"])
            set_cloth(proxy, garment_config["cloth_settings"])
            bpy.context.scene.frame_set(config["animation"]["start_frame"])
            surface_mod = bind_deform(proxy, garment)
            bake_cloth(
                config["animation"]["start_frame"], config["animation"]["end_frame"]
            )
            apply_deform(garment, surface_mod, proxy)
        else:
            set_cloth(garment, garment_config["cloth_settings"])
            bake_cloth(
                config["animation"]["start_frame"], config["animation"]["end_frame"]
            )

        # Post process
        seams_bevel = garment_config["post_process"]["seams_bevel"]
        shrink_seams = garment_config["post_process"]["shrink_seams"]
        thickness = garment_config["post_process"]["thickness"]
        subdivisions = garment_config["post_process"]["subdivisions"]
        post_process(garment, seams_bevel, shrink_seams, thickness, subdivisions)

        # Reset scale
        scale_obj(armature, 1)
        bpy.ops.object.smplx_snap_ground_plane()
        set_keyframe_location(armature, config["animation"]["end_frame"])
        scale_obj(garment, 0.1)

        # Output
        current_output_path = os.path.join(output_base_path, str(next_index)) 
        os.makedirs(current_output_path, exist_ok=True)

        # Render images
        if (
            config["render"]["avatar"]
            or config["render"]["garment"]
            or config["render"]["full"]
        ):
            images_path = os.path.join(current_output_path, "images")
            os.makedirs(images_path, exist_ok=True)

        if config["render"]["perspectives"]["side"]:
            side_rotation = tuple(
                math.radians(angle)
                for angle in config["scene"]["side"]["camera_rotation"]
            )
            bpy.ops.object.camera_add(
                location=config["scene"]["side"]["camera_location"],
                rotation=side_rotation,
            )
            camera_side = bpy.context.object
        if config["render"]["perspectives"]["back"]:
            back_rotation = tuple(
                math.radians(angle)
                for angle in config["scene"]["back"]["camera_rotation"]
            )
            bpy.ops.object.camera_add(
                location=config["scene"]["back"]["camera_location"],
                rotation=back_rotation,
            )
            camera_back = bpy.context.object

        if config["render"]["avatar"]:
            render_image(
                camera=camera,
                output_path=os.path.join(images_path, "avatar.png"),
                target_obj=mesh,
            )
            if config["render"]["perspectives"]["side"]:
                render_image(
                    camera=camera_side,
                    output_path=os.path.join(images_path, "avatar_side.png"),
                    target_obj=mesh,
                )
            if config["render"]["perspectives"]["back"]:
                render_image(
                    camera=camera_back,
                    output_path=os.path.join(images_path, "avatar_back.png"),
                    target_obj=mesh,
                )

        if config["render"]["garment"]:
            render_image(
                camera=camera,
                output_path=os.path.join(images_path, "garment.png"),
                target_obj=garment,
            )
            if config["render"]["perspectives"]["side"]:
                render_image(
                    camera=camera_side,
                    output_path=os.path.join(images_path, "garment_side.png"),
                    target_obj=garment,
                )
            if config["render"]["perspectives"]["back"]:
                render_image(
                    camera=camera_back,
                    output_path=os.path.join(images_path, "garment_back.png"),
                    target_obj=garment,
                )

        if config["render"]["full"]:
            render_image(
                camera=camera,
                output_path=os.path.join(images_path, "full.png"),
                target_obj=None,
            )
            if config["render"]["perspectives"]["side"]:
                render_image(
                    camera=camera_side,
                    output_path=os.path.join(images_path, "full_side.png"),
                    target_obj=None,
                )
            if config["render"]["perspectives"]["back"]:
                render_image(
                    camera=camera_back,
                    output_path=os.path.join(images_path, "full_back.png"),
                    target_obj=None,
                )

        # Export 3D
        if config["export"]["format"] == "OBJ":
            obj_export_path = os.path.join(current_output_path, "obj")
            os.makedirs(obj_export_path, exist_ok=True)
            if config["export"]["avatar"]:
                export_to_obj(
                    os.path.join(obj_export_path, "avatar.obj"),
                    garment=None,
                    avatar=mesh,
                )
            if config["export"]["garment"]:
                export_to_obj(
                    os.path.join(obj_export_path, "garment.obj"),
                    garment=garment,
                    avatar=None,
                )
            if config["export"]["full"]:
                export_to_obj(
                    os.path.join(obj_export_path, "full.obj"),
                    garment=garment,
                    avatar=mesh,
                )
        elif config["export"]["format"] != "OBJ":
            raise ValueError(
                f"Unsupported export format: {config['export']['format']} is not supported yet."
            )

        # Save Info
        if config["save_export_info"]:
            save_export_info(height, weight, gender, garment_name, garment_name.split("_")[0], current_output_path)

        # Save pose
        if config["save_pose"]:
            save_pose(pose_dict, current_output_path)

        # Cleanup
        cleanup()