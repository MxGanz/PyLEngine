# This is the start of the PyLE Python-Lua lightweight game Engine.
# The goal is to implement a simple ECS, using basic Python,
# to minimize the learning curve and maximize interoperability.


import pyglet
from pyglet import shapes

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

# --- Batch Rendering System --- #
# A batch is a collection of graphical objects that can be drawn all at once.
# This is much more efficient than drawing each object individually.
# We will add all our game objects (sprites, shapes, etc.) to this batch.
main_batch = pyglet.graphics.Batch()

# --- Game Objects --- #
# Let's create a primitive shape. A simple rectangle.
# We need to specify its position (x, y), size (width, height), color,
# and importantly, which batch it belongs to.
# The window's coordinate system starts at (0, 0) in the bottom-left corner.
rectangle = shapes.Rectangle(
    x=WINDOW_WIDTH // 2 - 50,  # Center the rectangle horizontally
    y=WINDOW_HEIGHT // 2 - 50,  # Center the rectangle vertically
    width=100,
    height=100,
    color=(255, 255, 255),  # White color
    batch=main_batch  # Add this shape to our main batch
)


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

    # FIXME change so this is not reset every render frame, small but needed
    # 2. Set a solid background color
    pyglet.gl.glClearColor(25/255, 135/255, 45/255, 1.0)

    # 3. Draw the batch
    # This single command tells Pyglet to draw every object that has been
    # added to the 'main_batch'.
    main_batch.draw()


# --- Main Entry Point for the Engine --- #
if __name__ == '__main__':
    # This command starts the Pyglet application event loop.
    # It will run continuously, processing system events and calling our
    # event handlers (like on_draw) until the window is closed.
    # This is the "engine" that keeps our game running.
    pyglet.app.run()

    print("Bye!")


