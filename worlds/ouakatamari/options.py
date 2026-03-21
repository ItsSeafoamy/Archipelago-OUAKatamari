from __future__ import annotations
from dataclasses import dataclass
from Options import PerGameCommonOptions, Range, Toggle, OptionSet, DeathLink

from .game_data import data

class PlanetClear(Toggle):
    """
    Determines if clearing levels gives the player Planets (up to 48 planets)
    """

    display_name = "Level Clears Gives Planets?"

class PlanetShuffle(Range):
    """
    The total amount of planets to be added to the item pool.
    """

    display_name = "Planets in Item Pool"

    range_start = 1
    range_end = 250
    default = 80

class PlanetRequirement(Range):
    """
    The percentage of total planets needed to unlock the final level "That Hole..." and beat the game.
    """

    display_name = "Planet Requirement Percentage"

    range_start = 0
    range_end = 100
    default = 60

class Cousins(Toggle):
    """
    Determines whether rolling up cousins will grant checks (up to 69 locations)
    """

    display_name = "Randomize Cousins"

class Presents(Toggle):
    """
    Determines whether rolling up presents will grant checks (up to 39 locations)
    """

    display_name = "Randomize Presents"

class Crowns(Toggle):
    """
    Determines whether rolling up crowns will grant checks (up to 141 locations)
    """

    display_name = "Randomize Crowns"

class StartingLevels(Range):
    """
    The number of levels that you will start with.
    You will always start with "Tutorial" and "As Large As Possible 1".
    """

    display_name = "Starting Level Count"
    range_start = 2
    range_end = 48
    default = 5

class ExcludeLevels(OptionSet):
    """
    Prevents these levels from showing up in the seed.
    """

    display_name = "Exclude Levels"
    starting_levels = {"Tutorial", "As Large As Possible 1"}
    valid_keys = set(data.keys() - starting_levels)


@dataclass
class OUAKatamariOptions(PerGameCommonOptions):
    planet_clear: PlanetClear
    planet_shuffle: PlanetShuffle
    planet_requirement: PlanetRequirement
    death_link: DeathLink
    cousins: Cousins
    presents: Presents
    crowns: Crowns
    starting_level_count: StartingLevels
    exclude_levels: ExcludeLevels