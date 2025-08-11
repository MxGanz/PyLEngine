# This system is responsible for keeping the visual shapes
# in sync with the data in the Position components.

def run(world, dt):
    # We need to get the component classes from the world's registry
    Position = world.get_component_class("Position")
    Renderable = world.get_component_class("Renderable")

    if not Position or not Renderable:
        return # One of the required components isn't registered

    for entity_id, (pos, renderable) in world.get_components(Position, Renderable):
        if renderable.shape:
            renderable.shape.x = pos.x
            renderable.shape.y = pos.y
