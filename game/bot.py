import discord
from discord.ext import commands
import requests

TOKEN = 'MTI5MDk1MjIyMjgzNzgzMzc0OQ.GmmO1F.Dm8jBBxrw5dLeYRzn33RkU7Dijg_3qGx7eE0cg'
BASE_URL = 'http://localhost:5000/api/'

bot = commands.Bot(command_prefix='!')


@bot.event()
async def on_ready():
    print(f'Logged in as {discord.client.user}')


@bot.command()
async def on_message(message):
    if message.content.startswith('!join'):
        player_name = message.author.name
        response = requests.post(f'{BASE_URL}join', json={'player_name': player_name})
        await message.author.send(f'Welcome {player_name}! Use the control buttons below.')

        # Add reaction buttons for control
        join_message = await message.author.send("Control your cat with these buttons:")
        await join_message.add_reaction('⬅️')
        await join_message.add_reaction('➡️')
        await join_message.add_reaction('⬆️')
        await join_message.add_reaction('⬇️')


@bot.command()
async def on_reaction_add(reaction, user):
    if user != discord.client.user:
        direction = ''
        if reaction.emoji == '⬅️':
            direction = 'left'
        elif reaction.emoji == '➡️':
            direction = 'right'
        elif reaction.emoji == '⬆️':
            direction = 'up'
        elif reaction.emoji == '⬇️':
            direction = 'down'

        if direction:
            requests.post(f'{BASE_URL}move', json={'player_name': user.name, 'direction': direction})
            await user.send(f'Moved {direction}')


bot.run(TOKEN)
