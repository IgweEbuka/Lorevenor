# LOREVENOR

## MVP Combat & Consumable Design Record

**Checkpoint:** 9 November 2026\
**Status:** Living design document

This document records established design decisions for Lorevenor's MVP.
It is the reference for implementation and should prevent previously
agreed mechanics from being changed accidentally.

### Decision labels

-   **CONFIRMED** --- Explicitly agreed.
-   **UNRESOLVED** --- Requires another design decision or balancing.
-   **PROPOSED** --- Suggested but not yet approved.

------------------------------------------------------------------------

# 1. Core Combat Structure

## 1.1 Team and turn structure

-   MVP team size is capped at 3 characters.
-   The underlying engine should support variable team sizes.
-   The entire player team acts before the enemy team responds.
-   Initial turn priority is determined by a coin toss or equivalent
    first-player roll.
-   Certain encounters, such as bosses or mini-bosses, may force enemies
    to act first.
-   Character levels reset at the beginning of a fresh run.

## 1.2 Universal damage calculation pipeline

**CONFIRMED ORDER**

1.  Base Attack Damage
2.  Elemental Modifiers
3.  Defence
4.  Elemental Resistance
5.  Damage Reduction
6.  Shield
7.  HP

Elemental modifiers are applied immediately after base attack damage.

------------------------------------------------------------------------

# 2. Elemental Damage

## 2.1 Elemental modifiers

  Situation                   Modifier
  ------------------------- ----------
  Elemental advantage             +25%
  Elemental disadvantage          -20%
  Neutral matchup                   0%
  Elemental Vulnerability         +15%

Advantage, disadvantage and vulnerability combine additively.

Examples: - Advantage + Vulnerability = +40%. - Disadvantage +
Vulnerability = -5%.

## 2.2 Elemental Vulnerability

-   Vulnerability is not automatically applied by ordinary elemental
    attacks.
-   Only explicitly designated effects can apply it.
-   The applying effect's element must counter the target's natural
    element.
-   Vulnerability bonus is +15%.
-   Duration is 2 team turns.
-   Only one vulnerability can be active on an enemy at a time.
-   Reapplying the same vulnerability refreshes its duration without
    changing its strength.
-   Different vulnerability effects use effect-specific priority
    ratings.
-   Higher priority replaces lower priority and receives a fresh
    duration.
-   Lower priority cannot replace higher priority.
-   Equal-priority effects follow first-applied-wins.
-   Vulnerability applies to eligible damage from its corresponding
    element, including basic attacks, abilities, Ultimates and offensive
    consumables.

------------------------------------------------------------------------

# 3. Defence and Elemental Resistance

## 3.1 Defence

-   Defence is percentage-based.
-   It provides general mitigation against incoming damage.
-   Defence applies regardless of the attack's element.
-   Defence Up increases effective Defence.
-   Defence Down decreases effective Defence.

## 3.2 Elemental Resistance

-   Resistance is percentage-based.
-   Every character and enemy has base Resistance to all six elements.
-   Resistance only mitigates incoming damage of its corresponding
    element.
-   Resistance Up and Resistance Down modify the relevant Resistance.
-   Both single-element and all-element Resistance effects are
    supported.
-   Resistance buffs and debuffs should be rare in the MVP.
-   Resistance does not determine status-effect application chances in
    the MVP.

## 3.3 Natural elemental affinity

-   Characters receive an additional natural Resistance bonus against
    the element their own element counters.
-   Characters sharing an element have the same elemental-affinity
    foundation.
-   Individual characters may have additional Resistance variations
    based on identity, role or specialisation.
-   Enemies can have individually designed Resistance profiles.
-   Bosses generally have higher overall elemental Resistance but must
    retain meaningful weaknesses.

Known elemental counter relationships:

  Character's element   Additional Resistance
  --------------------- -----------------------
  Light                 Shadow
  Shadow                Water
  Water                 Earth
  Earth                 Wind
  Wind                  Chaos

**UNRESOLVED:** The complete six-element relationship table, including
the remaining Chaos relationship, must be verified before
implementation.

------------------------------------------------------------------------

# 4. Defence and Resistance Modifiers

## 4.1 Relative percentage modification

Buffs and debuffs modify existing values proportionally, not by adding
or subtracting percentage points.

Examples: - 25% Defence Down multiplies existing Defence by 0.75. - 30%
Defence Up multiplies existing Defence by 1.30. - 25% Resistance Down
multiplies existing Resistance by 0.75. - 30% Resistance Up multiplies
existing Resistance by 1.30.

## 4.2 Preserve natural attributes

-   Natural Defence and Resistance values must remain unchanged when
    temporary effects are applied.
