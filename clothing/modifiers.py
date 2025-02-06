def add_collision(object, thickness_inner=0.001, thickness_outer=0.001):
    """Adds a collision modifier to an object.

    Args:
        object (bpy.types.Object): The object to add the collision modifier to.
        thickness_inner (float, optional): The thickness of the inner collision. Defaults to 0.001.
        thickness_outer (float, optional): The thickness of the outer collision. Defaults to 0.001.
    """
    if not object:
        print(f"Mesh {object} not found")
        return

    object.modifiers.new(name="Collision", type="COLLISION")
    object.collision.thickness_inner = thickness_inner
    object.collision.thickness_outer = thickness_outer


# TODO: Pants
def shrink_waistband(obj, target_obj):
    shrinkwrap_modifier = obj.modifiers.new(name="Shrinkwrap", type="SHRINKWRAP")

    shrinkwrap_modifier.wrap_method = "NEAREST_SURFACEPOINT"
    shrinkwrap_modifier.wrap_mode = "ON_SURFACE"
    shrinkwrap_modifier.target = target_obj
    shrinkwrap_modifier.offset = 0.005
    shrinkwrap_modifier.vertex_group = "Waistband"
