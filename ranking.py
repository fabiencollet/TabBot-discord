import sqlite_utils

import discord

import config

################################################################################
# Globals

DICT_RANKING = {
    config.ROLE_CLIENT_DE_PASSAGE_ID: {
        "rank": 1,
        "xp_needed": config.XP_RANK_CLIENT_DE_PASSAGE,
    },
    config.ROLE_ESPRESSO_ID: {
        "rank": 2,
        "xp_needed": config.XP_RANK_ESPRESSO,
    },
    config.ROLE_DOUBLE_ESPRESSO_ID: {
        "rank": 3,
        "xp_needed": config.XP_RANK_DOUBLE_ESPRESSO,
    },
    config.ROLE_AMERICANO_ID: {
        "rank": 4,
        "xp_needed": config.XP_RANK_AMERICANO,
    },
    config.ROLE_CAPPUCCINO_ID: {
        "rank": 5,
        "xp_needed": config.XP_RANK_CAPPUCCINO,
    },
    config.ROLE_MACHIATTO_ID: {
        "rank": 6,
        "xp_needed": config.XP_RANK_MACHIATTO,
    },
    config.ROLE_MACHIATTO_LATTE_ID: {
        "rank": 7,
        "xp_needed": config.XP_RANK_MACHIATTO_LATTE,
    },
    config.ROLE_IRISH_COFFEE_ID: {
        "rank": 8,
        "xp_needed": config.XP_RANK_IRISH_COFFEE,
    },
}


################################################################################
# Functions

def get_points_for_message_in_channel(channel: discord.TextChannel):

    if channel.type != discord.ChannelType.text:
        return

    category_id = channel.category_id

    if category_id == config.CAT_EXPOSITIONS_ID:
        return config.XP_EXPOSITIONS_MESSAGE
    elif category_id == config.CAT_MAGAZINES_ID:
        return config.XP_MAGAZINE_MESSAGE
    elif category_id == config.CAT_BIBLIOTHEQUE_ID:
        return config.XP_BIBLIOTHEQUE_MESSAGE
    elif category_id in config.LIST_CAT_STUDIOS_IDS:
        return config.XP_STUDIO_MESSAGE
    else:
        return 0


def add_point_to(member: discord.Member,
                 points: int):
    name = member.name

    # Get database xp
    database = sqlite_utils.Database("members_xp.db")
    current_dict = database["members"].get(member.id)
    current_xp = current_dict["xp"]

    # Update database xp
    database["members"].update(member.id, {"xp": current_xp + points})


def remove_point_to(member: discord.Member,
                    points: int):

    name = member.name

    # Get database xp
    database = sqlite_utils.Database("members_xp.db")
    current_dict = database["members"].get(member.id)
    current_xp = current_dict["xp"]

    # Update database xp
    database["members"].update(member.id, {"xp": current_xp - points})
