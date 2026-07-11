from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from . import game_data

if TYPE_CHECKING:
    from .world import OUAKatamariWorld

items_all = {}
items_groups = {
    "Levels": set(),
    "Cousins": set(),
    "Presents": set(),
    "Freebies": set(),
    "Traps": set(),
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

    for freebie_name, freebie_id in game_data.freebie_data.items():
        items_all[freebie_name] = freebie_id + game_data.FREEBIE_OFFSET
        items_groups["Freebies"].add(freebie_name)
        items_all[f"Super {freebie_name}"] = freebie_id + game_data.FREEBIE_SUPER_OFFSET
        items_groups["Freebies"].add(f"Super {freebie_name}")

    for trap_name, trap_id in game_data.trap_data.items():
        items_all[trap_name] = trap_id + game_data.TRAP_OFFSET
        items_groups["Traps"].add(trap_name)


def create_item(world: OUAKatamariWorld, name: str) -> OUAKatamariItem:
    id = items_all[name]

    # levels (progression)
    if game_data.LEVEL_OFFSET <= id < game_data.COUSIN_OFFSET:
        classification = ItemClassification.progression
    # cousins + presents (filler)
    elif game_data.COUSIN_OFFSET <= id < game_data.PLANET_OFFSET:
        classification = ItemClassification.filler
    # planets (progression)
    elif game_data.PLANET_OFFSET <= id < game_data.FILLER_OFFSET:
        classification = ItemClassification.progression
    # junk (filler)
    elif game_data.FILLER_OFFSET <= id < game_data.FREEBIE_OFFSET:
        classification = ItemClassification.filler
    # freebies (useful)
    elif game_data.FREEBIE_OFFSET <= id < game_data.TRAP_OFFSET:
        classification = ItemClassification.useful
    # traps
    else:
        classification = ItemClassification.trap

    return OUAKatamariItem(name, classification, id, world.player)


def create_all_items(world: OUAKatamariWorld) -> None:
    starting_levels = []
    starting_cousins = []

    if not world.options.skip_tutorial.value:
        starting_levels.append("Tutorial")

    # random starting levels
    level_names = sorted(game_data.data.keys() - starting_levels - world.options.exclude_levels.value - {"Tutorial"})
    world.random.shuffle(level_names)
    for _ in range(world.options.starting_level_count):
        starting_levels.append(level_names.pop())

    itempool: list[Item] = []
    cousins: list[str] = []
    cosmetics: list[str] = []

    for level_name, level_data in game_data.data.items():
        if level_name in world.options.exclude_levels.value: continue
        if level_name == "Tutorial" and world.options.skip_tutorial.value: continue

        # level unlocks
        if level_name not in starting_levels:
            itempool.append(world.create_item(level_name))

        # cousins
        if world.options.cousins.value:
            for cousin_name in level_data["cousins"].keys():
                cousins.append(cousin_name)

        # presents
        if world.options.presents.value:
            for present_name in level_data["present"].keys():
                cosmetics.append(present_name)

    if not world.options.cousins.value:
        starting_cousins.append("The Prince")
    else:
        world.random.shuffle(cousins)
        starting_cousins.append(cousins.pop())
        cosmetics.extend(cousins)

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

    # fill leftover items with filler
    itempool += [world.create_filler() for _ in range(number_of_unfilled_locations)]

    world.multiworld.itempool += itempool

    # give starting levels and cousin
    for name in starting_levels:
        world.push_precollected(world.create_item(name))
    for name in starting_cousins:
        world.push_precollected(world.create_item(name))


def get_random_filler_item(world: OUAKatamariWorld) -> str:
    # junk/traps
    if world.random.randint(0, 99) < world.options.junk_trap_chance.value:
        stardust_weight = world.options.stardust_weight
        washpan_weight = world.options.washpan_weight
        spider_weight = world.options.spider_weight
        fog_weight = world.options.fog_weight
        trap_weights = stardust_weight + washpan_weight + spider_weight + fog_weight

        if trap_weights > 0:
            return world.random.choices(
                population=["Stardust"] + list(game_data.trap_data.keys()),
                weights=[stardust_weight, washpan_weight, spider_weight, fog_weight],
                k=1
            )[0]

    # freebies
    rocket_weight = world.options.rocket_weight
    magnet_weight = world.options.magnet_weight
    sonar_weight = world.options.sonar_weight
    timer_weight = world.options.timer_weight
    mushroom_weight = world.options.mushroom_weight
    ice_axe_weight = world.options.ice_axe_weight
    freebie_weights = rocket_weight + magnet_weight + sonar_weight + timer_weight + mushroom_weight + ice_axe_weight

    if freebie_weights > 0:
        selected = world.random.choices(
            population=list(game_data.freebie_data.keys()),
            weights=[rocket_weight, magnet_weight, sonar_weight, timer_weight, mushroom_weight, ice_axe_weight],
            k=1
        )[0]

        if world.random.randint(0, 99) < world.options.super_freebie_chance.value:
            selected = f"Super {selected}"

        return selected

    # if all weights were zero, just return Stardust
    return "Stardust"
