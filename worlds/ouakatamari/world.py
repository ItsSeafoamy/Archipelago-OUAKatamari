from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World
from . import items, locations, regions, rules, web_world
from . import options as ouakatamari_options


class OUAKatamariWorld(World):
    """
    Once Upon a Katamari is a game where you roll up everything
    """

    game = "Once Upon a Katamari"

    web = web_world.OUAKatamariWebWorld()

    number_of_planets = 0

    options_dataclass = ouakatamari_options.OUAKatamariOptions
    options: ouakatamari_options.OUAKatamariOptions

    locations.define_locations()
    items.define_items()

    location_name_to_id = locations.locations_all
    item_name_to_id = items.items_all
    item_name_groups = items.items_groups

    def generate_early(self) -> None:
        excluded_levels = len(self.options.exclude_levels.value)
        max_levels = 47 - excluded_levels

        if self.options.starting_level_count.value > max_levels:
            self.options.starting_level_count.value = max_levels

    def create_regions(self) -> None:
        regions.create_regions(self)
        locations.create_locations(self)

    def set_rules(self) -> None:
        rules.set_completion_condition(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.OUAKatamariItem:
        return items.create_item(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "number_of_planets": self.number_of_planets,
            "planets_requirement": self.options.planet_requirement.value,
            "planets_on_clear": self.options.planet_clear.value,
            "death_link": self.options.death_link.value,
            "randomize_cousins": self.options.cousins.value,
            "randomize_presents": self.options.presents.value,
            "randomize_crowns": self.options.crowns.value,
            "skip_tutorial": self.options.skip_tutorial.value,
        }
