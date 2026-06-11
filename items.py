"""
WotLK Epic Gem Item IDs and transmute recipe definitions.
Realm 15 = Icecrown (Warmane), 3.3.5 patch.
Faction: 0 = Horde, 1 = Alliance
"""

REALM = 15

# ─── RAW EPIC GEMS ───────────────────────────────────────────────────────────
EPIC_GEMS = {
    "Cardinal Ruby":  36919,   # RED
    "King's Amber":   36922,   # YELLOW
    "Majestic Zircon": 36925,  # BLUE
    "Dreadstone":     36928,   # PURPLE
    "Ametrine":       36931,   # ORANGE
    "Eye of Zul":     36934,   # GREEN
}

# ─── TRANSMUTE MATERIAL IDs ───────────────────────────────────────────────────
TRANSMUTE_MATS = {
    "Scarlet Ruby":    36918,
    "Eternal Fire":    36860,
    "Autumn's Glow":   36921,
    "Eternal Life":    35625,
    "Sky Sapphire":    36924,
    "Eternal Air":     35623,
    "Twilight Opal":   36927,
    "Eternal Shadow":  35627,
    "Monarch Topaz":   36930,
    "Forest Emerald":  36933,
}

# ─── TRANSMUTE RECIPES ────────────────────────────────────────────────────────
# Each value is a list of (item_name, quantity) tuples
TRANSMUTES = {
    "Cardinal Ruby":   [("Scarlet Ruby", 1),   ("Eternal Fire", 1)],
    "King's Amber":    [("Autumn's Glow", 1),  ("Eternal Life", 1)],
    "Majestic Zircon": [("Sky Sapphire", 1),   ("Eternal Air", 1)],
    "Dreadstone":      [("Twilight Opal", 1),  ("Eternal Shadow", 1)],
    "Ametrine":        [("Monarch Topaz", 1),  ("Eternal Shadow", 1)],
    "Eye of Zul":      [("Forest Emerald", 3)],
}

# ─── CUT GEMS (name → item_id, grouped by base gem) ──────────────────────────

CARDINAL_RUBY_CUTS = {
    "Bold Cardinal Ruby":      40111,   # +20 Str
    "Delicate Cardinal Ruby":  40112,   # +20 Agi
    "Runed Cardinal Ruby":     40113,   # +23 SP
    "Bright Cardinal Ruby":    40114,   # +40 AP
    "Subtle Cardinal Ruby":    40115,   # +20 Dodge
    "Flashing Cardinal Ruby":  40116,   # +20 Parry
    "Fractured Cardinal Ruby": 40117,   # +20 ArPen
    "Precise Cardinal Ruby":   40118,   # +20 Expertise
}

KINGS_AMBER_CUTS = {
    "Brilliant King's Amber":  40123,   # +20 Int
    "Smooth King's Amber":     40124,   # +20 Crit
    "Rigid King's Amber":      40125,   # +20 Hit
    "Thick King's Amber":      40126,   # +20 Defense
    "Mystic King's Amber":     40127,   # +20 Resilience
    "Quick King's Amber":      40128,   # +20 Haste
}

MAJESTIC_ZIRCON_CUTS = {
    "Solid Majestic Zircon":    40119,  # +30 Stam
    "Sparkling Majestic Zircon": 40120, # +20 Spirit
    "Lustrous Majestic Zircon": 40121,  # +10 Mp5
    "Stormy Majestic Zircon":   40122,  # +25 Spell Pen
}

DREADSTONE_CUTS = {
    "Sovereign Dreadstone":   40129,   # +10 Str +15 Stam
    "Shifting Dreadstone":    40130,   # +10 Agi +15 Stam
    "Tenuous Dreadstone":     40131,   # +10 Agi +5 Mp5
    "Glowing Dreadstone":     40132,   # +12 SP +15 Stam
    "Purified Dreadstone":    40133,   # +12 SP +10 Spirit
    "Royal Dreadstone":       40134,   # +12 SP +5 Mp5
    "Mysterious Dreadstone":  40135,   # +12 SP +13 Spell Pen
    "Balanced Dreadstone":    40136,   # +20 AP +15 Stam
    "Infused Dreadstone":     40137,   # +20 AP +5 Mp5
    "Regal Dreadstone":       40138,   # +10 Dodge +15 Stam
    "Defender's Dreadstone":  40139,   # +10 Parry +15 Stam
    "Puissant Dreadstone":    40140,   # +10 ArPen +15 Stam
    "Guardian's Dreadstone":  40141,   # +10 Expertise +15 Stam
}

