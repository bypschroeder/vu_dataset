import bpy

def render_image(camera, output_path, target_object_name):
    """
    Renders an image and saves it to the specified output path.

    :param camera: The camera to use for rendering.
    :type camera: bpy.types.Object
    :param output_path: The path to the output image.
    :type output_path: str
    """
    bpy.context.scene.camera = camera

    bpy.context.scene.frame_set(bpy.context.scene.frame_end)

    bpy.context.scene.render.filepath = output_path
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.image_settings.color_mode = "RGBA"

    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080

    bpy.context.scene.render.film_transparent = True

    for obj in bpy.data.objects:
        if obj.type != 'LIGHT': 
            obj.hide_render = True
        else:
            obj.hide_render = False  

    if target_object_name:
        target_obj = bpy.data.objects.get(target_object_name)
        if target_obj:
            target_obj.hide_render = False
        else:
            print(f"Object '{target_object_name}' not found.")
    else:
        for obj in bpy.data.objects:
            obj.hide_render = False

    bpy.ops.render.render(write_still=True)

    print("Rendered image to", output_path)