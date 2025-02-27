"""
Player structure

Includes current player information, and preferences
"""
from dataclasses import dataclass, field
import os
from tomlkit import parse, TOMLDocument, document
from typing import Callable
from abacura import Config


# class Consumable:
#     short_name: str = ''
#     inventory_name: str = ''
#     min_quantity: int = 0
#     extra_quantity: int = 0
#     buff: str = ''
#     acquire_vnum: str = ''
#     acquire_command: str = ''
#     acquire_hours: tuple = (0, 24)
#     acquire_cost: int = 0
#     check_function: Callable = lambda x: True


@dataclass(slots=True)
class PlayerSkill:
    skill: str = ''
    clevel: int = 0
    mp_sp: int = 0
    skilled: int = 0
    rank: int = 0
    trained_rank: int = 0
    rank_bonus: int = 0
    locked: bool = False


@dataclass(slots=True)
class PlayerCharacter:
    """Kallisti specific player information"""
    _config: TOMLDocument = field(default_factory=document)
    home_vnum: str = ''
    egress_vnum: str = '3001'
    recall_vnum: str = '3001'
    char_name: str = ''
    skills: dict[str, PlayerSkill] = field(default_factory=dict)
    buffs: list[str] = field(default_factory=list)
    # consumables: list[Consumable] = field(default_factory=list)
    target_heros: int = 0

    def load(self, data_dir: str, name: str):
        """Load a player character record from disk"""
        self.char_name = name.lower()

        char_file = os.path.join(data_dir, self.char_name)
        char_file = f"{char_file}.player"
        if not os.path.isfile(char_file):
            with open(char_file, 'w', encoding="UTF-8") as fp:
                fp.write(f"char_name = '{self.char_name}'\n")

        self._config = parse(open(char_file, "r", encoding="UTF-8").read())
        for key, val in self._config.items():
            if hasattr(self, key):
                setattr(self, key, val)