AMETRINE_CUTS = {
    "Inscribed Ametrine":    40142,   # +10 Str +10 Crit
    "Etched Ametrine":       40143,   # +10 Str +10 Hit
    "Champion's Ametrine":   40144,   # +10 Str +10 Defense
    "Resplendent Ametrine":  40145,   # +10 Str +10 Resil
    "Fierce Ametrine":       40146,   # +10 Str +10 Haste
    "Deadly Ametrine":       40147,   # +10 Agi +10 Crit
    "Glinting Ametrine":     40148,   # +10 Agi +10 Hit
    "Lucent Ametrine":       40149,   # +10 Agi +10 Resil
    "Deft Ametrine":         40150,   # +10 Agi +10 Haste
    "Luminous Ametrine":     40151,   # +12 SP +10 Int
    "Potent Ametrine":       40152,   # +12 SP +10 Crit
    "Veiled Ametrine":       40153,   # +12 SP +10 Hit
    "Durable Ametrine":      40154,   # +12 SP +10 Resil
    "Reckless Ametrine":     40155,   # +12 SP +10 Haste
    "Wicked Ametrine":       40156,   # +20 AP +10 Crit
    "Pristine Ametrine":     40157,   # +20 AP +10 Hit
    "Empowered Ametrine":    40158,   # +20 AP +10 Resil
    "Stark Ametrine":        40159,   # +20 AP +10 Haste
    "Stalwart Ametrine":     40160,   # +10 Dodge +10 Defense
    "Glimmering Ametrine":   40161,   # +10 Parry +10 Defense
    "Accurate Ametrine":     40162,   # +10 Expertise +10 Hit
    "Resolute Ametrine":     40163,   # +10 Expertise +10 Defense
}

EYE_OF_ZUL_CUTS = {
    "Timeless Eye of Zul":   40164,   # +10 Int +15 Stam
    "Jagged Eye of Zul":     40165,   # +10 Crit +15 Stam
    "Vivid Eye of Zul":      40166,   # +10 Hit +15 Stam
    "Enduring Eye of Zul":   40167,   # +10 Defense +15 Stam
    "Steady Eye of Zul":     40168,   # +10 Resil +15 Stam
    "Forceful Eye of Zul":   40169,   # +10 Haste +15 Stam
    "Seer's Eye of Zul":     40170,   # +10 Int +10 Spirit
    "Misty Eye of Zul":      40171,   # +10 Crit +10 Spirit
    "Shining Eye of Zul":    40172,   # +10 Haste +10 Spirit
    "Turbid Eye of Zul":     40173,   # +10 Resil +10 Spirit
    "Intricate Eye of Zul":  40174,   # +10 Haste +10 Spirit (variant)
    "Dazzling Eye of Zul":   40175,   # +10 Int +5 Mp5
    "Sundered Eye of Zul":   40176,   # +10 Crit +5 Mp5
    "Lambent Eye of Zul":    40177,   # +10 Hit +5 Mp5
    "Opaque Eye of Zul":     40178,   # +10 Resil +5 Mp5
    "Energized Eye of Zul":  40179,   # +10 Haste +5 Mp5
    "Radiant Eye of Zul":    40180,   # +10 Crit +13 Spell Pen
    "Tense Eye of Zul":      40181,   # +10 Hit +13 Spell Pen
    "Shattered Eye of Zul":  40182,   # +10 Haste +13 Spell Pen
}

# ─── GROUPED STRUCTURE ────────────────────────────────────────────────────────
GEM_GROUPS = [
    {
        "color": "🔴 RED",
        "epic_gem": "Cardinal Ruby",
        "epic_gem_id": 36919,
        "transmute_mats": TRANSMUTES["Cardinal Ruby"],
        "cuts": CARDINAL_RUBY_CUTS,
    },
    {
        "color": "🟡 YELLOW",
        "epic_gem": "King's Amber",
        "epic_gem_id": 36922,
        "transmute_mats": TRANSMUTES["King's Amber"],
        "cuts": KINGS_AMBER_CUTS,
    },
    {
        "color": "🔵 BLUE",
        "epic_gem": "Majestic Zircon",
        "epic_gem_id": 36925,
        "transmute_mats": TRANSMUTES["Majestic Zircon"],
        "cuts": MAJESTIC_ZIRCON_CUTS,
    },
    {
        "color": "🟣 PURPLE",
        "epic_gem": "Dreadstone",
        "epic_gem_id": 36928,
        "transmute_mats": TRANSMUTES["Dreadstone"],
        "cuts": DREADSTONE_CUTS,
    },
    {
        "color": "🟠 ORANGE",
        "epic_gem": "Ametrine",
        "epic_gem_id": 36931,
        "transmute_mats": TRANSMUTES["Ametrine"],
        "cuts": AMETRINE_CUTS,
    },
    {
        "color": "🟢 GREEN",
        "epic_gem": "Eye of Zul",
        "epic_gem_id": 36934,
        "transmute_mats": TRANSMUTES["Eye of Zul"],
        "cuts": EYE_OF_ZUL_CUTS,
    },
]
