from typing import Tuple


class Entity:
    """
    A generic object to represent all entities (players, npcs, etc)
    """
    def __init__(self, x: int, y: int, char: str, colour: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour

    def move(self, dx: int, dy: int) -> None:
        """
        Move the entity according to a dx and dy
        """
        self.x += dx
        self.y += dy
