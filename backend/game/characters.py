# The characters available in the selection pool
from game import elements
from game import archetypes
from game import regions


class Character:
    EXP_THRESHOLDS = [1000, 1750, 2500, 4000]
    
    PATH: dict[archetypes.Archetype, dict[str, int]] = { 
        archetypes.Archetype.DPS: {"health": 1100, "damage": 150},
        archetypes.Archetype.TANK : {"health": 1500, "damage": 100},
        archetypes.Archetype.RANGER: {"health": 900, "damage": 170},
        archetypes.Archetype.SUPPORT: {"health": 1000, "damage": 120}
    }
    
    GROWTH: dict[archetypes.Archetype,dict[str, int]] = {
        archetypes.Archetype.DPS: {'health': +10, 'damage': +15},
        archetypes.Archetype.TANK: {'health': +15, 'damage': +10},
        archetypes.Archetype.RANGER: {'health': +5, 'damage': +10},
        archetypes.Archetype.SUPPORT: {'health': +10, 'damage': +10}
    }
    
    def __init__(self, name, gender, origin:regions.Region ,  affinity: elements.Element, path: archetypes.Archetype, level=1, exp=0, health = None, damage = None):
        self.name = name
        self.gender = gender
        if not isinstance(origin, regions.Region):
            raise ValueError("...")
        else:
            self.origin = origin
        if not isinstance(affinity, elements.Element):
            raise ValueError("...")
        else:
            self.affinity = affinity
        if not isinstance(path, archetypes.Archetype):
            raise ValueError('...')
        else:
            self.path = path
        self.level = level
        self.exp = exp
        if health is None:
            self.health = self.PATH[path]['health']
        else:
            self.health = health
        if damage is None:
            self.damage = self.PATH[path]['damage']
        else:
            self.damage = damage
    
    def __str__(self):
        return f"""
Name: {self.name}
Class: {self.path.name}
Origin: {self.origin.name}
Gender: {self.gender}
Damage: {self.damage}
Health: {self.health}
Affinity: {self.affinity.name}
Level: {self.level}
Exp: {self.exp}
"""
    
    def level_up(self):
        while self.level -1 < len(self.EXP_THRESHOLDS) and self.exp >= self.EXP_THRESHOLDS[self.level - 1]:
            growth = self.GROWTH[self.path]
            self.health += growth["health"]
            self.damage += growth["damage"]
            self.level += 1
    
    def add_exp(self,amount):
        self.exp += amount
        self.level_up()
