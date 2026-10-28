from game import elements, archetypes, characters, zones, regions


origin_region_S = regions.Region(elements.Element.SHADOW)
origin_region_L = regions.Region(elements.Element.LIGHT)
origin_region_C = regions.Region(elements.Element.CHAOS)
origin_region_E = regions.Region(elements.Element.EARTH)
origin_region_W = regions.Region(elements.Element.WATER)
origin_region_WI = regions.Region(elements.Element.WIND)

# Selectable Characters#


Night = characters.Character('Night', 'Male', origin_region_S, elements.Element.SHADOW, archetypes.Archetype.DPS)
Terra = characters.Character('Terra', 'Female', origin_region_E, elements.Element.EARTH, archetypes.Archetype.TANK)
Quranos = characters.Character('Quranos', 'Male', origin_region_L, elements.Element.LIGHT, archetypes.Archetype.SUPPORT)
Kza = characters.Character('The KZA', 'Male', origin_region_S, elements.Element.EARTH, archetypes.Archetype.DPS)

for _ in range(5):
    print(zones.Zone.camp_randomizer(elements.Element.CHAOS, 2))