from __future__ import annotations

from dataclasses import dataclass
from math import floor
from typing import TYPE_CHECKING
from typing_extensions import override

from rule_builder.rules import Has, Rule
from . import collectionsanity_data
from .options import PlanetRequirementType, CollectionsanityCowbearLogic

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
    milestone: int
    cowbear_logic: int

    @override
    def _instantiate(self, world: "OUAKatamariWorld") -> Rule.Resolved:
        return self.Resolved(milestone=self.milestone, cowbear_logic=self.cowbear_logic, player=world.player)

    class Resolved(Rule.Resolved):
        milestone: int
        cowbear_logic: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            reachable = set()

            for level, objects in collectionsanity_data.level_data.items():
                if state.has(level, self.player):
                    if level == "Cowbear Pasture":
                        if self.cowbear_logic == CollectionsanityCowbearLogic.option_exclude_all:
                            continue
                        elif self.cowbear_logic == CollectionsanityCowbearLogic.option_exclude_cowbears:
                            for object in objects:
                                if not collectionsanity_data.object_data[object]["cowbear"]:
                                    reachable.add(object)

                                    if len(reachable) >= self.milestone:
                                        return True

                            continue

                    reachable.update(objects)

                    if len(reachable) >= self.milestone:
                        return True

            return False
