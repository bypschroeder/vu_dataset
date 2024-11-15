import bpy

def render_image(camera, output_path):
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

    bpy.context.scene.render.film_transparent = True

    bpy.ops.render.render(write_still=True)

    print("Rendered image to", output_path)