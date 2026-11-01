
import pytest

from game.elements import Element
from game.elemental_system import ElementalSystem


def test_every_element_has_one_counter():
    assert len(ElementalSystem.COUNTERS) == 6

    for element in Element:
        assert element in ElementalSystem.COUNTERS


@pytest.mark.parametrize(
    "attacker, defender",
    [
        (Element.LIGHT, Element.SHADOW),
        (Element.SHADOW, Element.WATER),
        (Element.WATER, Element.EARTH),
        (Element.EARTH, Element.WIND),
        (Element.WIND, Element.CHAOS),
        (Element.CHAOS, Element.LIGHT)
    ]
)
def test_elemental_advantage(attacker, defender):
    assert ElementalSystem.get_multiplier(attacker, defender) == 1.25


@pytest.mark.parametrize(
    "attacker, defender",
    [
        (Element.SHADOW, Element.LIGHT),
        (Element.WATER, Element.SHADOW),
        (Element.EARTH, Element.WATER),
        (Element.WIND, Element.EARTH),
        (Element.CHAOS, Element.WIND),
        (Element.LIGHT, Element.CHAOS)
    ]
)
def test_elemental_disadvantage(attacker, defender):
    assert ElementalSystem.get_multiplier(attacker, defender) == 0.80


def test_neutral_matchups_have_no_modifier():
    for attacker in Element:
        for defender in Element:
            if attacker != defender:
                if (
                    ElementalSystem.COUNTERS[attacker] != defender
                    and ElementalSystem.COUNTERS[defender] != attacker
                ):
                    assert ElementalSystem.get_multiplier(
                        attacker, defender
                    ) == 1.00


def test_elemental_advantage_increases_damage():
    damage = ElementalSystem.calculate_damage(
        450, Element.SHADOW, Element.WATER
    )

    assert damage == 563


def test_elemental_disadvantage_reduces_damage():
    damage = ElementalSystem.calculate_damage(
        450, Element.SHADOW, Element.LIGHT
    )

    assert damage == 360


def test_neutral_matchup_preserves_damage():
    damage = ElementalSystem.calculate_damage(
        450, Element.SHADOW, Element.EARTH
    )

    assert damage == 450


def test_negative_damage_is_rejected():
    with pytest.raises(ValueError):
        ElementalSystem.calculate_damage(
            -100, Element.SHADOW, Element.WATER
        )
