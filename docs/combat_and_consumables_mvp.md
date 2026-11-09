# Lorevenor — Combat and Consumables MVP Design

**Document status:** Living design specification  
**Last updated:** 9 November 2026  
**Scope:** MVP combat, defensive attributes, elemental interactions, shields, status effects and consumables.

> This document records confirmed design decisions and explicitly labels unresolved rules. Numerical values marked as initial or provisional are intended to be validated through combat simulations and playtesting. They are not immutable balance targets.

---

## 1. Design principles

- Combat is turn-based. The entire player team acts before the enemy team responds.
- The engine should support variable team sizes, while the current MVP team cap is three.
- Fresh runs reset character levels.
- Defensive and offensive systems should be independently understandable and testable.
- Preserve agreed rules in this document before implementation. Do not silently convert proposals into confirmed rules.
- Use actual combat simulations and encounter tests to balance numerical values. Avoid excessive theoretical min-maxing before the engine exists.

## 2. Combat turn structure

### Confirmed
- The player team takes its actions as a team before enemies respond.
- The initial turn order is determined by a first-player roll/coin toss.
- Certain boss or mini-boss encounters may force the enemy team to act first.
- The combat engine should support variable team sizes, although the MVP team cap is three.

### To define later
- Exact action-point, cooldown and turn-transition rules not covered by this document.
- The detailed rules for forced enemy-first encounters.

---

## 3. Universal damage calculation pipeline

### Confirmed order

1. Base Attack Damage
2. Elemental Modifiers
3. Defence
4. Elemental Resistance
5. Damage Reduction
6. Shield
7. HP

Elemental modifiers are applied immediately after base attack damage.

### Damage calculation principles
- Each mitigation layer is applied sequentially to the remaining damage.
- Defence, Elemental Resistance and Damage Reduction are separate mechanics; their percentages are not simply added together.
- Damage cannot become negative.
- Preserve decimal precision throughout the calculation.
- Round only the final damage amount.
- Do not rely on Python's built-in `round()` because its halfway behavior uses banker's rounding.

### Rounding detail still unresolved
The exact halfway rule (for example, round-half-up) must be selected before implementation.

### Illustrative calculation only
For an attack with 1,000 damage, 25% Defence, 15% applicable Elemental Resistance and 25% Damage Reduction:

`1000 × (1 - 0.25) × (1 - 0.15) × (1 - 0.25) = 478.125`

The final damage would be 478 if the selected rounding rule rounds this value down.

This is an example to explain the pipeline, not a target that should be manually tuned into every encounter. Actual balance will be assessed through simulations and combat tests.

---

## 4. Elemental system

### 4.1 Counter relationships — confirmed

The six-element counter cycle is:

| Attacking element | Element it counters | Element that counters it |
|---|---|---|
| LIGHT | SHADOW | CHAOS |
| SHADOW | WATER | LIGHT |
| WATER | EARTH | SHADOW |
| EARTH | WIND | WATER |
| WIND | CHAOS | EARTH |
| CHAOS | LIGHT | WIND |

Each element has one counter and is countered by one element.

### 4.2 Elemental damage modifiers — confirmed

| Interaction | Modifier |
|---|---:|
| Advantage | +25% |
| Disadvantage | -20% |
| Neutral | 0% |
| Elemental Vulnerability | +15% |

- Advantage, disadvantage and vulnerability combine additively.
- Advantage plus vulnerability = +40%.
- Disadvantage plus vulnerability = -5%.
- Neutral matchups have no elemental modifier unless a separate effect applies.
- Vulnerability is not automatically applied by ordinary elemental attacks. Only designated effects can apply it.
- The element of the vulnerability effect must counter the target's natural element.
- Vulnerability applies to eligible damage from its corresponding element, including basic attacks, abilities, Ultimates and offensive consumables.
- Vulnerability lasts two team turns.
- Only one vulnerability can be active on an enemy at a time.
- Reapplying the same vulnerability refreshes its duration without increasing its strength.
- Different vulnerability effects follow effect-based priority:
  - A higher-priority effect replaces a lower-priority effect and receives a fresh two-team-turn duration.
  - A lower-priority effect cannot replace a higher-priority effect.
  - If priorities are equal, the first-applied effect remains.

