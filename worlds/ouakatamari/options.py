from __future__ import annotations

from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Toggle, OptionSet, DeathLink, OptionGroup, DefaultOnToggle, Choice
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


class PlanetRequirementType(Choice):
    """
    Whether the goal is defined as a percentage of planets in the pool, or a specific amount of planets.
    """

    display_name = "Planets Requirement Type"

    option_percentage = 0
    option_count = 1
    default = 0


class PlanetRequirementPercentage(Range):
    """
    The percentage of total planets needed to unlock the final level "That Hole..." and beat the game.
    Only used if 'Planet Requirement Type' is 'percentage'
    """

    display_name = "Planet Requirement Percentage"

    range_start = 0
    range_end = 100
    default = 60


class PlanetRequirementCount(Range):
    """
    The amount of total planets needed to unlock the final level "That Hole..." and beat the game.
    Only used if 'Planet Requirement Type' is 'count'
    """

    display_name = "Planets Requirement Count"

    range_start = 0
    range_end = 250
    default = 50


class Cousins(DefaultOnToggle):
    """
    Determines whether rolling up cousins will grant checks (up to 69 locations).
    """

    display_name = "Randomize Cousins"


class Presents(DefaultOnToggle):
    """
    Determines whether rolling up presents will grant checks (up to 39 locations).
    """

    display_name = "Randomize Presents"


class Crowns(DefaultOnToggle):
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


class Collectionsanity(Choice):
    """
    Adds checks for rolling up objects in the collection.

    Individual: Grants a check for every individual unique object in the collection. E.g. Collectionsanity: Tomato
    Milestones: Grants a check for every x amount of unique objects rolled up. E.g. Collectionsanity: 100 objects
    """

    display_name = "Collectionsanity"
    option_disabled = 0
    option_individual = 1
    option_milestones = 2
    default = 0


class CollectionsanityMilestones(Range):
    """
    How many unique objects must be rolled up before granting a check.
    Only used when Collectionsanity is 'milestones'.
    """

    display_name = "Milestones"
    range_start = 1
    range_end = 3637
    default = 100


class CollectionsanityOutOfLogic(Range):
    """
    How many unique objects that are possible to roll up are considered out of logic.
    e.g. If you can roll up 100 unique objects, but set this value to 20, 80 will be considered in logic.
    Only used when Collectionsanity is 'milestones'.
    """

    display_name = "Out of Logic"
    range_start = 0
    range_end = 3636
    default = 100


class CollectionsanityLocalFill(Range):
    """
    The percentage of collectionsanity checks that will be forced to have a local junk item.
    Recommended to keep high when using individual mode or a very low milestone such as 1.
    Recommended to turn down when using higher milestones.
    """

    display_name = "Local Fill Percentage"
    range_start = 0
    range_end = 100
    default = 90


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


class FogWeight(Range):
    """
    The weight of Fog Traps in the junk/trap pool.
    This trap adds the fog from 'Lots of Yokai', and will slowly dissipate over time.
    Does not activate while in 'Lots of Yokai'.
    """

    display_name = "Fog Trap Weight"
    range_start = 0
    range_end = 100
    default = 0


@dataclass
class OUAKatamariOptions(PerGameCommonOptions):
    planet_clear: PlanetClear
    planet_shuffle: PlanetShuffle
    planet_requirement_type: PlanetRequirementType
    planet_requirement_percentage: PlanetRequirementPercentage
    planet_requirement_count: PlanetRequirementCount
    death_link: DeathLink
    cousins: Cousins
    presents: Presents
    crowns: Crowns
    skip_tutorial: SkipTutorial
    starting_level_count: StartingLevels
    exclude_levels: ExcludeLevels
    collectionsanity: Collectionsanity
    collectionsanity_milestones: CollectionsanityMilestones
    collectionsanity_out_of_logic: CollectionsanityOutOfLogic
    collectionsanity_local_fill: CollectionsanityLocalFill
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
    fog_weight: FogWeight


option_groups = [
    OptionGroup(
        "Collectionsanity Options",
        [Collectionsanity, CollectionsanityMilestones, CollectionsanityOutOfLogic, CollectionsanityLocalFill],
    ),
    OptionGroup(
        "Freebie Options",
        [RocketWeight, MagnetWeight, SonarWeight, TimerWeight, MushroomWeight, IceAxeWeight, SuperFreebieChance],
    ),
    OptionGroup(
        "Junk & Trap Options",
        [JunkTrapChance, StardustWeight, WashpanWeight, SpiderWeight, FogWeight],
    )
]
