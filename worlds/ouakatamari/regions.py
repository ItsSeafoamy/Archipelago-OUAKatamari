from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.rules import Has
from .game_data import data

if TYPE_CHECKING:
    from .world import OUAKatamariWorld


def create_regions(world: OUAKatamariWorld) -> None:
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    for name in data.keys():
        if name in world.options.exclude_levels.value: continue

        # create region
        region = Region(name, world.player, world.multiworld)
        world.multiworld.regions.append(region)

        # connect to menu
        menu.connect(region, "Menu to " + name, Has(name))
