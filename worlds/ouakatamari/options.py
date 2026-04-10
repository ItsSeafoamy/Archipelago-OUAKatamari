from __future__ import annotations

from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Toggle, OptionSet, DeathLink, OptionGroup
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
    Determines whether rolling up cousins will grant checks (up to 69 locations).
    """

    display_name = "Randomize Cousins"


class Presents(Toggle):
    """
    Determines whether rolling up presents will grant checks (up to 39 locations).
    """

    display_name = "Randomize Presents"


class Crowns(Toggle):
    """
    Determines whether rolling up crowns will grant checks (up to 141 locations).
    """

    display_name = "Randomize Crowns"


class SkipTutorial(Toggle):
    """
    Skips the tutorial.
    """

    display_name = "Skip Tutorial"


class StartingLevels(Range):
    """
    The number of levels that you will start with.
    """

    display_name = "Starting Level Count"
    range_start = 1
    range_end = 47
    default = 5


class ExcludeLevels(OptionSet):
    """
    Prevents these levels from showing up in the seed.
    """

    display_name = "Exclude Levels"
    valid_keys = set(data.keys() - {"Tutorial"})


class RocketWeight(Range):
    """
    The weight of Rockets in the freebie pool.
    """

    display_name = "Rocket Weight"
    range_start = 0
    range_end = 100
    default = 50


class MagnetWeight(Range):
    """
    The weight of Magnets in the freebie pool.
    """

    display_name = "Magnet Weight"
    range_start = 0
    range_end = 100
    default = 50


class SonarWeight(Range):
    """
    The weight of Sonars in the freebie pool.
    """

    display_name = "Sonar Weight"
    range_start = 0
    range_end = 100
    default = 50


class TimerWeight(Range):
    """
    The weight of Timers in the freebie pool.
    """

    display_name = "Timer Weight"
    range_start = 0
    range_end = 100
    default = 50


class MushroomWeight(Range):
    """
    The weight of Mushrooms in the freebie pool.
    This freebie increases your Katamari's size by 10%.
    """

    display_name = "Mushroom Weight"
    range_start = 0
    range_end = 100
    default = 0


class IceAxeWeight(Range):
    """
    The weight of Ice Axes (Also known as "Pickels") in the freebie pool.
    This freebie allows you to scale walls higher and faster.
    """

    display_name = "Ice Axe Weight"
    range_start = 0
    range_end = 100
    default = 0


class SuperFreebieChance(Range):
    """
    The chance a freebie will be replaced by its super variant.
    Super Mushroom increases your Katamari's size by 20%.
    All other super freebies last twice as long as their regular variant.
    """

    display_name = "Super Freebie Chance"
    range_start = 0
    range_end = 100
    default = 0


class JunkTrapChance(Range):
    """
    The chance an unfilled location will be filled with a junk or trap item.
    """

    display_name = "Junk/Trap Chance"
    range_start = 0
    range_end = 100
    default = 20


class StardustWeight(Range):
    """
    The weight of Stardust (junk item) in the junk/trap pool.
    """

    display_name = "Stardust Weight"
    range_start = 0
    range_end = 100
    default = 50


class WashpanWeight(Range):
    """
    The weight of Washpan Traps in the junk/trap pool.
    This trap decreases your Katamari's size by 10%.
    """

    display_name = "Washpan Trap Weight"
    range_start = 0
    range_end = 100
    default = 0


class SpiderWeight(Range):
    """
    The weight of Spider Traps in the junk/trap pool.
    This trap causes you to move slower.
    """

    display_name = "Spider Trap Weight"
    range_start = 0
    range_end = 100
    default = 0


@dataclass
class OUAKatamariOptions(PerGameCommonOptions):
    planet_clear: PlanetClear
    planet_shuffle: PlanetShuffle
    planet_requirement: PlanetRequirement
    death_link: DeathLink
    cousins: Cousins
    presents: Presents
    crowns: Crowns
    skip_tutorial: SkipTutorial
    starting_level_count: StartingLevels
    exclude_levels: ExcludeLevels
    rocket_weight: RocketWeight
    magnet_weight: MagnetWeight
    sonar_weight: SonarWeight
    timer_weight: TimerWeight
    mushroom_weight: MushroomWeight
    ice_axe_weight: IceAxeWeight
    super_freebie_chance: SuperFreebieChance
    junk_trap_chance: JunkTrapChance
    stardust_weight: StardustWeight
    washpan_weight: WashpanWeight
    spider_weight: SpiderWeight


option_groups = [
    OptionGroup(
        "Freebie Options",
        [RocketWeight, MagnetWeight, SonarWeight, TimerWeight, MushroomWeight, IceAxeWeight, SuperFreebieChance]
    ),
    OptionGroup(
        "Junk & Trap Options",
        [JunkTrapChance, StardustWeight, WashpanWeight, SpiderWeight]
    )
]