---

## 5. Defensive attributes

Defence, Elemental Resistance and Damage Reduction are distinct layers in the damage pipeline.

### 5.1 Defence — confirmed

- Defence is percentage-based general mitigation against all eligible incoming damage.
- Defence Up increases effective Defence; Defence Down decreases effective Defence.
- Defence buffs and debuffs use relative percentage modification, not percentage-point changes.
  - Example: 25% Defence Down multiplies the current value by 0.75.
  - Example: 30% Defence Up multiplies the current value by 1.30.
- Natural Defence is preserved. Temporary modifiers are tracked separately.
- Multiple modifiers affecting the same attribute stack multiplicatively.
- Effective Defence is recalculated from the natural value and active modifiers.
- Effective Defence cannot exceed the confirmed 30% cap.

### 5.2 Elemental Resistance — confirmed

- Resistance is percentage-based mitigation against damage of its corresponding element only.
- Every character and enemy has a natural Resistance value against all six elements.
- A character receives an additional natural Resistance bonus against the element its own element counters.
- Characters sharing an element share the same archetype-based affinity foundation, while individual character-specific variations may be added based on identity, role or specialisation.
- Enemies may have individually designed Resistance profiles.
- Bosses generally have higher overall Resistance but must retain meaningful weaknesses.
- Single-element and all-element Resistance buffs/debuffs are supported, but expected to be rare in the MVP.
- Resistance buffs/debuffs use relative percentage modification, not percentage-point changes.
- Natural Resistance is preserved; temporary modifiers are tracked separately.
- Multiple modifiers affecting the same Resistance value stack multiplicatively.
- Effective Resistance is recalculated from the natural value and active modifiers.
- Effective Resistance cannot exceed the confirmed 30% cap.
- Resistance does not affect status-effect application chance in the MVP.

### 5.3 Effective defensive caps — confirmed

| Attribute | Maximum effective value |
|---|---:|
| Defence | 30% |
| Elemental Resistance | 30% |
| Combined Damage Reduction | 75% |

The Defence and Resistance caps apply after their modifiers are calculated. They do not overwrite natural attribute values.

The 75% Damage Reduction ceiling is a theoretical upper limit and should be difficult to reach. It is not an ordinary expected combat value.

### 5.4 Natural Defence by archetype — confirmed initial values

| Archetype | Natural Defence |
|---|---:|
| TANK | 20% |
| SUPPORT | 12% |
| RANGER | 10% |
| DPS | 8% |

These values establish archetype-based defensive foundations. Individual characters may have variations later, while retaining their archetype identity.

### 5.5 Natural Elemental Resistance by archetype — confirmed initial values

Every character begins with the following baseline Resistance against **each** of the six elements:

| Archetype | Baseline Resistance against each element |
|---|---:|
| TANK | 10% |
| SUPPORT | 7% |
| RANGER | 5% |
| DPS | 5% |

In addition, each character receives a **+5 percentage-point natural affinity bonus** against the element its own element counters.

Examples:
- LIGHT character: +5% SHADOW Resistance.
- SHADOW character: +5% WATER Resistance.
- WATER character: +5% EARTH Resistance.
- EARTH character: +5% WIND Resistance.
- WIND character: +5% CHAOS Resistance.
- CHAOS character: +5% LIGHT Resistance.

The affinity bonus is part of the character's natural Resistance foundation. The effective 30% Resistance cap still applies after temporary modifiers are calculated.

### 5.6 Defensive identity — confirmed direction

- TANK has the strongest natural defensive foundation.
- SUPPORT has moderate natural Defence and can specialise in team protection.
- RANGER has a lower-to-moderate defensive foundation.
- DPS has the lowest natural Defence foundation.
- Individual character identity, element and specialisation may create variations.

### 5.7 Balance philosophy — confirmed direction

A well-built tank should generally receive around **400–500 damage from an attack that would otherwise deal 1,000 damage**, while receiving noticeably less damage from elements it resists.

This is a qualitative balancing target, not a fixed formula requirement. Actual damage received will depend on the attack's element, the tank's Resistance, active effects and shields.

The exact caps and archetype values are initial balancing values. They will be evaluated using actual combat simulations and encounter tests rather than repeatedly adjusted through paper calculations.

