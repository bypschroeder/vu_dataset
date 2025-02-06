import bpy


def render_image(camera, output_path, target_obj=None):
    """Renders an image and saves it to the specified output path.

    Args:
        camera (bpy.types.Object): The camera to use for rendering.
        output_path (str): The path to the output image.
        target_obj (bpy.types.Object, optional): The object to render. Defaults to None.

    Notes:
        Only renders the selected objects which are given as target_obj. If target_obj is None, renders all objects.
    """
    bpy.context.scene.frame_set(bpy.context.scene.frame_end)

    bpy.context.scene.render.filepath = output_path
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.image_settings.color_mode = "RGBA"

    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080

    bpy.context.scene.render.film_transparent = True

    for obj in bpy.data.objects:
        if obj.type != "LIGHT":
            obj.hide_render = True
        else:
            obj.hide_render = False

    if target_obj:
        if target_obj:
            target_obj.hide_render = False
        else:
            print(f"Object '{target_obj}' not found.")
    else:
        for obj in bpy.data.objects:
            obj.hide_render = False

    bpy.context.scene.camera = camera

    bpy.ops.render.render(write_still=True)
    print("Rendered image to", output_path)
