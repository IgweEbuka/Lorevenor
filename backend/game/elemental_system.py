
from game.elements import Element


class ElementalSystem:

    # Each element has one element it counters.
    COUNTERS = {
        Element.LIGHT: Element.SHADOW,
        Element.SHADOW: Element.WATER,
        Element.WATER: Element.EARTH,
        Element.EARTH: Element.WIND,
        Element.WIND: Element.CHAOS,
        Element.CHAOS: Element.LIGHT
    }

    # Damage modifiers.
    ADVANTAGE_MULTIPLIER = 1.25
    DISADVANTAGE_MULTIPLIER = 0.80
    NEUTRAL_MULTIPLIER = 1.00

    @classmethod
    def get_multiplier(cls, attacker: Element, defender: Element):
        if not isinstance(attacker, Element):
            raise ValueError("Attacker must have a valid Element.")

        if not isinstance(defender, Element):
            raise ValueError("Defender must have a valid Element.")

        # Attacker has an elemental advantage.
        if cls.COUNTERS[attacker] == defender:
            return cls.ADVANTAGE_MULTIPLIER

        # Defender counters the attacker.
        if cls.COUNTERS[defender] == attacker:
            return cls.DISADVANTAGE_MULTIPLIER

        # Neither element counters the other.
        return cls.NEUTRAL_MULTIPLIER

    @classmethod
    def calculate_damage(
        cls,
        base_damage: int,
        attacker: Element,
        defender: Element
    ):
        if type(base_damage) is not int or base_damage < 0:
            raise ValueError("Base damage must be a non-negative integer.")

        multiplier = cls.get_multiplier(attacker, defender)

        # Round to the nearest whole number.
        return int(base_damage * multiplier + 0.5)
