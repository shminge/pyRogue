from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler



class Engine:
    """
    This class will handle 'running' the game
    """
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map

        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        """
        Handles the events systematically
        """
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov()

    def update_fov(self) -> None:
        """
        Recompute the visible area
        """
        self.game_map.visible[:] = compute_fov(
            transparency=self.game_map.tiles["transparent"],
            pov=(self.player.x, self.player.y),
            radius=8
        )

        # if a tile is visible it should also be explored

        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        """
        Draws stuff on the screen
        """

        self.game_map.render(console)

        for entity in self.entities:
            if self.game_map.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.colour)

        context.present(console)

        console.clear()




