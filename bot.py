import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv() 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents) 
# prefixo do bot

@bot.event
async def on_ready():
    print(f'{bot.user} estou online!')

@bot.command()
async def ping(ctx):
    await ctx.send('VAI SE FUDER!') 
# teste pra ver se tá funcionando

@bot.command()
async def ola(ctx):
    await ctx.send(f'Oi pia {ctx.author.mention}!')

if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print('Token do Discord não encontrado')
    else:
        bot.run(token)