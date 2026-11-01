
from game.characters import Character
from game.combatant import Combatant
from game import elements, archetypes, regions


def create_test_combatant():
    character = Character(
        "Night",
        "Male",
        regions.Region(elements.Element.SHADOW),
        elements.Element.SHADOW,
        archetypes.Archetype.DPS
    )
    return Combatant(character)


def test_combatant_starts_with_full_health():
    combatant = create_test_combatant()

    assert combatant.current_health == 3000
    assert combatant.max_health == 3000
    assert combatant.is_alive is True


def test_combatant_takes_damage():
    combatant = create_test_combatant()

    combatant.take_damage(1000)

    assert combatant.current_health == 2000


def test_shield_absorbs_damage_first():
    combatant = create_test_combatant()

    combatant.add_shield(500)
    combatant.take_damage(800)

    assert combatant.shield == 0
    assert combatant.current_health == 2700


def test_combatant_can_heal():
    combatant = create_test_combatant()

    combatant.take_damage(1000)
    combatant.heal(500)

    assert combatant.current_health == 2500


def test_healing_cannot_exceed_maximum_health():
    combatant = create_test_combatant()

    combatant.take_damage(500)
    combatant.heal(1000)

    assert combatant.current_health == 3000


def test_combatant_is_defeated_at_zero_health():
    combatant = create_test_combatant()

    combatant.take_damage(5000)

    assert combatant.current_health == 0
    assert combatant.is_alive is False


def test_defeated_combatant_cannot_be_healed():
    combatant = create_test_combatant()

    combatant.take_damage(5000)
    combatant.heal(1000)

    assert combatant.current_health == 0
    assert combatant.is_alive is False
