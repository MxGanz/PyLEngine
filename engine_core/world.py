import json
import os
from collections import defaultdict
from dataclasses import make_dataclass
from pyglet import shapes


class World:
    """
    The World class manages all entities, components, and their instantiation from files.
    """

    def __init__(self, batch, component_dir):
        """
        Initializes the World.
        :param batch: The main pyglet rendering batch.
        :param component_dir: The directory where .comp files are stored.
        """
        self.next_entity_id = 0
        self.component_stores = defaultdict(dict)
        self.main_batch = batch
        self._component_registry = {}

        print("--- Loading Components ---")
        self._load_and_register_components(component_dir)
        print("--------------------------")

    def _load_and_register_components(self, component_dir):
        """Scans the component directory and dynamically creates component classes."""
        for filename in os.listdir(component_dir):
            if filename.endswith(".comp"):
                filepath = os.path.join(component_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)

                comp_name = data["name"]
                comp_fields = list(data["fields"].items())

                # Dynamically create a dataclass in memory
                new_comp_class = make_dataclass(comp_name, comp_fields)

                # Register it
                self.register_component(new_comp_class)
                print(f"Registered component: {comp_name}")

    def register_component(self, component_class):
        """Adds a component class to the registry."""
        self._component_registry[component_class.__name__] = component_class

    def get_component_class(self, name: str):
        """Returns the component class from the registry by name."""
        return self._component_registry.get(name)

    def create_entity_from_file(self, filepath: str) -> int:
        """Loads an entity definition from a file and builds it."""
        entity_id = self.next_entity_id
        self.next_entity_id += 1

        with open(filepath, 'r') as f:
            entity_data = json.load(f)

        for comp_name, comp_data in entity_data.get("components", {}).items():
            component_class = self.get_component_class(comp_name)
            if component_class:
                # Special handling for Renderable to create the pyglet shape
                if comp_name == "Renderable":
                    shape_type = comp_data.get("shape_type", "Rectangle")
                    props = comp_data.get("properties", {})

                    # --- FIX ---
                    # The shape needs x and y at creation. We get this from the
                    # Position component defined in the same entity file.
                    position_data = entity_data.get("components", {}).get("Position", {})
                    props['x'] = position_data.get('x', 0)
                    props['y'] = position_data.get('y', 0)
                    # --- END FIX ---

                    props['batch'] = self.main_batch

                    # Create the shape instance
                    if hasattr(shapes, shape_type):
                        shape_instance = getattr(shapes, shape_type)(**props)
                        component_instance = component_class(shape=shape_instance)
                    else:
                        print(f"Warning: Shape type '{shape_type}' not found.")
                        continue
                else:
                    # For all other components, just pass the data
                    component_instance = component_class(**comp_data)

                self.add_component(entity_id, component_instance)
            else:
                print(f"Warning: Component '{comp_name}' not found in registry.")

        print(f"Created entity '{entity_data.get('name', 'Unnamed')}' with ID {entity_id}")
        return entity_id

    def add_component(self, entity_id: int, component_instance):
        """Adds a component instance to a specific entity."""
        component_type = type(component_instance)
        self.component_stores[component_type][entity_id] = component_instance

    def get_components(self, *component_types):
        """A generator that yields entities and their specified components."""
        try:
            # Get the set of entities that have the first component type
            entity_set = set(self.component_stores[component_types[0]].keys())

            # Intersect this set with entities from other component stores
            for component_type in component_types[1:]:
                entity_set.intersection_update(self.component_stores[component_type].keys())

            # Yield the results for entities that are in the final set
            for entity_id in entity_set:
                yield entity_id, [self.component_stores[ctype][entity_id] for ctype in component_types]
        except (KeyError, IndexError):
            # This happens if a component type has no entities, which is fine.
            return
