from __future__ import annotations

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups

class OUAKatamariWebWorld(WebWorld):
    game = "Once Upon a Katamari"

    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Once Upon a Katamari for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Seafoamy"]
    )

    tutorials = [setup_en]

    option_groups = option_groups