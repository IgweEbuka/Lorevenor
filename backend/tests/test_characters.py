
from game.characters import Character
from game import elements, archetypes, regions


def create_test_character():
    return Character(
        "Test",
        "Male",
        regions.Region(elements.Element.SHADOW),
        elements.Element.SHADOW,
        archetypes.Archetype.DPS
    )


def test_character_starts_at_level_one():
    character = create_test_character()

    assert character.level == 1
    assert character.exp == 0
    assert character.max_health == 3000
    assert character.attack == 450


def test_character_levels_up():
    character = create_test_character()

    character.gain_experience(1000)

    assert character.level == 2
    assert character.max_health == 3250
    assert character.attack == 550


def test_character_cannot_exceed_level_five():
    character = create_test_character()

    character.gain_experience(10000)

    assert character.level == 5
    assert character.max_health == 4000
    assert character.attack == 850


def test_character_resets_for_new_run():
    character = create_test_character()

    character.gain_experience(10000)
    character.reset_for_new_run()

    assert character.level == 1
    assert character.exp == 0
    assert character.max_health == 3000
    assert character.attack == 450


def test_character_rejects_invalid_level():
    try:
        Character(
            "Test",
            "Male",
            regions.Region(elements.Element.SHADOW),
            elements.Element.SHADOW,
            archetypes.Archetype.DPS,
            level=6
        )
    except ValueError:
        assert True
    else:
        assert False, "Invalid level should raise ValueError."


def test_character_rejects_inconsistent_experience():
    try:
        create_test_character_with_invalid_experience()
    except ValueError:
        assert True
    else:
        assert False, "Inconsistent experience should raise ValueError."


def create_test_character_with_invalid_experience():
    return Character(
        "Test",
        "Male",
        regions.Region(elements.Element.SHADOW),
        elements.Element.SHADOW,
        archetypes.Archetype.DPS,
        level=2,
        exp=500
    )
