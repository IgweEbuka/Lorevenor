
from game import elements
from game import archetypes
from game import regions


class Character:
    # Maximum level during one run.
    MAX_LEVEL = 5

    # Cumulative XP required to reach each level.
    EXP_THRESHOLDS = (1000, 1750, 2500, 4000)

    BASE_STATS = {
        archetypes.Archetype.DPS: {
            "health": 3000,
            "damage": 450
        },
        archetypes.Archetype.TANK: {
            "health": 4500,
            "damage": 300
        },
        archetypes.Archetype.RANGER: {
            "health": 2700,
            "damage": 510
        },
        archetypes.Archetype.SUPPORT: {
            "health": 3300,
            "damage": 360
        }
    }

    STAT_GROWTH = {
        archetypes.Archetype.DPS: {
            "health": 250,
            "damage": 100
        },
        archetypes.Archetype.TANK: {
            "health": 400,
            "damage": 65
        },
        archetypes.Archetype.RANGER: {
            "health": 200,
            "damage": 110
        },
        archetypes.Archetype.SUPPORT: {
            "health": 300,
            "damage": 80
        }
    }

    def __init__(
        self,
        name,
        gender,
        origin: regions.Region,
        affinity: elements.Element,
        path: archetypes.Archetype,
        level=1,
        exp=0,
        health=None,
        damage=None
    ):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Character name must be a non-empty string.")

        if not isinstance(gender, str) or not gender.strip():
            raise ValueError("Gender must be a non-empty string.")

        if not isinstance(origin, regions.Region):
            raise ValueError("Origin must be a valid Region.")

        if not isinstance(affinity, elements.Element):
            raise ValueError("Affinity must be a valid Element.")

        if not isinstance(path, archetypes.Archetype):
            raise ValueError("Path must be a valid Archetype.")

        if type(level) is not int or not 1 <= level <= self.MAX_LEVEL:
            raise ValueError("Level must be between 1 and 5.")

        if type(exp) is not int or exp < 0:
            raise ValueError("Experience must be a non-negative integer.")

        # XP must be sufficient for the supplied level.
        minimum_exp = 0 if level == 1 else self.EXP_THRESHOLDS[level - 2]

        if exp < minimum_exp:
            raise ValueError("Experience is too low for the supplied level.")

        # XP cannot already qualify the character for another level.
        if level < self.MAX_LEVEL and exp >= self.EXP_THRESHOLDS[level - 1]:
            raise ValueError("Experience is too high for the supplied level.")

        self.name = name.strip()
        self.gender = gender.strip()
        self.origin = origin
        self.affinity = affinity
        self.path = path

        self.level = level
        self.exp = exp

        stats = self.BASE_STATS[path]

        self.base_health = stats["health"] if health is None else health
        self.base_damage = stats["damage"] if damage is None else damage

        if type(self.base_health) is not int or self.base_health <= 0:
            raise ValueError("Health must be a positive integer.")

        if type(self.base_damage) is not int or self.base_damage <= 0:
            raise ValueError("Damage must be a positive integer.")

    @property
    def max_health(self):
        growth = self.STAT_GROWTH[self.path]["health"]
        return self.base_health + growth * (self.level - 1)

    @property
    def attack(self):
        growth = self.STAT_GROWTH[self.path]["damage"]
        return self.base_damage + growth * (self.level - 1)

    @property
    def damage(self):
        return self.attack

    def gain_experience(self, amount):
        if type(amount) is not int or amount < 0:
            raise ValueError("Experience gained must be a non-negative integer.")

        self.exp += amount
        return self.level_up()

    def add_exp(self, amount):
        return self.gain_experience(amount)

    def level_up(self):
        levels_gained = 0

        while (
            self.level < self.MAX_LEVEL
            and self.exp >= self.EXP_THRESHOLDS[self.level - 1]
        ):
            self.level += 1
            levels_gained += 1

        return levels_gained

    def reset_for_new_run(self):
        self.level = 1
        self.exp = 0

    def __str__(self):
        return (
            f"\nName: {self.name}"
            f"\nClass: {self.path.name}"
            f"\nOrigin: {self.origin.name}"
            f"\nGender: {self.gender}"
            f"\nAttack: {self.attack}"
            f"\nMaximum Health: {self.max_health}"
            f"\nAffinity: {self.affinity.name}"
            f"\nLevel: {self.level}"
            f"\nExp: {self.exp}\n"
        )
