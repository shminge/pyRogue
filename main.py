#!/usr/bin/env python3
import tcod

from engine import Engine
from input_handlers import EventHandler
from entity import Entity
from roomprocgen import generate_dungeon


def main() -> None:
    """
    This function holds the main game loop
    """

    # basic setup
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 50


    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = Entity(x=int(screen_width/2), y=int(screen_height/2), char="@", colour=(255, 255, 255))
    npc = Entity(x=int(screen_width/2-5), y=int(screen_height/2), char="@", colour=(255, 255, 0))
    entities = {npc, player}

    game_map = generate_dungeon(map_width=map_width, map_height=map_height)

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="pyRogue",
        vsync=True
    ) as context:

        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()
            engine.handle_events(events)







if __name__ == "__main__":
    main()