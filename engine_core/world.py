import json
from collections import defaultdict
from pyglet import shapes
import components


class World:
    """
    The World class manages all entities, components, and their instantiation from files.
    """

    def __init__(self, batch):
        self.next_entity_id = 0
        self.component_stores = defaultdict(dict)
        self.main_batch = batch

        # --- Component Registry ---
        # This maps the string name of a component (from a file)
        # to the actual Python class. This is key for dynamic loading.
        self._component_registry = {}
        self.register_core_components()

    def register_core_components(self):
        """Finds and registers all component classes from the components module."""
        for name in dir(components):
            obj = getattr(components, name)
            if isinstance(obj, type) and not name.startswith("_"):
                # We assume any class in the components module is a component
                self.register_component(obj)

    def register_component(self, component_class):
        """Adds a component class to the registry."""
        self._component_registry[component_class.__name__] = component_class

    def create_entity_from_file(self, filepath: str) -> int:
        """Loads an entity definition from a file and builds it."""
        entity_id = self.next_entity_id
        self.next_entity_id += 1

        with open(filepath, 'r') as f:
            data = json.load(f)

        for comp_name, comp_data in data.get("components", {}).items():
            if comp_name in self._component_registry:
                component_class = self._component_registry[comp_name]

                # Special handling for Renderable to create the pyglet shape
                if component_class == components.Renderable:
                    shape_type = comp_data.get("shape_type", "Rectangle")
                    props = comp_data.get("properties", {})

                    # Add the batch to the properties
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
                print(f"Warning: Component '{comp_name}' not registered.")

        print(f"Created entity '{data.get('name', 'Unnamed')}' with ID {entity_id}")
        return entity_id

    def add_component(self, entity_id: int, component_instance):
        """Adds a component instance to a specific entity."""
        component_type = type(component_instance)
        self.component_stores[component_type][entity_id] = component_instance

    def get_components(self, *component_types):
        """Generator that yields entities and their specified components."""
        try:
            entity_set = set(self.component_stores[component_types[0]].keys())
            for component_type in component_types[1:]:
                entity_set.intersection_update(self.component_stores[component_type].keys())
            for entity_id in entity_set:
                yield entity_id, [self.component_stores[ctype][entity_id] for ctype in component_types]
        except (KeyError, IndexError):
            return
