import pyglet
from pyglet import shapes

# Import the ECS core components
from engine_core.world import World
from engine_core.components import Position, Renderable

# --- Game-Specific Systems ---
# Systems contain the logic of your game. They operate on entities
# that have a specific set of components.


def movement_system(world: World, dt: float):
    """
    This is a placeholder for now. In the future, it would update the
    Position component based on the Velocity component.
    """
    # Example of how it would work:
    # for entity_id, (pos, vel) in world.get_components(Position, Velocity):
    #     pos.x += vel.dx * dt
    #     pos.y += vel.dy * dt
    pass


def render_update_system(world: World):
    """
    This system updates the visual representation of entities.
    It finds all entities with a Position and a Renderable component
    and updates the shape's position to match the component's data.
    """
    for entity_id, (pos, renderable) in world.get_components(Position, Renderable):
        renderable.shape.x = pos.x
        renderable.shape.y = pos.y


# --- The Main Engine Class (User Facing) ---

class Engine:
    """
    The main class for the user's game.
    This class initializes the game world, entities, and systems.
    """
    def __init__(self, window_width, window_height):
        self.world = World()
        self.main_batch = pyglet.graphics.Batch()

        # --- Entity Creation ---
        # This is how a user would create a game object.
        # 1. Create a blank entity ID
        player_entity = self.world.create_entity()

        # 2. Create component instances with data
        player_position = Position(x=window_width / 2, y=window_height / 2)
        player_renderable = Renderable(
            shape=shapes.Rectangle(
                x=player_position.x,
                y=player_position.y,
                width=100,
                height=100,
                color=(255, 255, 255),
                batch=self.main_batch
            )
        )

        # 3. Add components to the entity
        self.world.add_component(player_entity, player_position)
        self.world.add_component(player_entity, player_renderable)

    def update(self, dt: float):
        """The main update loop for the game logic."""
        # Run all the game's systems
        movement_system(self.world, dt)
        render_update_system(self.world)

    def draw(self):
        """The main drawing loop for the game."""
        self.main_batch.draw()

