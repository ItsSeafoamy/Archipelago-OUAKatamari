from __future__ import annotations

from BaseClasses import Item, ItemClassification
from typing import TYPE_CHECKING

from . import game_data
from .game_data import LEVEL_OFFSET, COUSIN_OFFSET

if TYPE_CHECKING:
    from .world import OUAKatamariWorld

items_all = {}
items_groups = {
    "Levels": set(),
    "Cousins": set(),
    "Presents": set()
}

class OUAKatamariItem(Item):
    game = "Once Upon a Katamari"

def define_items() -> None:
    for level_name, level_data in game_data.data.items():
        items_all[level_name] = level_data["id"] + game_data.LEVEL_OFFSET
        items_groups["Levels"].add(level_name)

        for cousin_name, cousin_id in level_data["cousins"].items():
            items_all[cousin_name] = cousin_id + game_data.COUSIN_OFFSET
            items_groups["Cousins"].add(cousin_name)

        for present_name, present_id in level_data["present"].items():
            items_all[present_name] = present_id + game_data.PRESENT_OFFSET
            items_groups["Presents"].add(present_name)

    items_all["Planet"] = game_data.PLANET_OFFSET
    items_all["Stardust"] = game_data.FILLER_OFFSET

def create_item(world: OUAKatamariWorld, name: str) -> OUAKatamariItem:
    id = items_all[name]

    # levels (progression)
    if game_data.LEVEL_OFFSET <= id < game_data.COUSIN_OFFSET: classification = ItemClassification.progression
    # cousins + presents (filler)
    elif game_data.COUSIN_OFFSET <= id < game_data.PLANET_OFFSET: classification = ItemClassification.filler
    # planets (progression)
    elif game_data.PLANET_OFFSET <= id < game_data.FILLER_OFFSET: classification = ItemClassification.progression
    # junk (filler)
    else: classification = ItemClassification.filler

    return OUAKatamariItem(name, classification, id, world.player)

def create_all_items(world: OUAKatamariWorld) -> None:
    starting_levels = ["Tutorial", "As Large As Possible 1", "As Fast As Possible 1"]
    starting_cousins = ["The Prince"]

    itempool: list[Item] = []
    cosmetics: list[str] = []

    for level_name, level_data in game_data.data.items():
        if level_name in world.options.exclude_levels.value: continue

        # level unlocks
        if level_name not in starting_levels:
            itempool.append(world.create_item(level_name))

        # cousins
        if world.options.cousins:
            for cousin_name in level_data["cousins"].keys():
                if cousin_name not in starting_cousins:
                    cosmetics.append(cousin_name)

        # presents
        if world.options.presents:
            for present_name in level_data["present"].keys():
                cosmetics.append(present_name)

    number_of_levels = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player)) - number_of_levels

    if world.options.planet_shuffle.value > number_of_unfilled_locations:
        world.options.planet_shuffle.value = number_of_unfilled_locations

    # create planets
    number_of_planets = world.options.planet_shuffle.value
    itempool += [world.create_item("Planet") for _ in range(number_of_planets)]
    number_of_unfilled_locations -= number_of_planets
    world.number_of_planets = number_of_planets
    if world.options.planet_clear:
        world.number_of_planets += number_of_levels

    # create cousin & present items
    world.random.shuffle(cosmetics)
    number_of_cosmetics_needed = min(number_of_unfilled_locations, len(cosmetics))

    for i in range(number_of_cosmetics_needed):
        itempool.append(world.create_item(cosmetics[i]))
        number_of_unfilled_locations -= 1

    # fill leftover items with stardust
    itempool += [world.create_filler() for _ in range(number_of_unfilled_locations)]

    world.multiworld.itempool += itempool

    # give starting levels and cousin
    for name in starting_levels:
        world.push_precollected(world.create_item(name))
    for name in starting_cousins:
        world.push_precollected(world.create_item(name))

def get_random_filler_item() -> str:
    return "Stardust"