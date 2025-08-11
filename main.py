# This is the start of the PyLE Python-Lua lightweight game Engine.
# The goal is to implement a simple ECS, using basic Python,
# to minimize the learning curve and maximize interoperability.


import pyglet


# --- CONSTRAINTS AND CONFIG --- #
# This section holds the general settings for the pyglet window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Your PyLE Game!"    # Replace with your window name
#IS_FULLSCREEN = FALSE              # unused
#IS_BORDERLESS = FALSE              # unused

# --- Create the Main Window --- #
# This is the primary surface where all our graphics will be drawn.
# We pass our configuration constants to create a window of the desired size and title.
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

# --- Event Handlers --- #
# Pyglet uses an event-driven model. We use decorators to "listen" for
# specific events from the window (like drawing, mouse clicks, key presses, etc.).


@window.event
def on_draw():
    """
    This function is called by Pyglet automatically whenever the window needs
    to be redrawn (which happens many times per second). This is the heart
    of the rendering loop.
    """

    # 1. Clear the window
    window.clear()

    # 2. Set a solid background color
    pyglet.gl.glClearColor(25/255, 135/255, 45/255, 1.0)

    # 3. Add your drawing code here!


# --- Main Entry Point for the Engine --- #
if __name__ == '__main__':
    # This command starts the Pyglet application event loop.
    # It will run continuously, processing system events and calling our
    # event handlers (like on_draw) until the window is closed.
    # This is the "engine" that keeps our game running.
    pyglet.app.run()

    print("Bye!")


