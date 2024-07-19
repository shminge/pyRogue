from __future__ import annotations

from typing import Tuple, Iterator, List, TYPE_CHECKING

import tcod
import random

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity


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

    def intersects(self, other: RectangularRoom) -> bool:
        """
        Return True if this room overlaps with another room
        """
        return(
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        player: Entity
) -> GameMap:
    """
    Generates a new roomed dungeon
    """
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        newRoom = RectangularRoom(x=x, y=y, width=room_width, height=room_height)

        if any(newRoom.intersects(other_room) for other_room in rooms):
            continue # intersection, so new attempt

        # if it gets down here, the room is valid

        dungeon.tiles[newRoom.inner] = tile_types.floor

        if len(rooms) == 0:
            # this is the first room, so start the player here
            player.x, player.y = newRoom.centre
        else:
            # all other rooms we dig a tunnel to from the previous one
            for x, y in tunnel_between(rooms[-1].centre, newRoom.centre):
                dungeon.tiles[x, y] = tile_types.floor

        rooms.append(newRoom)

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