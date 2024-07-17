from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity



class Action:
    """
    Default Action Class
    """
    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        'engine' is the scope that this action is being performed in
        'entity' is the thing that it is being performed by
        This should be overridden
        """
        raise NotImplementedError


class EscapeAction(Action):
    """
    Action Class to represent user quitting
    """
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class MovementAction(Action):
    """
    Movement Action, represented by the dx,dy of the movement
    """
    def __init__(self, dx, dy):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Move the player
        """
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return # destination is out of bounds
        if not engine.game_map.tiles["walkable"][dest_x,dest_y]:
            return # there's a wall

        entity.move(self.dx, self.dy)