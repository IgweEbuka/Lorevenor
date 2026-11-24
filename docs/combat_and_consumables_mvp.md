# Lorevenor — Combat and Consumables MVP Design

**Document status:** Living design specification  
**Last updated:** 24 November 2026  
**Scope:** MVP combat, defensive attributes, elemental interactions, shields, status effects and consumables.

> This document consolidates confirmed design decisions through Step 85 and explicitly labels unresolved rules. Numerical values marked as initial or provisional are intended to be validated through combat simulations and playtesting. They are not immutable balance targets.

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

### 7.1 Shield resource model

- Each character has one visible, combined shield pool.
- The player sees one total shield value, not separate bars for individual grants.
- New shield grants add to the character's current shield total.
- The engine must internally distinguish temporary and persistent shield portions so that their expiration and absorption rules can be enforced.
- The MVP does not require source-level tracking of every shield grant. Keep the internal model as simple as possible while preserving the rules below.
- Shield amounts are granted as predefined numerical values. Healing modifiers do not affect shielding, and there are no shield-strength modifier status effects in the MVP.

### 7.2 Temporary and persistent shielding

**Temporary shielding**
- Has a defined duration.
- Its duration begins immediately when applied.
- It does not lose duration immediately just because it was applied during the recipient's turn.
- It remains active until the recipient's turn finishes; duration is then reduced according to the agreed turn timing.
- If its duration reaches zero, any remaining amount in that temporary portion expires and is removed. It does not carry over.
- A new grant adds to the current shield pool; it does not refresh or replace existing shielding by default.

**Persistent shielding**
- Has no turn-based expiration.
- Remains until depleted, explicitly removed, or the encounter ends.
- Persistent shielding is removed when the encounter ends.

**Mixed grants**
- A single ability may grant temporary and persistent shielding at the same time.
- Each portion retains its own amount and expiration condition.
- Both portions contribute to the same visible shield total.
- When one temporary portion expires, only its remaining amount is removed; persistent shielding and other unexpired portions remain.

### 7.3 Shield absorption priority

- Shields absorb eligible incoming damage before HP.
- Temporary shielding is consumed before persistent shielding.
- Among temporary portions, the portion expiring soonest is consumed first.
- If two temporary portions have the same expiration time, the earlier-applied portion is consumed first.
- Once temporary shielding is exhausted, damage consumes persistent shielding.
- Any damage remaining after all available shielding is depleted passes to HP.
- This priority applies to ordinary incoming damage, DoT damage and self-inflicted damage unless an ability explicitly bypasses shields.

### 7.4 Shield amount and eligibility

- Shielding can exceed a character's maximum HP; there is no universal HP-based shield cap.
- Characters can receive shielding at full HP. HP and shields are independent resources.
- Defeated characters cannot receive shielding.
- Single-target abilities cannot target defeated characters for shielding. Team or multi-target abilities skip defeated characters.
- Shielding cannot revive a defeated character.
- When a character is defeated, all remaining shielding is removed immediately.
- Enemies follow the same shield rules: they may grant shielding to themselves or allied enemies, but defeated enemies cannot receive it.

### 7.5 Shield removal

- Abilities may explicitly remove a specified amount of shielding or remove all shielding.
- Shield removal does not directly damage HP.
- If the requested removal exceeds the available shield, the shield total becomes zero.
- There is no universal shield-removal cap; each ability defines its own amount or full-removal behavior.
- Shield-removal abilities may target one enemy, multiple selected enemies, or an entire team.
- Shield removal can have additional status effects, but those effects must be explicitly defined by the ability. Shield removal does not automatically apply a status effect.
- A secondary effect is still attempted if the target has no shielding, unless the ability explicitly requires successful shield removal first.
- Enemies may remove shielding from themselves or allied enemies when an ability explicitly permits it.
- Player-character shield removal/transfer mechanics should not be assumed unless separately designed.

**Default partial-removal priority**
1. Temporary portion expiring soonest.
2. Other temporary portions in expiration order.
3. Persistent shielding.
4. For equal expiration times, earlier-applied temporary portions first.

A specifically designed ability may override the default priority only when its targeting and removal behavior can be represented by the MVP shield model.

### 7.6 Shield transfers

