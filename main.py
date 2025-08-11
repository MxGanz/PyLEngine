# This is the start of the PyLE Python-Lua lightweight game Engine.
# The goal is to implement a simple ECS, using basic Python,
# to minimize the learning curve and maximize interoperability.

import pyglet
import os
import importlib.util

# Use relative imports for our engine core
from engine_core.world import World

# --- Constants and Configuration ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "My Awesome Game Engine"
COMPONENT_DIR = "components"
ENTITY_DIR = "entities"
SYSTEM_DIR = "systems"

# --- Main Application Setup ---
if __name__ == '__main__':
    # 1. Create the main window and a batch for rendering
    window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    main_batch = pyglet.graphics.Batch()

    # 2. Create the World. This will automatically load and register all .comp files.
    world = World(batch=main_batch, component_dir=COMPONENT_DIR)

    # 3. Load all entity definitions from the 'entities' directory
    print("--- Loading Entities ---")
    for filename in os.listdir(ENTITY_DIR):
        if filename.endswith(".ent"):
            filepath = os.path.join(ENTITY_DIR, filename)
            world.create_entity_from_file(filepath)
    print("------------------------")

    # 4. Load all system scripts from the 'systems' directory
    print("--- Loading Systems ---")
    systems = []
    for filename in os.listdir(SYSTEM_DIR):
        # --- FIX ---
        # Changed from .sys to .py so Python's import system can find the loader.
        if filename.endswith(".py") and not filename.startswith("__"):
            filepath = os.path.join(SYSTEM_DIR, filename)
            module_name = filename[:-3]  # Use -3 for .py
            # --- END FIX ---

            # Dynamically import the system module
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            if spec and spec.loader:  # Check that the spec was created successfully
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Assume each system file has a function called 'run'
                if hasattr(module, 'run'):
                    systems.append(module.run)
                    print(f"Loaded system: {module_name}")
            else:
                print(f"Warning: Could not load system '{filename}'.")

    print("-----------------------")


    # 5. Define the main update function
    def update(dt):
        """This function runs all loaded systems."""
        for system_func in systems:
            system_func(world, dt)


    pyglet.clock.schedule_interval(update, 1 / 60.0)


    # 6. Set up the on_draw event handler
    @window.event
    def on_draw():
        window.clear()
        pyglet.gl.glClearColor(25 / 255, 35 / 255, 45 / 255, 1.0)
        main_batch.draw()


    # 7. Run the Pyglet application
    pyglet.app.run()

    print("Window closed. Exiting application.")