-   Active modifiers are tracked independently.
-   Effective values are recalculated from natural values and active
    modifiers.
-   Expired or removed effects must not permanently alter natural
    attributes.

## 4.3 Modifier stacking

-   Multiple buffs and debuffs affecting the same attribute stack
    multiplicatively.

Example:

``` text
Natural Defence = 20%
Defence Up = 20%
Defence Up = 30%
Defence Down = 25%

Effective Defence = 20% × 1.20 × 1.30 × 0.75
                  = 23.4%
```

------------------------------------------------------------------------

# 5. Defensive Attribute Limits

-   Defence has its own maximum effective value.
-   Elemental Resistance has a separate maximum effective value.
-   Damage Reduction has a separate combined maximum of 75%.
-   Defence and Resistance caps are not yet assigned numerical values.
-   Caps are applied after calculating active modifiers.
-   Natural attributes remain unchanged when a cap is reached.
-   Combining defensive mechanics must not make characters practically
    invulnerable.

**UNRESOLVED:** Actual Defence and Resistance caps require balancing.

------------------------------------------------------------------------

# 6. Damage Reduction

Two types are supported:

1.  **General Damage Reduction** --- applies to all eligible incoming
    damage.
2.  **Elemental Damage Reduction** --- applies to incoming damage from a
    specified element.

Rules: - Applicable General and Elemental Damage Reduction combine
additively. - The combined Damage Reduction cannot exceed 75%. - Damage
Reduction cannot reduce damage below zero. - Damage Reduction is
independent of Defence and Elemental Resistance. - The 75% ceiling is a
theoretical maximum, not an ordinary target. - Ordinary abilities and
consumables must have modest values. - Reaching the cap should require
substantial investment, strong combinations or careful timing.

------------------------------------------------------------------------

# 7. Shields

**CONFIRMED MVP DESIGN**

-   Each character has one visible combined shield pool.
-   Additional shield grants increase the displayed total.
-   The engine internally tracks individual grants separately.
-   Each grant tracks remaining amount, source, expiration condition and
    remaining duration where applicable.
-   Incoming damage is absorbed by shields before HP.
-   Grants expiring soonest are consumed first.
-   If two grants expire at the same time, the earlier-applied grant is
    consumed first.
-   Temporary shields expire after their specified duration.
-   Persistent shields remain until depleted or the encounter ends.
-   All remaining shields disappear at encounter end.

The interface shows one combined shield value, not multiple shield bars.

------------------------------------------------------------------------

# 8. Defensive Effect Durations

Three duration categories are supported:

1.  Instant.
2.  Temporary.
3.  Encounter-long.

General design principles: - Instant effects should be relatively modest
and not excessively expensive. - Temporary effects last 1--2 team turns
and can be stronger. - Encounter-long effects provide greater strategic
utility but must not be overpowered.

**UNRESOLVED:** The precise meaning of Instant remains to be finalised.
It could mean protection against one eligible incoming attack or
protection lasting at least one team turn.

------------------------------------------------------------------------

# 9. Damage Precision and Rounding

**CONFIRMED**

-   Preserve decimal precision throughout all damage calculation stages.
-   Do not round intermediate results.
-   Round only the final damage output.
-   Use an explicit conventional rounding rule.
-   Do not rely on Python's default `round()` because it uses banker's
    rounding for halfway cases.
-   Damage must never become negative.

**UNRESOLVED:** The exact halfway-value convention must be specified
explicitly during implementation.

------------------------------------------------------------------------

# 10. Consumable System

## 10.1 Inventory

-   Shared team inventory.
-   Maximum capacity: 6 slots.
-   Limited stacking.
-   Consumables persist throughout a run.
-   No rarity system.
-   Only selected consumables can be sold to merchants.
-   No consumable upgrades in the MVP.
-   Effects have predefined strengths.

## 10.2 Usage restrictions

-   No AP cost to use consumables.
-   Maximum one consumable per team turn.
-   Pre-battle consumable use is allowed.
-   Maximum two consumables per encounter.
-   After Stage 14, a final-boss preparation window allows the same
    two-item limit.
-   Preparation effects carry into the final boss.
-   In-combat inventory rearrangement is restricted.

## 10.3 Acquisition

Sources include: - Combat rewards. - Merchants. - Special events. - Boss
rewards.

Acquisition follows a hybrid approach: - Most consumables are randomly
acquired. - Selected important encounters guarantee certain rewards. -
Ordinary encounters should not produce frequent consumable drops. -
Harder encounters have better chances. - Merchants have limited stock. -
Events occasionally provide unique items. - Boss rewards should be
meaningful without flooding inventory. - Powerful and unique items have
stricter per-run acquisition limits.

