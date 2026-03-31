from __future__ import annotations

from math import floor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import OUAKatamariWorld


def set_completion_condition(world: OUAKatamariWorld) -> None:
    planet_requirement = max(1, floor(world.number_of_planets * (world.options.planet_requirement.value / 100.0)))

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Planet", world.player, planet_requirement)