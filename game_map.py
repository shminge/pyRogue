import numpy as np

from tcod.console import Console

import tile_types


class GameMap:
    """
    Handles the map
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.tiles = np.full(shape=(width, height), fill_value=tile_types.wall, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Checks if a given x and y are within map bounds
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Places the map on the console
        """
        console.rgb[0:self.width, 0:self.height] = self.tiles["dark"]