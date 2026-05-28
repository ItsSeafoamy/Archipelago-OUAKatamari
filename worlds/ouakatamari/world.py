from collections.abc import Mapping
from math import floor
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
        self.collectionsanity_locations = []

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

    def pre_fill(self) -> None:
        if self.options.collectionsanity.value:
            fill_count = floor(len(self.collectionsanity_locations) * (self.options.collectionsanity_local_fill.value / 100.0))
            self.random.shuffle(self.collectionsanity_locations)

            while fill_count > 0:
                loc = self.collectionsanity_locations.pop()
                loc.place_locked_item(self.create_item("Stardust"))
                fill_count -= 1

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "number_of_planets": self.number_of_planets,
            "planets_requirement": self.options.planet_requirement.value,
            "planets_on_clear": self.options.planet_clear.value,
            "death_link": self.options.death_link.value,
            "randomize_cousins": self.options.cousins.value,
            "randomize_presents": self.options.presents.value,
            "randomize_crowns": self.options.crowns.value,
            "collectionsanity": self.options.collectionsanity.value,
            "skip_tutorial": self.options.skip_tutorial.value,
        }