---

## 6. Damage Reduction — confirmed

There are two types:

1. **General Damage Reduction:** applies to all eligible incoming damage.
2. **Elemental Damage Reduction:** applies to damage from a specified element.

Rules:
- Applicable general and elemental Damage Reduction values stack additively.
- The combined Damage Reduction has a maximum cap of 75%.
- The 75% cap is a theoretical ceiling and should be difficult to reach.
- Ordinary abilities and consumables should grant modest values.
- Damage Reduction is independent of Defence and Elemental Resistance.
- Damage cannot become negative.

---

## 7. Shields — confirmed MVP design

- Each character has one visible combined shield pool.
- New shield grants add to the displayed total.
- Internally, each shield grant is tracked independently, including:
  - Remaining amount.
  - Source.
  - Expiration condition.
  - Remaining duration, if temporary.
- Incoming damage is absorbed by shields before HP.
- Shield grants expiring soonest are consumed first.
- If two grants expire at the same time, the earlier-applied grant is consumed first.
- Temporary grants expire when their duration ends.
- Persistent grants remain until depleted or the encounter ends.
- All remaining shields disappear at encounter end.
- The UI displays one combined shield number rather than separate shield bars.

---

## 8. Defensive effect durations

Three broad categories have been agreed:

| Category | General direction |
|---|---|
| Instant | Modest effects; should last at least a turn or a short, clearly defined window |
| Temporary | Lasts one to two team turns; may be stronger |
| Encounter-long | Persists for the encounter; has higher strategic utility but must not be overpowered |

### Unresolved
- The precise trigger and expiration definition for Instant effects.
- Whether each effect's duration is counted in player team turns, enemy turns, or another explicit timing unit. Vulnerability is already specified as two team turns.
- Exact strengths and costs for effects in each duration category.

Do not assume that "Instant" means one hit or one trigger until its definition is agreed.

---

## 9. Status effects

The general status-effect framework and individual effects are not yet fully designed.

Known decisions:
- Elemental Vulnerability is defined in Section 4.2.
- Defence and Resistance buffs/debuffs follow the modifier rules in Section 5.
- Bosses have increased resistance to status effects applied by consumables, but are not immune.
- If a consumable-applied status effect successfully applies to a boss, it retains its normal duration.

### Unresolved
- The exact boss resistance percentage against consumable-applied status effects.
- Whether the same boss resistance applies to status effects applied by abilities.
- General status-effect stacking, refresh, replacement and immunity rules beyond the specific vulnerability rules.
- Individual status-effect definitions, durations, strengths and interactions.

---

## 10. Consumables

### 10.1 Inventory and use — confirmed

- Inventory is shared by the team.
- Capacity is six slots.
- Consumables have limited stacking.
- Activating a consumable costs no AP.
- During combat, the team may use at most one consumable per team turn.
- Pre-battle use is allowed, with a maximum of two consumables per encounter.
- The final boss has a preparation window after Stage 14; the same two-item limit applies, and effects carry into the final boss encounter.
- Consumables persist throughout a run.
- There is no rarity system.
- Only selected consumables can be sold.
- Consumables can be acquired through combat rewards, merchants, events and boss rewards.
- Ordinary encounters should not drop consumables too frequently. Harder encounters have better chances; merchants have limited stock; events may offer occasional unique items; boss rewards should be meaningful without flooding inventory.
- Acquisition is hybrid: most drops are random, while selected important encounters guarantee at least one.
- Per-run acquisition limits vary: ordinary items are flexible, powerful items are strictly limited, and special items have unique conditions.
- Consumables are not upgraded; each has a predefined effect.

### 10.2 Inventory management — confirmed

Outside combat, players can:
- Rearrange inventory.
- Combine identical items up to the stack limit.
- Split stacks.
- Discard items.
- Inspect item descriptions.

During combat, inventory rearrangement is restricted.

### 10.3 Targeting — confirmed

Consumable target scopes include:
- Single-target.
- Team-wide.
- Encounter-wide.

Consumables are primarily player-focused, although a small selection may affect enemies.

### 10.4 Healing and resource restoration — confirmed

