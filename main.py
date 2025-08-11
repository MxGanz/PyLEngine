# This is the start of the PyLE Python-Lua lightweight game Engine.
# The goal is to implement a simple ECS, using basic Python,
# to minimize the learning curve and maximize interoperability.

import pyglet
from engine import Engine  # Import the user-facing Engine class

# --- Constants and Configuration ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "My Awesome Game Engine"

# --- Main Application Setup ---
if __name__ == '__main__':
    # 1. Create the main window
    window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # 2. Create an instance of the user's game engine
    game_engine = Engine(WINDOW_WIDTH, WINDOW_HEIGHT)

    # 3. Define the update function for the game loop
    def update(dt):
        """
        This function is called by Pyglet's clock at a regular interval.
        'dt' is the delta-time, the time since the last update.
        """
        game_engine.update(dt)

    # 4. Schedule the update function
    pyglet.clock.schedule_interval(update, 1/60.0)  # Aim for 60 updates per second

    # 5. Set up the on_draw event handler
    @window.event
    def on_draw():
        """
        This is called by Pyglet whenever the window needs to be redrawn.
        """
        window.clear()
        pyglet.gl.glClearColor(25/255, 35/255, 45/255, 1.0)
        game_engine.draw()

    # 6. Run the Pyglet application
    pyglet.app.run()

    print("Window closed. Exiting application.")

