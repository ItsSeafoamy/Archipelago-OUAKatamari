from __future__ import annotations

from math import floor
from typing import TYPE_CHECKING

from rule_builder.rules import Has

if TYPE_CHECKING:
    from .world import OUAKatamariWorld


def set_completion_condition(world: OUAKatamariWorld) -> None:
    if world.options.planet_requirement_type == 0: # Percentage
        world.planet_requirement = floor(world.number_of_planets * (world.options.planet_requirement_percentage.value / 100.0))

    elif world.options.planet_requirement_type == 1: # Count
        world.planet_requirement = min(world.number_of_planets, world.options.planet_requirement_count.value)
        world.options.planet_requirement_count.value = world.planet_requirement

    world.set_completion_rule(Has("Planet", count=world.planet_requirement))
