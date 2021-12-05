from typing import TypeVar, Set, Dict

T = TypeVar("T")


def bfs(root: T, root_to_neighbors: Dict[T, Set[T]]) -> Set[T]:
    """
    Find all of the other cities that are reachable from a given root city and mapping from city to other cities.
    Returns a set of cities that a user can reach from the root.

    ASSUMPTION: Assumes directed graph. This means the keys are the starting city, and the edges go in the direction
    "towards" the city in the set of values.
    """
    frontier = [root]
    seen_cities = set()
    while frontier:
        city = frontier.pop(0)
        seen_cities.add(city)
        for neighbor in root_to_neighbors.get(city, set()):
            if neighbor not in seen_cities:
                frontier.append(neighbor)
    return seen_cities
