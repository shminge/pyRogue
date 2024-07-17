from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg", "3B"),
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", np.bool), # whether the tile is solid
        ("transparent", np.bool), # whether the tile blocks sight
        ("dark", graphic_dt), # graphics for when the tile is not rendered
    ]
)


def new_tile(
        *,
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int,int,int], Tuple[int,int,int]]
) -> np.ndarray:
    """
    helpful function to define tile types
    """
    return np.array((walkable, transparent, dark), dtype=tile_dt)


floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(
        ord(" "),
        (255, 255, 255),
        (50, 50, 150)
    )
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(
        ord(" "),
        (255, 255, 255),
        (0, 0, 100)
    )
)