- Enemy abilities may transfer existing shielding between enemy combatants.
- The ability must specify the amount, source and recipient.
- A transfer cannot exceed the source's available shielding.
- Transferred shielding retains its original type and expiration condition.
- Defeated enemies cannot be a source or recipient.
- Player-character shield transfers are excluded from the MVP.

### 7.7 Excluded shield mechanics

The following are excluded from the MVP:
- Shield Boost and Shield Weakness status effects.
- Percentage-based shield increase or reduction modifiers.
- A separate Shield Protection status effect.
- Player-character shield transfers.
- Unnecessary source-level tracking or separate visible shield bars.

Shield values, costs and ability balance should be tuned through playtesting rather than adding extra shield mechanics to compensate for high values.

## 8. Defensive effect durations

Three broad duration categories have been agreed:

| Category | General direction |
|---|---|
| Instant | Modest effects; should last at least a turn or a short, clearly defined window |
| Temporary | Generally lasts one to two turns; may be stronger |
| Encounter-long | Persists for the encounter; has higher strategic utility but must not be overpowered |

### Confirmed
- These are broad duration categories for defensive effects.
- Instant effects should not be so powerful or costly that their short duration creates an imbalance.
- Temporary effects can generally be stronger than Instant effects.
- Encounter-long effects can be stronger in general use, but must remain balanced.

### Unresolved
- The exact trigger and expiration definition for Instant effects.
- Whether a particular effect counts duration in player-team turns, enemy turns, or another explicitly defined timing unit. Vulnerability and status-effect timing have their own specific rules elsewhere in this document.
- Exact strengths and costs for each effect.

Do not assume that "Instant" means one hit or one trigger until its definition is agreed.

## 9. Status effects — confirmed MVP framework

### 9.1 Unified status-effect system

- Buffs and debuffs use one unified status-effect system.
- A status effect is beneficial or harmful, and its polarity determines whether it is eligible for dispelling or cleansing.
- There is no universal cap on the number of different status effects that can be active simultaneously in the MVP.
- A fixed status-slot limit may be considered later if testing shows a need for readability or balance.
- Status effects do not automatically interact with one another. They may coexist even when their effects appear contradictory. Any interaction must be explicitly designed in an ability, consumable, enemy mechanic or elemental reaction.

### 9.2 Status-effect identity and reapplication

- Every status effect has a unique internal system ID.
- Two applications count as the same effect only when they share the same defined ID. Display names alone do not determine identity.
- The same effect is source-independent by default. Two different combatants applying the same effect do not create separate active instances merely because their sources differ.
- Source information may be recorded for logs or explicitly designed special interactions, but source does not change the effect's stacking identity by default.
- Reapplying the same effect refreshes its duration; it does not increase its strength or create multiple independent instances by default.

When the same effect is reapplied at a different strength:
- **Stronger application:** replaces the weaker application and uses the new application's duration.
- **Equal-strength application:** keeps the strength and refreshes the duration to the new application's duration.
- **Weaker application:** is rejected and does not refresh the existing duration.
- Strength from repeated applications never adds together.

Different effects remain separate even if they modify the same attribute. For example, two applications with the same Attack Down effect ID follow reapplication rules, while Attack Down and Weaken are distinct effects and can coexist unless a specific mechanic defines an interaction.

### 9.3 Status-effect categories

Every status effect has exactly one primary functional category:

1. **Damage over Time (DoT)**
2. **Control**
3. **Attribute Modifiers**
4. **Recovery Modifiers**
5. **Protection**

An effect cannot belong to multiple primary categories. Additional behavior does not change its category. Category-based immunity, cleansing and dispelling use this primary category assignment.

### 9.4 Application rules

- Application may be guaranteed or chance-based, depending on the ability, consumable or enemy effect.
- More disruptive or powerful effects may be assigned lower application chances.
- There is no separate Status Resistance stat in the MVP.
- Defence, Elemental Resistance and Damage Reduction do not affect status-effect application probability.
- Bosses and special enemies may have explicitly designed status-application resistance rules.
- Multi-target status applications roll independently for each eligible target.
- An attached status effect requires a successful hit before its application roll. If the attack misses or is evaded, the attached effect is not applied.
- If the attack hits but shielding absorbs all of its damage, the status-effect application can still be attempted.
- Defeated characters are not eligible to receive status effects. Team-wide applications skip defeated targets, and application rolls are made only for eligible living targets.

### 9.5 Immunity

