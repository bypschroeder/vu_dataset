import bpy

def set_material_base_color(obj_name, hex_color):
    """
    Sets the base color of a material on an object.

    :param obj: The object to set the material on.
    :type obj: bpy.types.Object
    :param hex_color: The hex color to set.
    :type hex_color: str
    """
    
    obj = bpy.data.objects[obj_name]

    if not obj:
        raise ValueError(f"Object {obj_name} not found.")
    
    if not obj.data.materials:
        mat = bpy.data.materials.new(name="BaseColor")
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]

    if not mat.use_nodes:
        mat.use_nodes = True

    nodes = mat.node_tree.nodes

    bsdf = nodes.get("Principled BSDF")

    if not bsdf:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        output = nodes.get("Material Output")
        if output:
            mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))

    bsdf.inputs["Base Color"].default_value = (*rgb, 1)