## 10.4 Targeting

Supported targeting: - Single target. - Team-wide. - Encounter-wide.

Consumables are primarily player-focused, with a small selection able to
affect enemies.

## 10.5 Healing and resources

-   Healing is percentage-based, not a fixed-plus-percentage hybrid.
-   Healing can restore HP to 100%.
-   Full-recovery items are rare and strictly limited.
-   Healing is usable both in and out of combat.
-   HP persists between encounters.
-   There is no automatic full recovery after battle.
-   Defeated characters cannot be healed or revived by consumables.
-   Ultimate charge restoration is supported.
-   Ordinary Ultimate restoration is partial; rare items may fill the
    meter.
-   Ultimate charge is capped at 100%.
-   AP restoration and cooldown-reset consumables are excluded from the
    initial MVP.

## 10.6 Cleansing

-   Specific status cleansing is supported.
-   Category-based cleansing is supported.
-   Broad cleansing is supported but should be rarer.
-   Cleansing does not grant immunity.
-   Temporary immunity consumables are excluded from the MVP.

## 10.7 Consumable effect stacking

-   Different effects can coexist.
-   Reapplying the same consumable effect refreshes its duration without
    increasing strength.
-   Explicitly designated stackable effects may follow separate rules.
-   Conflicting effects follow their own replacement or cancellation
    rules.
-   A central effect-stacking framework should eventually govern
    consumables, abilities, equipment, runes, passives and status
    effects.

------------------------------------------------------------------------

# 11. Offensive Consumables

-   Immediate damage, normally one hit.
-   No multi-turn damage by default.
-   Damage should be modest and balanced against abilities and
    Ultimates.
-   Single-target consumables generally deal more damage per target.
-   Multi-target consumables deal less damage per target and hit all
    eligible enemies.
-   Consumable attacks have guaranteed hits and no accuracy check.
-   Enemy evasion cannot cause these attacks to miss.
-   Attacks remain subject to Defence and elemental modifiers.
-   Offensive consumables can damage regional and final bosses under
    normal combat rules.
-   Damage is fixed and does not scale with character Attack or other
    attributes.
-   Enemy Defence and elemental modifiers still affect final damage.
-   Only selected offensive consumables apply status effects.
-   Damage and status application chance are balanced separately.
-   Only explicitly designated consumables trigger elemental reactions.
-   Consumables may interact with an existing status to trigger an
    additional effect only when specifically designed to do so.

## Boss status-effect resistance

-   Bosses have a reduced chance of receiving consumable-applied status
    effects.
-   If an effect succeeds, it receives its full normal duration.
-   Boss resistance percentage remains unresolved.
-   Whether this resistance also applies to ability-applied status
    effects remains unresolved.

------------------------------------------------------------------------

# 12. Implementation Principles

These engineering requirements are derived from the confirmed design:

1.  Keep natural attributes separate from active combat modifiers.
2.  Track active effects independently, including source and expiration.
3.  Use reusable effect-handling logic rather than separate
    implementations for every ability and consumable.
4.  Recalculate effective Defence and Resistance from their natural
    values and active modifiers.
5.  Apply the universal damage pipeline consistently to characters and
    enemies.
6.  Keep damage calculation separate from shield absorption and HP
    application where practical.
7.  Test stacking, expiration, caps, elemental interactions and damage
    rounding.
8.  Never silently change a confirmed game-design rule during
    implementation.
9.  If implementation reveals a design problem, document it and discuss
    the proposed change before altering the rule.

------------------------------------------------------------------------

# 13. Outstanding Decisions

  -----------------------------------------------------------------------
  Item                                Status
  ----------------------------------- -----------------------------------
  Defence maximum effective           UNRESOLVED
  percentage                          

  Elemental Resistance maximum        UNRESOLVED
  effective percentage                

  Exact natural Defence values        UNRESOLVED

  Exact base Elemental Resistance     UNRESOLVED
  values                              

  Elemental affinity bonus            UNRESOLVED
  percentages                         

  Complete six-element counter        UNRESOLVED
  relationship table                  

  Exact meaning of Instant defensive  UNRESOLVED
  effects                             

  Exact rounding behaviour for        UNRESOLVED
  halfway values                      

  Boss resistance to                  UNRESOLVED
  consumable-applied status effects   

  Whether boss status resistance      UNRESOLVED
  affects ability-applied effects     

  Complete mathematical interaction   TO BE VERIFIED IN IMPLEMENTATION
  of all damage modifiers             TESTS
  -----------------------------------------------------------------------

------------------------------------------------------------------------

**Document status:** Living MVP design record. Confirmed decisions
should only change through an explicit design discussion and revision of
this document.
