# --- components.py --- #
# This is the core place where Components
# are defined and exist.

from dataclasses import dataclass
from pyglet import shapes

# --- Component Definitions ---
# Components are simple data containers. They should not contain any logic.
# We use @dataclass to automatically generate methods like __init__ and __repr__.


@dataclass
class Position:
    """Represents the position of an entity in 2D space."""
    x: float = 0.0
    y: float = 0.0


@dataclass
class Velocity:
    """Represents the velocity of an entity."""
    dx: float = 0.0
    dy: float = 0.0


@dataclass
class Renderable:
    """
    Contains the graphical representation of an entity.
    This holds the actual pyglet shape object that will be drawn.
    """
    shape: shapes.ShapeBase  # The pyglet shape object (e.g., Rectangle, Circle)


@dataclass
class PlayerControlled:
    """A tag component to identify the player entity. It has no data."""
    pass
