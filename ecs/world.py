from collections import defaultdict


class World:
    """
    The World class manages all entities and their components.
    It provides methods for creating entities and accessing components.
    """
    def __init__(self):
        self.next_entity_id = 0
        self.component_stores = defaultdict(dict)

    def create_entity(self) -> int:
        """
        Creates a new entity and returns its ID.
        An entity is simply a unique integer.
        """
        entity_id = self.next_entity_id
        self.next_entity_id += 1
        return entity_id

    def add_component(self, entity_id: int, component_instance):
        """
        Adds a component instance to a specific entity.
        The component's type is used as the key for the store.
        """
        component_type = type(component_instance)
        self.component_stores[component_type][entity_id] = component_instance

    def get_components(self, *component_types):
        """
        A generator that yields entities and their specified components
        if the entity has ALL the requested component types.

        Example Usage:
        for entity_id, (pos, vel) in world.get_components(Position, Velocity):
            # ... do something with pos and vel ...
        """
        try:
            # Get the set of entities that have the first component type
            entity_set = set(self.component_stores[component_types[0]].keys())

            # Intersect this set with entities from other component stores
            for component_type in component_types[1:]:
                entity_set.intersection_update(self.component_stores[component_type].keys())

            # Yield the results for entities that are in the final set
            for entity_id in entity_set:
                components = [self.component_stores[ctype][entity_id] for ctype in component_types]
                yield entity_id, components
        except (KeyError, IndexError):
            # This happens if a component type has no entities, which is fine.
            # We just return, as there are no entities to yield.
            return

