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
    apply_z_offset_keyframes,
    cleanup,
)
from _helpers.export import export_to_obj, save_export_info, save_pose
from _helpers.render import render_image
from _helpers.modifier import add_collision, shrink_waistband
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

# Load base config
config = load_config(os.path.abspath("./config/config.json"))

# TODO: start/endframe überarbeiten
# Set constants
VIEWS = config["scene"]["views"]
SCALE = config["scene"]["scale"]
AVATAR_COLOR = config["avatar"]["color"]
AVATAR_THICKNESS_INNER = config["avatar"]["thickness_inner"]
AVATAR_THICKNESS_OUTER = config["avatar"]["thickness_outer"]
GARMENT_COLOR = config["garment"]["color"]
ANIMATION_START_FRAME = config["animation"]["start_frame"]
ANIMATION_END_FRAME = config["animation"]["end_frame"]
RENDER_AVATAR = config["render"]["avatar"]
RENDER_GARMENT = config["render"]["garment"]
RENDER_FULL = config["render"]["full"]
RENDER_FRONT_PERSPECTIVE = config["render"]["perspectives"]["front"]
RENDER_LEFT_SIDE_PERSPECTIVE = config["render"]["perspectives"]["left_side"]
RENDER_RIGHT_SIDE_PERSPECTIVE = config["render"]["perspectives"]["right_side"]
RENDER_BACK_PERSPECTIVE = config["render"]["perspectives"]["back"]
EXPORT_FORMAT = config["export"]["format"]
EXPORT_AVATAR = config["export"]["avatar"]
EXPORT_GARMENT = config["export"]["garment"]
EXPORT_FULL = config["export"]["full"]
SAVE_EXPORT_INFO = config["save_export_info"]
SAVE_POSE = config["save_pose"]

