BASE_INVENTORY_SLOTS_TO_CHECK = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

BASE_CRITERIAS = {
    "Helm": {
        "Matches Needed": 3,
        "Attributes Needed": {},
    },
    "Chest": {
        "Matches Needed": 3,
        "Attributes Needed": {},
    },
    "Gloves": {
        "Matches Needed": 3,
        "Attributes Needed": {},
    },
    "Pants": {
        "Matches Needed": 3,
        "Attributes Needed": {},
    },
    "Boots": {
        "Matches Needed": 3,
        "Attributes Needed": {},
    },
    "Amulet": {
        "Matches Needed": 3,
        "Attributes Needed": {},
    },
    "Ring": {
        "Matches Needed": 3,
        "Attributes Needed": {},
    },
    "One-Handed Weapon": {
        "Matches Needed": 3,
        "Attributes Needed": {},
    },
    "Two-Handed Weapon": {
        "Matches Needed": 3,
        "Attributes Needed": {},
    },
    "Off Hand": {
        "Matches Needed": 3,
        "Attributes Needed": {},
    },
    "Shield": {
        "Matches Needed": 3,
        "Attributes Needed": {},
    },
}

CRITERIAS = {
    "Helm": {
        "Matches Needed": 3,
        "Attributes Needed": {
            "Basic Skill Attack Speed": 0,
            "Cooldown Reduction": 0,
            "Life On Kill": 0,
            "Maximum Life": 0,
            "Total Armor": 0,
            "Ranks of Cold Imbuement": 0,
            "Ranks of Shadow Imbuement": 0,
            "Ranks of Poison Imbuement": 0,
        },
    },
    "Chest": {
        "Matches Needed": 3,
        "Attributes Needed": {
            "Damage Reduction": 0,
            "Damage Reduction from Close Enemies": 0,
            "Damage Reduction from Distant Enemies": 0,
            "Life on Kill": 0,
            "Maximum Life": 0,
            "Total Armor": 0,
            "Damage Reduction from Enemies That Are Poisoned": 0,
        },
    },
    "Gloves": {
        "Matches Needed": 3,
        "Attributes Needed": {
            "Attack Speed": 0,
            "Critical Strike Chance": 0,
            "Lucky Hit Chance": 0,
            "Ranks of Barrage": 0,
            "Ranks of Flurry": 0,
            "Ranks of Penetrating Shot": 0,
            "Ranks of Rapid Fire": 0,
            "Ranks of Twisting Blades": 0,
        },
    },
    "Pants": {
        "Matches Needed": 3,
        "Attributes Needed": {
            "Damage Reduction": 0,
            "Damage Reduction while Injured": 0,
            "Damage Reduction from Close Enemies": 0,
            "Damage Reduction from Distant Enemies": 0,
            "Maximum Life": 0,
            "Total Armor": 0,
            "Damage Reduction from Enemies that are Poisoned": 0,
        },
    },
    "Boots": {
        "Matches Needed": 3,
        "Attributes Needed": {
            "Dexterity": 0,
            "Damage Reduction while Injured": 0,
            "Movement Speed": 0,
            "Energy Cost Reduction": 0,
        },
    },
    "Amulet": {
        "Matches Needed": 3,
        "Attributes Needed": {
            "Cooldown Reduction": 0,
            "Damage Reduction": 0,
            "Damage Reduction while Injured": 0,
            "Movement Speed": 0,
            "Total Armor": 0,
            "Damage Reduction from Enemies That Are Poisoned": 0,
            "Energy Cost Reduction": 0,
            "Rank of All Imbuement Skills": 0,
            "Ranks of the Exploit Passive": 0,
            "Ranks of the Frigid Finesse Passive": 0,
            "Ranks of the Malice Passive": 0,
            "Ranks of the Weapon Mastery Passive": 0,
        },
    },
    "Ring": {
        "Matches Needed": 3,
        "Attributes Needed": {
            "Critical Strike Chance": 0,
            "Critical Strike Damage": 0,
            "Lucky Hit Chance": 0,
            "Maximum Life": 0,
            "Vulnerable Damage": 0,
            "Critical Strike Damage with Imbued Skills": 0,
        },
    },
    "One-Handed Weapon": {
        "Matches Needed": 3,
        "Attributes Needed": {
            "Dexterity": 0,
            "All Stats": 0,
            # "Core Skill Damage": 0,
            "Critical Strike Damage": 16,
            "Critical Strike Damage with Imbued Skills": 0,
            "Vulnerable Damage": 0,
        },
    },
    "Shield": {
        "Matches Needed": 3,
        "Attributes Needed": {
        },
    }
}

ALL_GEAR_TYPES = [
    "Helm",
    "Chest",
    "Gloves",
    "Pants",
    "Boots",
    "Amulet",
    "Ring",
    "Axe",
    "Dagger",
    "Mace",
    "Sword",
    "Scythe",
    "Wand",
    "Staff",
    "Polearm",
    "Two-Handed Axe",
    "Two-Handed Mace",
    "Two-Handed Sword",
    "Two-Handed Scythe",
    "Bow",
    "Crossbow",
    "Totem",
    "Focus",
    "Shield",
]

WEAPONS_LIST = {
    "Axe": ["Damage to Healthy Enemies", "One-Handed Weapon"],
    "Dagger": ["Damage to Close Enemies", "One-Handed Weapon"],
    "Mace": ["Overpower Damage", "One-Handed Weapon"],
    "Sword": ["Critical Strike Damage", "One-Handed Weapon"],
    "Scythe": ["Life on Kill", "One-Handed Weapon"],
    "Wand": ["Lucky Hit Chance", "One-Handed Weapon"],
    "Staff": ["Damage to Crowd Controlled Enemies", "Two-Handed Weapon"],
    "Polearm": ["Damage to Injured Enemies",  "Two-Handed Weapon"],
    "Two-Handed Axe": ["Damage to Healthy Enemies", "Two-Handed Weapon"],
    "Two-Handed Mace": ["Overpower Damage", "Two-Handed Weapon"],
    "Two-Handed Sword": ["Critical Strike Damage", "Two-Handed Weapon"],
    "Two-Handed Scythe": ["Life on Kill", "Two-Handed Weapon"],
    "Bow": ["Damage to Distant Enemies", "Two-Handed Weapon"],
    "Crossbow": ["Vulnerable Damage", "Two-Handed Weapon"],
    "Totem": ["Cooldown Reduction", "Off Handed"],
    "Focus": ["Cooldown Reduction", "Off Handed"],
    "Shield": ["Block Chance", "Shield"],
}