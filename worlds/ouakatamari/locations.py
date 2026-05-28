from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location
from rule_builder.rules import HasAny
from . import game_data
from .collectionsanity_data import collection_data

if TYPE_CHECKING:
    from .world import OUAKatamariWorld

locations_all = {}


class OUAKatamariLocation(Location):
    game = "Once Upon a Katamari"


def define_locations() -> None:
    for level_name, level_data in game_data.data.items():
        locations_all[f"{level_name} - Clear"] = level_data["id"] + game_data.LEVEL_OFFSET
        locations_all[f"{level_name} - Planet"] = level_data["id"] + game_data.PLANET_OFFSET

        for cousin_name, cousin_id in level_data["cousins"].items():
            locations_all[f"{level_name} - Cousin: {cousin_name}"] = cousin_id + game_data.COUSIN_OFFSET

        for present_name, present_id in level_data["present"].items():
            locations_all[f"{level_name} - Present"] = present_id + game_data.PRESENT_OFFSET

        if level_data["crown_index"] != -1:
            for i in range(3):
                locations_all[f"{level_name} - Crown {str(i+1)}"] = level_data["crown_index"] + i + game_data.CROWN_OFFSET

    for object_name, object_data in collection_data.items():
        locations_all[f"Collectionsanity: {object_name}"] = object_data["id"] + game_data.COLLECTIONSANITY_OFFSET

def create_locations(world: OUAKatamariWorld) -> None:
    for level_name, level_data in game_data.data.items():
        if level_name in world.options.exclude_levels.value: continue
        if level_name == "Tutorial" and world.options.skip_tutorial.value: continue

        region = world.get_region(level_name)

        # level clear check
        loc = OUAKatamariLocation(world.player,
                                  f"{level_name} - Clear",
                                  level_data["id"] + game_data.LEVEL_OFFSET,
                                  region)
        region.locations.append(loc)

        # planet check
        if world.options.planet_clear:
            loc = OUAKatamariLocation(world.player,
                                      f"{level_name} - Planet",
                                      level_data["id"] + game_data.PLANET_OFFSET,
                                      region)
            loc.place_locked_item(world.create_item("Planet"))
            region.locations.append(loc)

        # cousin checks
        if world.options.cousins:
            for cousin_name, cousin_id in level_data["cousins"].items():
                loc = OUAKatamariLocation(world.player,
                                          f"{level_name} - Cousin: {cousin_name}",
                                          cousin_id + game_data.COUSIN_OFFSET,
                                          region)
                region.locations.append(loc)

        # present checks
        if world.options.presents:
            for present_name, present_id in level_data["present"].items():
                loc = OUAKatamariLocation(world.player,
                                          f"{level_name} - Present",
                                          present_id + game_data.PRESENT_OFFSET,
                                          region)
                region.locations.append(loc)

        # crown checks
        if world.options.crowns and level_data["crown_index"] != -1:
            for i in range(3):
                loc = OUAKatamariLocation(world.player,
                                          f"{level_name} - Crown {str(i+1)}",
                                          level_data["crown_index"] + i + game_data.CROWN_OFFSET,
                                          region)
                region.locations.append(loc)

    # collectionsanity
    if world.options.collectionsanity:
        region = world.get_region("Menu")

        for object_name, object_data in collection_data.items():
            levels = [
                level_name for level_name in object_data["levels"]
                if level_name not in world.options.exclude_levels.value
                if level_name != "That Hole..."
            ]

            if not levels: continue

            loc = OUAKatamariLocation(world.player,
                                      f"Collectionsanity: {object_name}",
                                      object_data["id"] + game_data.COLLECTIONSANITY_OFFSET,
                                      region)

            region.locations.append(loc)
            world.set_rule(loc, HasAny(*levels))
            world.collectionsanity_locations.append(loc)
