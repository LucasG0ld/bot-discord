import discord
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load the bot token from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    BOT_TOKEN = config['BOT_TOKEN']

# Replace these values with your actual IDs and names
WELCOME_CHANNEL_ID = 1146533136658878494
GUILD_ID = 1141807080290926612

role_mappings = {
    "🚿": "League of Legends",
    "🚖": "Rocket League",
    "💀": "Escape the backrooms",
    "🔫": "Valorant",
    "⭐": "Summoners War",
    "💂": "World of Tanks",
    "🌳": "Minecraft",
    "🥇": "Teamfight Tactics",
    "🚀": "War Thunder"
}

role_bases = {
    "LES NOUVEAUX": None,
    "LES HABITUÉS": None,
    "LES COPAINS": None
}

# Dictionary to store users who have reacted
users_with_reactions = {}

async def assign_new_member_role(member):
    has_base_role = False
    for role_name in role_bases:
        role = discord.utils.get(member.roles, name=role_name)
        if role:
            has_base_role = True
            break
    
    if not has_base_role:
        for emoji in role_mappings:
            if discord.utils.get(member.roles, name=role_mappings[emoji]):
                role = discord.utils.get(member.guild.roles, name="LES NOUVEAUX")
                if role:
                    await member.add_roles(role)

@bot.event
async def on_ready():
    print(f'{bot.user.name} est connecté, prêt à attribuer les rôles !')

@bot.event
async def on_member_join(member):
    print(f"New member joined: {member.name}")
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    message = await channel.send(f"Bienvenue, {member.mention}! Réagis avec les emojis en fonction des jeux auxquels tu joues :\n🚿 : League of Legends\n🚖 : Rocket League\n💀 : Escape the backrooms\n🔫 : Valorant\n⭐ : Summoners War\n💂 : World of Tanks\n🌳 : Minecraft\n🥇 : Teamfight Tactics\n🚀 : War Thunder")
    for emoji in role_mappings:
        await message.add_reaction(emoji)
    
    # Store the new member's ID for checking later
    users_with_reactions[message.id] = member.id

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == WELCOME_CHANNEL_ID:
        guild = bot.get_guild(GUILD_ID)
        reacted_emoji = str(payload.emoji)
        
        # Check if the reacted user is the same as the user to whom the message was sent
        if reacted_emoji in role_mappings:
            role_name = role_mappings[reacted_emoji]
            role = discord.utils.get(guild.roles, name=role_name)
            
            if role:
                # Check if the reaction was on a message for a new member
                if payload.message_id in users_with_reactions:
                    member = guild.get_member(payload.user_id)
                    if member.id == users_with_reactions[payload.message_id]:
                        await member.add_roles(role)
                        
                        # Assign the "LES NOUVEAUX" role as well
                        await assign_new_member_role(member)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id == WELCOME_CHANNEL_ID:
        guild = bot.get_guild(GUILD_ID)
        reacted_emoji = str(payload.emoji)
        
        # Check if the reacted user is the same as the user to whom the message was sent
        if reacted_emoji in role_mappings:
            role_name = role_mappings[reacted_emoji]
            role = discord.utils.get(guild.roles, name=role_name)
            
            if role:
                # Check if the reaction was on a message for a new member
                if payload.message_id in users_with_reactions:
                    member = guild.get_member(payload.user_id)
                    if member.id == users_with_reactions[payload.message_id]:
                        await member.remove_roles(role)

# Run the bot
bot.run(BOT_TOKEN)