- Full immunity to a status effect is allowed.
- Both permanent and temporary immunity are supported.
- Immunity may apply to one specific effect or to an entire named category.
- Category immunity also covers future effects added to that category, unless a specific, documented exception is designed.
- Immunity blocks new applications by default; it does not automatically remove an effect that is already active.
- A specific immunity mechanic may explicitly remove existing effects when activated. Such behavior must be stated by that mechanic.
- Immunity and cleansing are separate mechanics.

### 9.6 Turn timing and duration

Status-effect duration decreases at the end of the affected side's completed turn, not at the end of a global round.

- If an effect is applied during a side's own turn, it does not immediately lose duration at that turn's end.
- Player-applied effects on enemies tick down after the enemy side completes its turn.
- Enemy-applied effects on players tick down after the player side completes its turn.

The standard affected-side turn sequence is:

1. At the start of the affected side's turn, resolve applicable DoT effects.
2. Resolve eligible periodic recovery effects, after all DoTs.
3. The affected side takes its actions.
4. At the end of that side's turn, reduce the duration of its active status effects.
5. Remove effects whose duration has expired.

If a DoT defeats a character at the start of the turn, that character cannot act, and no later scheduled effects for that defeated character resolve.

### 9.7 Damage-over-time ordering and reapplication

- DoT effects trigger at the start of the affected side's turn.
- DoT damage follows the normal damage pipeline: Elemental Modifiers, Defence, Elemental Resistance, Damage Reduction, Shield and HP, as applicable.
- Multiple DoTs resolve in application order, earliest first.
- Each individual effect application receives a unique internal sequence number, including applications made at the same time. Lower sequence numbers resolve first.
- If an earlier DoT defeats the target, later DoTs do not trigger.
- When a character is defeated, all active DoTs, buffs and debuffs are removed immediately. No further status processing occurs for that character.
- A newly applied DoT triggers at the next eligible start-of-turn.
- Reapplying the same DoT before it triggers refreshes its duration but does not cause immediate extra damage or delay its next scheduled trigger.
- Reapplication preserves the DoT's original trigger position; it does not create a new instance or move it behind other effects.
- Effects remain active if their source is defeated by default. A future effect may explicitly define `remove_on_source_defeat`; the default behavior is not to remove it.

### 9.8 Periodic recovery ordering

- Periodic recovery effects resolve at the start of the affected side's turn, after all DoT effects.
- If a DoT defeats the target, periodic recovery does not trigger.
- Multiple periodic recovery effects resolve independently in application order.
- Reapplying the same periodic recovery effect preserves its original position in the resolution order.
- A periodic recovery effect with one turn remaining still triggers at the start of that turn. It remains active through the turn, then its duration decreases at the end and it expires.
- Healing cannot exceed maximum HP. Any excess healing is discarded, not stored.

### 9.9 Attribute modifiers and stacking

- Different status effects that modify the same attribute stack multiplicatively.
- Buffs and debuffs that modify the same attribute also stack multiplicatively.
- Example: Attack Down of 20% and Weaken of 15% produce `1000 × 0.80 × 0.85 = 680` effective Attack, a combined reduction of 32%.
- Example: Attack Up of 20% and Attack Down of 15% produce `1000 × 1.20 × 0.85 = 1020` effective Attack.
- Effective attributes cannot fall below zero.
- Natural/base attribute values remain unchanged; active modifiers are applied to calculate effective values.
- This rule applies to Attack, Defence, Resistance and other attributes governed by the modifier system.

### 9.10 Healing and recovery modifiers

- Healing modifiers affect all eligible healing sources, including direct ability healing, consumables, periodic recovery and future eligible healing sources, unless an effect explicitly excludes a source.
- Multiple healing modifiers affecting the same healing calculation stack multiplicatively, regardless of whether they increase or reduce healing.
- Example: a 25% healing increase and a 20% healing reduction applied to 200 healing produce `200 × 1.25 × 0.80 = 200`.
- Healing modifiers do not affect shielding. Shielding is calculated independently from predefined ability or consumable amounts.
- Healing modifiers have maximum limits. Exact maximum healing increase remains unresolved.
- The maximum healing reduction is capped at 50%.
- Healing-reduction modifiers stack multiplicatively before the cap is applied.
- Effective healing reduction cannot exceed 50%, and healing cannot become negative. Eligible healing therefore retains at least 50% of its original amount when the reduction cap is reached.

### 9.11 Cleansing and dispelling

