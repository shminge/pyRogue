from typing import Tuple, Iterator

import tcod
import random

from game_map import GameMap
import tile_types


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height


    @property
    def centre(self) -> Tuple[int, int]:
        """
        yields the centre of the room
        """
        centre_x = int((self.x1+self.x2)/2)
        centre_y = int((self.y1+self.y2)/2)
        return centre_x, centre_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """
        Gives in slices the interior area of the room (walls excluded
        """
        return slice(self.x1+1, self.x2), slice(self.y1+1, self.y2)



def generate_dungeon(map_width: int, map_height: int) -> GameMap:
    dungeon = GameMap(width=map_width, height=map_height)

    room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor

    for x, y in tunnel_between(room_1.centre, room_2.centre):
        dungeon.tiles[x, y] = tile_types.floor
    return dungeon


def tunnel_between(start: Tuple[int, int], end: Tuple[int,int]) -> Iterator[Tuple[int, int]]:
    """
    Returns an L shaped tunnel between two points
    """
    x1, y1 = start
    x2, y2 = end
    if random.random() > 0.5:
        corner_x = x2
        corner_y = y1
    else:
        corner_x = x1
        corner_y = y2

    for x, y in tcod.los.bresenham(start=(x1, y1), end=(corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham(start=(corner_x, corner_y), end=(x2, y2)).tolist():
        yield x, y