# Load garment configs
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

        # Clear scene
        clear_scene()

        # Get random height, weight, gender
        if not gender:
            gender = get_random_gender()
        height = get_random_height(gender)
        weight = get_random_weight(height)
        print(f"Gender: {gender}, Height: {height}, Weight: {weight}")

        # Import SMPLX model
        armature, mesh = import_smplx_model(gender)

        # Scale up for better simulation
        scale_obj(armature, SCALE)

        # Set color
        set_color(mesh, AVATAR_COLOR)

        bpy.ops.object.smplx_snap_ground_plane()

        # Set keyframes
        set_keyframe_bones(armature, ANIMATION_START_FRAME + 5)
        set_keyframe_location(armature, ANIMATION_START_FRAME + 5)
        set_keyframe_shape_keys(mesh, ANIMATION_START_FRAME + 5)

        # Load pose and check for self-intersections
        while True:
            pose_path, pose_dict = generate_random_pose(
                os.path.abspath("./smpl/random_pose.pkl")
            )
            load_pose(pose_path)

            depsgraph = bpy.context.evaluated_depsgraph_get()
            obj_eval = mesh.evaluated_get(depsgraph)

            intersect = bmesh_check_self_intersect_object(obj_eval)

            if len(intersect) <= 600:
                print("Regenerating Pose")
                break

        # Set Keyframes
        set_keyframe_bones(armature, ANIMATION_END_FRAME)
        bpy.context.scene.frame_set(ANIMATION_END_FRAME)
        set_height_weight(height, weight, gender)  # Apply height and weight to mesh
        set_keyframe_shape_keys(mesh, ANIMATION_END_FRAME)
        set_keyframe_location(armature, ANIMATION_END_FRAME)

        # Only for bottoms relevant
        z_offset = None
        for fcurve in armature.animation_data.action.fcurves:
            if fcurve.data_path == "location" and fcurve.array_index == 2:  # Z-axis
                keyframe_points = fcurve.keyframe_points
                z_start = keyframe_points[0].co[1]
                z_end = keyframe_points[1].co[1]
                z_offset = z_end - z_start
                z_offset = z_offset
                break

        if z_offset is None:
            raise ValueError(
                "Z-offset could not be calculated. Ensure keyframes are properly set."
            )

        # Add collision for avatar
        add_collision(mesh, AVATAR_THICKNESS_INNER, AVATAR_THICKNESS_OUTER)

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
        scale_obj(garment, SCALE)
        apply_all_transforms(garment)

        # Set color
        set_color(garment, GARMENT_COLOR)

        # Create proxy and add cloth simulation
        if garment_config["decimation_ratio"] < 1.0:
            proxy = create_proxy(garment, garment_config["decimation_ratio"])
            set_cloth(proxy, garment_config["cloth_settings"])

            bpy.context.scene.frame_set(config["animation"]["start_frame"])
            surface_mod = bind_deform(proxy, garment)
            bake_cloth(ANIMATION_START_FRAME, ANIMATION_END_FRAME)
            apply_deform(garment, surface_mod, proxy)
        else:
            # Proxy doesn't work for bottoms
            if garment_config["type"] == "bottom":
                apply_z_offset_keyframes(
                    garment, z_offset, ANIMATION_START_FRAME + 5, ANIMATION_END_FRAME
                )

            set_cloth(garment, garment_config["cloth_settings"])
            bake_cloth(ANIMATION_START_FRAME, ANIMATION_END_FRAME)

        # Post process
        SEAMS_BEVEL = garment_config["post_process"]["seams_bevel"]
        SHRINK_SEAMS = garment_config["post_process"]["shrink_seams"]
        THICKNESS = garment_config["post_process"]["thickness"]
        SUBDIVISIONS = garment_config["post_process"]["subdivisions"]
        post_process(garment, SEAMS_BEVEL, SHRINK_SEAMS, THICKNESS, SUBDIVISIONS)

        # Reset scale
        scale_obj(armature, 1)
        bpy.ops.object.smplx_snap_ground_plane()
        set_keyframe_location(armature, ANIMATION_END_FRAME)
        scale_obj(garment, 1 / SCALE)
        if garment_config["type"] == "bottom":
            garment.location.z = z_offset / SCALE
            garment.keyframe_insert(data_path="location", frame=ANIMATION_END_FRAME)

        # Output
        current_output_path = os.path.join(output_base_path, str(next_index))
        os.makedirs(current_output_path, exist_ok=True)

        # Render images
        if RENDER_AVATAR or RENDER_GARMENT or RENDER_FULL:
            images_path = os.path.join(current_output_path, "images")
            os.makedirs(images_path, exist_ok=True)

            # Setup scene
            cameras = setup_scene(VIEWS)

        if RENDER_AVATAR:
            if RENDER_FRONT_PERSPECTIVE:
                render_image(
                    camera=cameras["front"],
                    output_path=os.path.join(images_path, "avatar_front.png"),
                    target_obj=mesh,
                )
            if RENDER_LEFT_SIDE_PERSPECTIVE:
                render_image(
                    camera=cameras["left_side"],
                    output_path=os.path.join(images_path, "avatar_left_side.png"),
                    target_obj=mesh,
                )
            if RENDER_RIGHT_SIDE_PERSPECTIVE:
                render_image(
                    camera=cameras["right_side"],
                    output_path=os.path.join(images_path, "avatar_right_side.png"),
                    target_obj=mesh,
                )
            if RENDER_BACK_PERSPECTIVE:
                render_image(
                    camera=cameras["back"],
                    output_path=os.path.join(images_path, "avatar_back.png"),
                    target_obj=mesh,
                )

        if RENDER_GARMENT:
            if RENDER_FRONT_PERSPECTIVE:
                render_image(
                    camera=cameras["front"],
                    output_path=os.path.join(images_path, "garment_front.png"),
                    target_obj=garment,
                )
            if RENDER_LEFT_SIDE_PERSPECTIVE:
                render_image(
                    camera=cameras["left_side"],
                    output_path=os.path.join(images_path, "garment_left_side.png"),
                    target_obj=garment,
                )
            if RENDER_RIGHT_SIDE_PERSPECTIVE:
                render_image(
                    camera=cameras["right_side"],
                    output_path=os.path.join(images_path, "garment_right_side.png"),
                    target_obj=garment,
                )
            if RENDER_BACK_PERSPECTIVE:
                render_image(
                    camera=cameras["back"],
                    output_path=os.path.join(images_path, "garment_back.png"),
                    target_obj=garment,
                )

        if RENDER_FULL:
            if RENDER_FRONT_PERSPECTIVE:
                render_image(
                    camera=cameras["front"],
                    output_path=os.path.join(images_path, "full_front.png"),
                    target_obj=None,
                )
            if RENDER_LEFT_SIDE_PERSPECTIVE:
                render_image(
                    camera=cameras["left_side"],
                    output_path=os.path.join(images_path, "full_left_side.png"),
                    target_obj=None,
                )
            if RENDER_RIGHT_SIDE_PERSPECTIVE:
                render_image(
                    camera=cameras["right_side"],
                    output_path=os.path.join(images_path, "full_right_side.png"),
                    target_obj=None,
                )
            if RENDER_BACK_PERSPECTIVE:
                render_image(
                    camera=cameras["back"],
                    output_path=os.path.join(images_path, "full_back.png"),
                    target_obj=None,
                )

        # Export 3D
        if EXPORT_FORMAT == "OBJ":
            obj_export_path = os.path.join(current_output_path, "obj")
            os.makedirs(obj_export_path, exist_ok=True)
            if EXPORT_AVATAR:
                export_to_obj(
                    os.path.join(obj_export_path, "avatar.obj"),
                    garment=None,
                    avatar=mesh,
                )
            if EXPORT_GARMENT:
                export_to_obj(
                    os.path.join(obj_export_path, "garment.obj"),
                    garment=garment,
                    avatar=None,
                )
            if EXPORT_FULL:
                export_to_obj(
                    os.path.join(obj_export_path, "full.obj"),
                    garment=garment,
                    avatar=mesh,
                )
        elif EXPORT_FORMAT != "OBJ":
            raise ValueError(
                f"Unsupported export format: {config['export']['format']} is not supported yet."
            )

        # Save Info
        if SAVE_EXPORT_INFO:
            save_export_info(
                height,
                weight,
                gender,
                garment_name.split("_")[1],
                garment_name.split("_")[0],
                current_output_path,
            )

        # Save pose
        if SAVE_POSE:
            save_pose(pose_dict, current_output_path)

        # Cleanup
        cleanup()
