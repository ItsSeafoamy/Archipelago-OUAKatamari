from __future__ import annotations

from math import floor
from typing import TYPE_CHECKING

from rule_builder.rules import Has

if TYPE_CHECKING:
    from .world import OUAKatamariWorld


def set_completion_condition(world: OUAKatamariWorld) -> None:
    planet_requirement = max(1, floor(world.number_of_planets * (world.options.planet_requirement.value / 100.0)))

    world.set_completion_rule(Has("Planet", count=planet_requirement))