Cleansing and dispelling are separate mechanics:

- **Cleansing** removes harmful effects (debuffs).
- **Dispelling** removes beneficial effects (buffs).
- A special ability may explicitly perform both.

Both mechanics support three scopes:
- **Specific:** remove one particular effect.
- **Category:** remove eligible effects in a specified category.
- **Broad:** remove all eligible effects of the relevant polarity from the target.

Broad cleansing and dispelling should be less common or more restricted than specific removal.

Removal is guaranteed when the target and effect meet the mechanic's conditions. There are no chance rolls or resistance-to-removal stat in the MVP.

When an effect is cleansed, dispelled or expires naturally:
- It terminates immediately.
- Its remaining duration is discarded.
- It causes no final damage or bonus by default.
- A specific ability may explicitly define a removal-triggered effect.

### 9.12 Defeat and status cleanup

- When a character is defeated, all active buffs, debuffs and DoTs are removed immediately.
- No further status processing occurs for that character.
- Defeated characters cannot receive status effects.
- Team-wide status applications skip defeated characters.
- Active effects remain if their source is defeated, unless the effect explicitly defines a different rule. The default is that source defeat does not remove the effect.

### 9.13 Shield-related status-effect exclusions

The MVP does not include:
- Shield Boost status effects.
- Shield Weakness status effects.
- Percentage-based shield increase or reduction status effects.
- A Shield Protection status effect.

Shield amounts and shield removal are handled by the shield rules in Section 7, not by shield-strength modifiers.

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

The following design questions remain unresolved and must be settled before implementing the relevant behavior:

| Topic | Outstanding decision |
|---|---|
| Damage rounding | Exact halfway rounding rule |
| Instant duration | Precise trigger and expiration definition |
| Healing modifiers | Maximum healing-increase cap |
| Boss status resistance | Exact resistance against consumable-applied status effects |
| Ability-applied status effects | Whether boss status resistance also applies to status effects applied by abilities |
| Individual status effects | Specific effect catalogue, strengths, durations and ability-specific interactions |
| Effect timing | Duration rules for any future effect whose timing is not already specified by the general framework |

### Deferred to implementation and testing

These are intentionally deferred balance or content tasks, not unresolved framework rules:
- Validate the 30% Defence and 30% Resistance caps.
- Validate archetype natural Defence and Resistance values.
- Validate the 75% theoretical Damage Reduction ceiling.
- Test the 400–500 damage tank survivability target against representative attacks.
- Tune enemy and boss defensive profiles using encounter simulations.
- Tune shield amounts and ability costs through playtesting.
- Balance individual status-effect strengths, chances and durations when the effect catalogue and abilities are designed.
- Validate the healing-reduction cap and select a healing-increase cap through testing.

## 13. Implementation guidance

When implementation begins:

1. Keep natural attributes separate from temporary modifiers.
2. Recalculate effective attributes from natural values and active effects.
3. Apply the damage pipeline in the exact order in Section 3.
4. Preserve decimal precision throughout damage calculations and round only the final damage amount, using the agreed rounding rule once it is selected.
5. Keep one visible shield total per combatant. Internally track only the shield portions and timing information required to distinguish temporary from persistent shielding, apply expiration, and enforce absorption/removal priority.
6. Apply status effects through one unified system for buffs and debuffs.
7. Use unique internal effect IDs to determine whether two applications are the same effect.
8. Preserve application order for DoTs and periodic recovery, including a unique sequence number for each application.
9. Resolve start-of-turn effects and end-of-turn duration reductions in the order defined in Section 9.
10. Ensure defeat immediately clears the defeated combatant's statuses and shield pool, and prevents further status processing.
11. Keep cleansing, dispelling, immunity and shield removal as distinct operations.
12. Make combat calculations deterministic and unit-test each stage independently.
13. Add integration tests for complete damage resolution, including elemental interactions, Defence, Resistance, Damage Reduction, shields and HP.
14. Add tests for status reapplication, duration timing, DoT ordering, recovery ordering, immunity, cleansing, dispelling and defeat cleanup.
15. Build repeatable combat simulations to evaluate archetypes, enemies, bosses, shields and status effects.
16. Treat numerical values in this document as initial balance values where stated, and adjust them only in response to test evidence.

**Do not implement unresolved rules by guessing.** Mark the relevant behavior as pending until the design decision is made.