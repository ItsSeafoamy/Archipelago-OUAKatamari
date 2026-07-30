from __future__ import annotations

from dataclasses import dataclass
from math import floor
from typing import TYPE_CHECKING
from typing_extensions import override

from rule_builder.field_resolvers import FieldResolver, resolve_field
from rule_builder.rules import Has, Rule
from . import collectionsanity_data
from .options import PlanetRequirementType

if TYPE_CHECKING:
    from .world import OUAKatamariWorld


def set_completion_condition(world: OUAKatamariWorld) -> None:
    if world.options.planet_requirement_type == PlanetRequirementType.option_percentage:
        world.planet_requirement = floor(world.number_of_planets * (world.options.planet_requirement_percentage.value / 100.0))

    elif world.options.planet_requirement_type == PlanetRequirementType.option_count:
        world.planet_requirement = min(world.number_of_planets, world.options.planet_requirement_count.value)
        world.options.planet_requirement_count.value = world.planet_requirement

    world.set_completion_rule(Has("Planet", count=world.planet_requirement))


@dataclass()
class CollectionRule(Rule["OUAKatamariWorld"], game="Once Upon a Katamari"):
    milestone: int | FieldResolver

    @override
    def _instantiate(self, world: "OUAKatamariWorld") -> Rule.Resolved:
        return self.Resolved(milestone=resolve_field(self.milestone, world, int), player=world.player)

    class Resolved(Rule.Resolved):
        milestone: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            reachable = set()

            for level, objects in collectionsanity_data.level_data.items():
                if state.has(level, self.player):
                    reachable.update(objects)

                    if len(reachable) >= self.milestone:
                        return True

            return False
