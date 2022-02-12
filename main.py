import asyncio
import datetime

import discord
import sqlite_utils

import config
import themes
import ranking

################################################################################
# Globals


################################################################################


class MyClient(discord.Client):

    async def on_ready(self):

        # Init database
        database = sqlite_utils.Database("members_xp.db")
        members_table = database["members"]
        for member in self.get_all_members():
            members_table.insert({
                "id": member.id,
                "name": member.name,
                "xp": 0,
            }, pk="id", ignore=True)

        print('Logged in as')
        print(self.user.name)
        print('------')

        # TabBot React to all themes
        la_carte_channel = self.get_channel(config.CHANNEL_LA_CARTE_ID)
        theme_msg: discord.PartialMessage = la_carte_channel.get_partial_message(
            config.MESSAGE_CHOOSE_THEMES_ID)

        for emoji in themes.DICT_THEMES_EMOJI:
            await theme_msg.add_reaction(emoji)

        self.loop.create_task(self.check_reward_experience())
        self.loop.create_task(self.check_entrance())
        ########################################################################

    async def check_entrance(self):
        while True:
            for member in self.get_all_members():

                if member.top_role.id in config.LIST_ROLE_MODERATOR_IDS:
                    continue

                if member.top_role.id not in config.LIST_ROLE_CLIENTS_IDS:
                    la_carte: discord.TextChannel = self.get_channel(
                        config.CHANNEL_LA_CARTE_ID)

                    msg = f"\n:robot: Biiiip bip bip biiip, Nouveau client detecter à l'entrée du Café :robot: \n" \
                          f"Il semblerait que tu n'ais pas réussi à ouvrir la porte d'entrée, elle est un peu vielle et se bloque constament.\n" \
                          f"Pour ce faire il te suffit d'aller dans le channel {la_carte.mention} de lire les régles et réagir au message en cliquant sur la réaction :white_check_mark: pour les accepter, " \
                          f"ainsi tu pourras rentrer à l'intérieur et découvrir les Informations, Expositions, Magazines et la Bibliothéque du Café"

                    await member.send(content=msg)

            await asyncio.sleep(60*60*6)

    async def check_reward_experience(self):

        while True:
            database = sqlite_utils.Database("members_xp.db")

            for member in self.get_all_members():

                if member.top_role.id in config.LIST_ROLE_MODERATOR_IDS:
                    continue

                if member.top_role.id in config.LIST_ROLE_THEMES_IDS:
                    continue

                if member.top_role.id == config.ROLE_EVERYONE_ID:
                    continue

                dict_ranking = ranking.DICT_RANKING
                current_rank = dict_ranking[member.top_role.id]["rank"]

                if current_rank >= len(dict_ranking):
                    continue

                # Calculate current XP
                database_dict = database["members"].get(member.id)
                database_xp = database_dict["xp"]

                number_days = (
                            datetime.datetime.now() - member.joined_at).days
                current_xp = database_xp + (
                            (number_days + 1) * config.XP_DAY)

                new_top_role_id = member.top_role.id

                for role_id in dict_ranking:
                    xp_needed = dict_ranking[role_id]["xp_needed"]
                    if current_xp >= xp_needed:
                        new_top_role_id = role_id
                    else:
                        continue

                last_role = member.guild.get_role(member.top_role.id)
                new_role = member.guild.get_role(new_top_role_id)

                if last_role == new_role:
                    continue

                await member.remove_roles(last_role)
                await member.add_roles(new_role)

                # Send Message into La Gazette for celebrating the new Role
                if member.guild.system_channel is not None:
                    to_send = f"Pour tous ces jours passer avec nous dans ce café et ton implications **{member.mention}**,\n" \
                              f"l'equipe à le plaisir de t'offrir un **{new_role}** ! Merci Beaucoup :coffee: "
                    await member.guild.system_channel.send(to_send)

            await asyncio.sleep(60*15)

    async def on_member_join(self, member: discord.Member):
        guild: discord.Guild = member.guild

        la_carte: discord.TextChannel = self.get_channel(
            config.CHANNEL_LA_CARTE_ID)

        msg = f"""Bienvenue {member.display_name} sur le serveur {guild.name}🙂 \n
Pense à bien lire les régles et réagir au message en cliquant sur la réaction :white_check_mark: pour les accepter, ainsi tu auras accès au catégories Informations, Expositions, Magazines et Bibliothéque. \n
Pense aussi à choisir les thêmes qui t'interesse :
🎨  =  2D
💻  =  3D
🎮   =  Jeux
📷   =  Photo
🎥   =  Vidéo
🎵   =  Musique
🛠️   =  DIY
✍️   =  Écriture
en réagissant au message dans le channel {la_carte.mention}, tu auras ainsi accès au espaces Studios pour approfondir les thêmes qui t'intéresse."""

        await member.send(content=msg)

        database = sqlite_utils.Database("members_xp.db")
        members_table = database["members"]
        members_table.insert({
            "id": member.id,
            "name": member.name,
            "xp": 0,
        }, pk="id", ignore=True)

    async def on_member_remove(self, member: discord.Member):
        # Uncheck reactions dans le channel La Carte
        pass

    async def on_message(self,
                         message: discord.Message):

        member = message.author

        # Add points for the member reaction
        points = ranking.get_points_for_message_in_channel(message.channel)

        if not points:
            return

        ranking.add_point_to(member, points)

    async def on_message_delete(self,
                                message: discord.Message):

        member = message.author

        # Add points for the member reaction
        points = ranking.get_points_for_message_in_channel(message.channel)

        if not points:
            return

        ranking.remove_point_to(member, points)

    async def on_raw_reaction_add(self,
                                  raw_reaction: discord.RawReactionActionEvent):

        msg_id = raw_reaction.message_id
        guild: discord.Guild = self.get_guild(raw_reaction.guild_id)
        member = raw_reaction.member

        # Add points for the member reaction
        ranking.add_point_to(member, config.XP_REACTION)

        # Set Role for Themes choosed
        if msg_id == config.MESSAGE_CHOOSE_THEMES_ID:

            partial_emoji = raw_reaction.emoji

            if partial_emoji not in themes.DICT_THEMES_EMOJI:
                la_carte_channel = self.get_channel(config.CHANNEL_LA_CARTE_ID)
                theme_msg = la_carte_channel.get_partial_message(config.MESSAGE_CHOOSE_THEMES_ID)
                await theme_msg.clear_reaction(partial_emoji)
                return

            role_id = themes.DICT_THEMES_EMOJI[partial_emoji]["role_id"]

            role: discord.Role = guild.get_role(role_id)

            await member.add_roles(role)

        # Set Role after check Rules
        elif msg_id == config.MESSAGE_REGLES_ID:

            partial_emoji = raw_reaction.emoji

            if partial_emoji != discord.PartialEmoji(name="✅"):
                la_carte_channel = self.get_channel(
                    config.CHANNEL_LA_CARTE_ID)
                rules_msg = la_carte_channel.get_partial_message(
                    config.MESSAGE_REGLES_ID)
                await rules_msg.clear_reaction(partial_emoji)
                return

            role_id = config.ROLE_CLIENT_DE_PASSAGE_ID

            role: discord.Role = guild.get_role(role_id)

            await member.add_roles(role)
            if guild.system_channel is not None:
                to_send = f" Un nouveau client **{member.mention}** vient d'entrer dans le café!  "
                await guild.system_channel.send(to_send)

    async def on_raw_reaction_remove(self,
                                  raw_reaction: discord.RawReactionActionEvent):

        msg_id = raw_reaction.message_id
        guild: discord.Guild = self.get_guild(raw_reaction.guild_id)
        member = guild.get_member(raw_reaction.user_id)

        # Remove points for the member reaction
        ranking.remove_point_to(member, config.XP_REACTION)

        if msg_id == config.MESSAGE_CHOOSE_THEMES_ID:

            partial_emoji = raw_reaction.emoji

            if partial_emoji not in themes.DICT_THEMES_EMOJI:
                return

            role_id = themes.DICT_THEMES_EMOJI[partial_emoji]["role_id"]

            role: discord.Role = guild.get_role(role_id)

            await member.remove_roles(role)


# Setup Intents needed for the client
intents = discord.Intents.default()
intents.members = True
intents.reactions = True

# Connect the bot to the server
client = MyClient(intents=intents)
client.run(config.TOKEN)