- Healing is percentage-based, not a hybrid of fixed and percentage healing.
- Healing can restore a character to 100% HP, but full-recovery items are rare and strictly limited.
- Healing can be used in and out of combat.
- HP is tracked between encounters; there is no automatic full heal after battle.
- HP restoration is supported.
- Ultimate charge restoration is supported. Ordinary items restore a portion; rare items may fill the meter. Ultimate charge is capped at 100%.
- AP restoration is excluded from the initial MVP.
- Ability cooldown-reset consumables are excluded from the initial MVP.
- Cleansing can target a specific status, a category of statuses, or broadly remove statuses. Broad cleansing is rarer.
- Cleansing does not grant immunity.
- Temporary-immunity consumables are excluded from the MVP.
- Consumables cannot revive defeated characters.
- Healing cannot target defeated characters.

### 10.5 Offensive consumables — confirmed

- Offensive consumables deal instant damage, normally in one hit; multi-turn damage is not the default.
- Damage should be modest and balanced against abilities and Ultimates.
- Both single-target and multi-target consumables are supported.
- Single-target consumables generally deal more damage per target.
- Multi-target consumables deal less damage per target and hit all eligible enemies.
- Offensive consumables have guaranteed hits: no accuracy check, and enemy evasion cannot cause them to miss.
- Their damage is still subject to enemy Defence and applicable elemental modifiers, Resistance and Damage Reduction.
- They can damage regional and final bosses. There is no special boss-specific damage immunity or reduction; normal defensive rules apply.
- Consumable damage is fixed and does not scale with character Attack, Ability Power or attributes.
- Selected offensive consumables may apply status effects; not all do. Damage and status application chance are balanced separately.
- Bosses have increased resistance to consumable-applied status effects but are not immune.
- Only specially designated consumables trigger elemental reactions. Not all consumables do.
- A designated consumable may interact with an active status to trigger an additional effect only when explicitly designed to do so.
- Offensive consumables have fixed base damage, but applicable elemental modifiers still apply.

---

## 11. Boss defensive considerations

- Bosses generally have higher overall Elemental Resistance than ordinary enemies.
- Bosses must retain meaningful elemental weaknesses.
- Bosses are not immune to consumable-applied status effects.
- Bosses have increased resistance to consumable-applied status effects, but the exact value remains unresolved.
- Successful consumable-applied status effects retain their normal duration.
- Bosses use the normal damage pipeline unless a specific, explicitly designed mechanic states otherwise.
- No special boss damage immunity/reduction applies to offensive consumables by default.

---

## 12. Outstanding decisions

The following items remain unresolved and should be settled before the relevant implementation work:

| Topic | Outstanding decision |
|---|---|
| Damage rounding | Exact halfway rounding rule |
| Instant duration | Precise trigger and expiration definition |
| Status effects | General stacking, refresh, replacement and immunity framework |
| Status effects | Individual effect definitions, durations, strengths and interactions |
| Boss status resistance | Exact resistance against consumable-applied status effects |
| Ability-applied status effects | Whether boss status resistance also applies |
| Combat timing | Precise duration-counting rules for effects not already specified |

### Deferred to implementation and testing
These are not unresolved design questions; they are intentionally deferred balance work:
- Validate the 30% Defence and 30% Resistance caps.
- Validate archetype natural Defence and Resistance values.
- Validate the 75% theoretical Damage Reduction ceiling.
- Test the 400–500 damage tank survivability target against representative attacks.
- Tune enemy and boss defensive profiles using actual encounter simulations.

---

## 13. Implementation guidance

When implementation begins:

1. Keep natural attributes separate from temporary modifiers.
2. Recalculate effective attributes from natural values and active effects.
3. Apply the damage pipeline in the exact order in Section 3.
4. Keep shield grants independently tracked internally, even though the UI shows one combined pool.
5. Make combat calculations deterministic and unit-test each stage independently.
6. Add integration tests for complete damage resolution, including elemental interactions, Defence, Resistance, Damage Reduction, shields and HP.
7. Build repeatable combat simulations to evaluate archetypes, enemies and bosses.
8. Treat the numerical values in this document as initial balance values and adjust them only in response to test evidence.

**Do not implement unresolved rules by guessing.** Mark the relevant behavior as pending until the design decision is made.
