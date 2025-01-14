import bpy
import bmesh


def set_cloth_material(obj, material_type):
    """
    Sets the cloth material for an object.

    :param obj: The object to set the cloth material for.
    :type obj: bpy.types.Object
    :param material_type: The type of material to use.
    :type material_type: str
    """
    cloth_modifier = obj.modifiers.get("Cloth")

    if not cloth_modifier:
        cloth_modifier = obj.modifiers.new(name="Cloth", type="CLOTH")

    cloth_settings = cloth_modifier.settings
    collision_settings = cloth_modifier.collision_settings

    if material_type == "t-shirt":
        cloth_settings.quality = 8
        cloth_settings.mass = 0.2

        cloth_settings.tension_stiffness = 15
        cloth_settings.compression_stiffness = 15
        cloth_settings.shear_stiffness = 15
        cloth_settings.bending_stiffness = 0.500

        cloth_settings.tension_damping = 5
        cloth_settings.compression_damping = 5
        cloth_settings.shear_damping = 5
        cloth_settings.bending_damping = 0.500

        collision_settings.collision_quality = 4
        collision_settings.distance_min = 0.03

        collision_settings.use_self_collision = True
        collision_settings.self_distance_min = 0.001
    elif material_type == "pants":
        cloth_settings.quality = 8
        cloth_settings.mass = 0.8
        cloth_settings.air_damping = 1

        cloth_settings.tension_stiffness = 40
        cloth_settings.compression_stiffness = 40
        cloth_settings.shear_stiffness = 40
        cloth_settings.bending_stiffness = 10

        cloth_settings.tension_damping = 25
        cloth_settings.compression_damping = 25
        cloth_settings.shear_damping = 5
        cloth_settings.bending_damping = 0.5

        collision_settings.collision_quality = 4
        collision_settings.distance_min = 0.03

        collision_settings.use_self_collision = True
        collision_settings.self_distance_min = 0.001

        cloth_settings.vertex_group_mass = "Waistband"
        cloth_settings.pin_stiffness = 0.1
    elif material_type == "shorts":
        cloth_settings.quality = 8
        cloth_settings.mass = 0.4
        cloth_settings.air_damping = 1

        cloth_settings.tension_stiffness = 30
        cloth_settings.compression_stiffness = 30
        cloth_settings.shear_stiffness = 30
        cloth_settings.bending_stiffness = 7

        cloth_settings.tension_damping = 25
        cloth_settings.compression_damping = 25
        cloth_settings.shear_damping = 5
        cloth_settings.bending_damping = 0.5

        collision_settings.collision_quality = 4
        collision_settings.distance_min = 0.03

        collision_settings.use_self_collision = True
        collision_settings.self_distance_min = 0.001

        cloth_settings.vertex_group_mass = "Waistband"
        cloth_settings.pin_stiffness = 0.1
    elif material_type == "hoodie":
        cloth_settings.quality = 8
        cloth_settings.mass = 0.5

        cloth_settings.tension_stiffness = 25
        cloth_settings.compression_stiffness = 25
        cloth_settings.shear_stiffness = 25
        cloth_settings.bending_stiffness = 0.800

        cloth_settings.tension_damping = 7
        cloth_settings.compression_damping = 7
        cloth_settings.shear_damping = 7
        cloth_settings.bending_damping = 0.700

        collision_settings.collision_quality = 4
        collision_settings.distance_min = 0.03

        collision_settings.use_self_collision = True
        collision_settings.self_distance_min = 0.002
    elif material_type == "sweatshirt":
        cloth_settings.quality = 8
        cloth_settings.mass = 0.4

        cloth_settings.tension_stiffness = 20
        cloth_settings.compression_stiffness = 20
        cloth_settings.shear_stiffness = 20
        cloth_settings.bending_stiffness = 0.600

        cloth_settings.tension_damping = 6
        cloth_settings.compression_damping = 6
        cloth_settings.shear_damping = 6
        cloth_settings.bending_damping = 0.600

        collision_settings.collision_quality = 4
        collision_settings.distance_min = 0.03

        collision_settings.use_self_collision = True
        collision_settings.self_distance_min = 0.002
    else:
        print("Material type not found")


def add_solidify_modifier(obj, thickness=-0.1):
    """
    Adds a solidify modifier to an object.

    :param obj: The object to add the solidify modifier to.
    :type obj: bpy.types.Object
    """
    solidify_modifier = obj.modifiers.new(name="Solidify", type="SOLIDIFY")

    solidify_modifier.thickness = thickness


def add_smooth_modifier(obj):
    """
    Adds a smooth modifier to an object.

    :param obj: The object to add the smooth modifier to.
    :type obj: bpy.types.Object
    """
    smooth_modifier = obj.modifiers.new(name="Smooth", type="SMOOTH")

    smooth_modifier.factor = 0.275
    smooth_modifier.iterations = 2


def add_subdivision_modifier(obj, levels=1, render_levels=2):
    """
    Adds a subdivision modifier to an object.

    :param obj: The object to add the subdivision modifier to.
    :type obj: bpy.types.Object
    """
    subdivision_modifier = obj.modifiers.new(name="Subdivision", type="SUBSURF")

    subdivision_modifier.subdivision_type = "CATMULL_CLARK"
    subdivision_modifier.levels = levels
    subdivision_modifier.render_levels = render_levels


def postprocess_top(obj, thickness, subdivisions):
    """
    Postprocesses the top clothing for better output.

    :param obj: The object to apply the cloth modifiers to.
    :type obj: bpy.types.Object
    """

    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="Cloth")

    bpy.ops.object.mode_set(mode="EDIT")

    bm = bmesh.from_edit_mesh(obj.data)

    for edge in bm.edges:
        if edge.seam:
            edge.select_set(True)

    bmesh.update_edit_mesh(obj.data)

    bpy.ops.mesh.bevel(
        offset=0.01, offset_pct=0, segments=3, profile=0.5, affect="EDGES"
    )

    bpy.ops.mesh.select_less()
    bpy.ops.transform.shrink_fatten(value=-0.02, use_even_offset=True)

    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode="OBJECT")

    add_solidify_modifier(obj, thickness=thickness)
    add_subdivision_modifier(obj, levels=subdivisions, render_levels=subdivisions)


def postprocess_bottom(obj, thickness, subdivisions):
    """
    Postprocesses the bottom clothing for better output.

    :param obj: The object to postprocess.
    :type obj: bpy.types.Object
    """

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="Shrinkwrap")
    bpy.ops.object.modifier_apply(modifier="Cloth")

    add_solidify_modifier(obj, thickness)
    add_subdivision_modifier(obj, levels=subdivisions, render_levels=subdivisions)


def add_collision_modifier(mesh):
    """
    Adds the collision modifier to the given mesh.

    :param mesh_name: The name of the mesh.
    :type mesh_name: str
    """
    if not mesh:
        print(f"Mesh {mesh} not found")
        return

    mesh.modifiers.new(name="Collision", type="COLLISION")
    mesh.collision.thickness_inner = 0.001
    mesh.collision.thickness_outer = 0.001


def shrink_waistband(obj, target_obj):
    shrinkwrap_modifier = obj.modifiers.new(name="Shrinkwrap", type="SHRINKWRAP")

    shrinkwrap_modifier.wrap_method = "NEAREST_SURFACEPOINT"
    shrinkwrap_modifier.wrap_mode = "ON_SURFACE"
    shrinkwrap_modifier.target = target_obj
    shrinkwrap_modifier.offset = 0.005
    shrinkwrap_modifier.vertex_group = "Waistband"
