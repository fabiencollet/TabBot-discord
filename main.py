import os

import discord

import config
import themes

################################################################################
# Globals


################################################################################


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print('------')

    async def on_member_join(self, member: discord.Member):
        guild: discord.Guild = member.guild
        if guild.system_channel is not None:
            to_send = f"Welcome {member.mention} to {guild.name}!"
            basic_role = guild.get_role(config.ROLE_CLIENT_DE_PASSAGE_ID)

            await member.add_roles(basic_role)
            await guild.system_channel.send(to_send)

    async def on_message(self,
                         message: discord.Message):

        print(message.author)
        print(message.content)

    async def on_raw_reaction_add(self,
                                  raw_reaction: discord.RawReactionActionEvent):

        msg_id = raw_reaction.message_id
        guild: discord.Guild = self.get_guild(raw_reaction.guild_id)
        member = raw_reaction.member

        if msg_id != config.CHOOSE_THEMES_MESSAGE_ID:
            return

        partial_emoji = raw_reaction.emoji

        if partial_emoji not in themes.DICT_THEMES_EMOJI:
            la_carte_channel = self.get_channel(config.CHANNEL_LA_CARTE_ID)
            theme_msg = la_carte_channel.get_partial_message(config.CHOOSE_THEMES_MESSAGE_ID)
            await theme_msg.clear_reaction(partial_emoji)
            return

        theme_name = themes.DICT_THEMES_EMOJI[partial_emoji]["theme"]
        role_id = themes.DICT_THEMES_EMOJI[partial_emoji]["role_id"]

        role: discord.Role = guild.get_role(role_id)

        print(f" The Member {member.name} is interest to the theme {theme_name}, his new role is {role.name}")

        await member.add_roles(role)

    async def on_raw_reaction_remove(self,
                                  raw_reaction: discord.RawReactionActionEvent):

        msg_id = raw_reaction.message_id
        guild: discord.Guild = self.get_guild(raw_reaction.guild_id)
        member = guild.get_member(raw_reaction.user_id)

        if msg_id != config.CHOOSE_THEMES_MESSAGE_ID:
            return

        partial_emoji = raw_reaction.emoji

        if partial_emoji not in themes.DICT_THEMES_EMOJI:
            return

        theme_name = themes.DICT_THEMES_EMOJI[partial_emoji]["theme"]
        role_id = themes.DICT_THEMES_EMOJI[partial_emoji]["role_id"]

        role: discord.Role = guild.get_role(role_id)

        print(f" The Member {member.name} is not interest anymore to the theme {theme_name}, his  role {role.name} is remove")

        await member.remove_roles(role)

# Setup Intents needed for the client
intents = discord.Intents.default()
intents.members = True
intents.reactions = True

# Connect the bot to the server
client = MyClient(intents=intents)
client.run(config.TOKEN)
