import bpy
import os
import addon_utils

addon_zip_path="./smpl/smplx_blender_addon_20220623.zip"

def install_addon(addon_zip_path):
    if "smplx_blender_addon" not in bpy.context.preferences.addons:
        if not os.path.exists(addon_zip_path):
            bpy.ops.wm.quit_blender()
            raise ValueError("SMPL-X for Blender addon zip file not found")
        bpy.ops.preferences.addon_install(filepath=addon_zip_path)
        print("Installed SMPL-X for Blender")

    for mod in addon_utils.modules():
        if mod.bl_info["name"] == "SMPL-X for Blender":
            addon_utils.enable("smplx_blender_addon", default_set=True)
            print(f"Enabled {mod.bl_info['name']}")
            bpy.ops.wm.quit_blender()
            return

bpy.context.preferences.view.show_splash = False
install_addon(addon_zip_path)