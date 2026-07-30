from collections.abc import Mapping
from typing import Any

from Options import OptionError
from worlds.AutoWorld import World
from . import items, locations, regions, rules, web_world
from . import options as ouakatamari_options


class OUAKatamariWorld(World):
    """
    Once Upon a Katamari is a game where you roll up everything
    """

    game = "Once Upon a Katamari"

    web = web_world.OUAKatamariWebWorld()

    options_dataclass = ouakatamari_options.OUAKatamariOptions
    options: ouakatamari_options.OUAKatamariOptions

    locations.define_locations()
    items.define_items()

    location_name_to_id = locations.locations_all
    item_name_to_id = items.items_all
    item_name_groups = items.items_groups

    def __init__(self, world, player: int):
        super().__init__(world, player)
        self.number_of_planets = 0
        self.planet_requirement = 0

    def generate_early(self) -> None:
        excluded_levels = len(self.options.exclude_levels.value)
        max_levels = 47 - excluded_levels

        if max_levels == 0:
            raise OptionError("Attempted to exclude every single level. Please leave at least one enabled.")

        if self.options.starting_level_count.value > max_levels:
            self.options.starting_level_count.value = max_levels

    def create_regions(self) -> None:
        regions.create_regions(self)
        locations.create_locations(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.OUAKatamariItem:
        return items.create_item(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item(self)

    def set_rules(self) -> None:
        rules.set_completion_condition(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "mod_version": 0,
            "world_version": str(self.world_version.as_simple_string()),
            "number_of_planets": int(self.number_of_planets),
            "planet_requirement": int(self.planet_requirement),
            "planets_on_clear": bool(self.options.planet_clear.value),
            "death_link": bool(self.options.death_link.value),
            "randomize_cousins": bool(self.options.cousins.value),
            "randomize_presents": bool(self.options.presents.value),
            "randomize_crowns": bool(self.options.crowns.value),
            "collectionsanity": int(self.options.collectionsanity.value),
            "skip_tutorial": bool(self.options.skip_tutorial.value),
        }
