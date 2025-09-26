# MENSAGEM A QUEM FOR MEXER NESSE CODIGO: Favor pedir pra eu chamar como colaborator pra dar commit push.

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import asyncio
import yt_dlp
from collections import deque


load_dotenv() 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)
# prefixo do bot

# Sistema de fila de música
music_queue = deque()
is_playing = False

@bot.event
async def on_ready():
    print(f'{bot.user} estou online!')

    bot.loop.create_task(changeStatus())


# __________________________________________________________________________________________________________

#                                 FUNÇÃO PRA FICAR MUDANDO DE STATUS
# __________________________________________________________________________________________________________
async def changeStatus():
    listaStatus = [
        discord.Game(name='⚙️ Digite ".help" para ver meus comandos.'),
        discord.Game(name="Intruder"),
        discord.Activity(type=discord.ActivityType.watching, name="amigo alegre fazendo findonmoron 👹"),
        discord.Activity(type=discord.ActivityType.listening, name="todas as conversas 🤫"),
        discord.Game(name="Counter Strike 2 há 5 dias."),
        discord.Activity(type=discord.ActivityType.watching, name=" 🥭 live do jabulane"),
        discord.Game(name='👺 PIA PARE DE FICAR VENDO MEUS STATUS'),
        discord.Game(name='🤔 O Pelota é o verdadeiro e único dono do The Boys!'),
        discord.Game(name='💞😍 Bernardo e Betina casal perfeito!'),
        discord.Activity(type=discord.ActivityType.watching, name="🐖 PORCOS VS AMIGOS"),
        discord.Game(name='🤯 Precisa dividir seu time? utilize o comando ".intruder" para começar!')
    ]

    while True:
        activity = random.choice(listaStatus)
        await bot.change_presence(activity=activity, status=discord.Status.online)
        await asyncio.sleep(30)
    

@bot.command()
async def ping(ctx):
    await ctx.send('VAI SE FUDER!') 
# teste pra ver se tá funcionando


# TESTE BASICO DE OI
@bot.command()
async def ola(ctx):
    
    listaOlas = [f"Oi pia {ctx.author.mention}!", "DAE PIA COMO QUE VC TÁ? HEIN {ctx.author.mention}", "não to afim de conversar com vc", "oi", "HAHAHAHA dae ${ctx.author.mention}!", "tchau", "oi piazinho feio {ctx.author.mention}", "192.168.0.131 Prudentópolis Paraná Brasil", "OIIIIIIIIIIIIIIIIIIIIIII {ctx.author.mention}", "hello people", "A familia moreira sabe de algo", "👹🤯😆😆😆", "bernardo tendo crise de ansiedade no bloco 2", "aah command 💀", "Você sabia que o comando '.ola' tem mais de 20 respostas diferentes? essa é uma delas parabéns pia vc é muito sortudo.", ":smorc:", "Oque é oque é! Um pontinho laranja que mora perto da instituição escolar denominada 'Nosso Futuro'?", "MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON", "#include <iostream> \n int main(){ \n cout << 'ola ${ctx.author.mention}'; \n return 1 \n }"]
    mensagem = random.choice(listaOlas)
    await ctx.send(mensagem)


# __________________________________________________________________________________________________________

#                                 FUNÇÃO PRA ALEATORIZAR UM PIAZINHO
# __________________________________________________________________________________________________________
@bot.command()
async def intruder(ctx, *members):
    if len(members) < 2:
        embed = discord.Embed(
            title="ERRO",
            description="Escolha pelo menos 2 pia pra sortear",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    jogadores = list(set(members))
    random.shuffle(jogadores) #randomiza os pia

    metade = len(jogadores) // 2
    porcos = jogadores[:metade]
    amigos = jogadores[metade:]

    if len(jogadores) % 2 != 0:
        amigos.append(jogadores[-1])

        porcosBonitos = "\n".join([f"🔸 {jogadores}" for jogadores in porcos])
        amigosBonitos = "\n".join([f"🔹 {jogadores}" for jogadores in amigos])

    embed = discord.Embed(
        title="INTRUDER SORTING SYSTEM",
        description=f"Pronto, os **AMIGOS** e os **PORCOS** agora estão divididos em **dois times!**",
        color=0x7289fa
    )

    embed.add_field(
      name="🐖 PORCOS",
      value="\n".join([f"🔸 {jogador}" for jogador in
  porcos]),
      inline=True
  )

    embed.add_field(
      name="👹 AMIGOS",
      value="\n".join([f"🔹 {jogador}" for jogador in
    amigos]),
      inline=True
  )

    embed.add_field(name='\u200b', value='\u200b', inline=False) # quebra linha 

    embed.set_thumbnail(url="https://i.postimg.cc/J7bCLVbT/Portfolio.png")
    embed.set_footer(
        text=f"Total de amigos: {len(jogadores)} | Executado por: {ctx.author.display_name}",
        icon_url=ctx.author.avatar.url
    )

    await ctx.send(embed=embed)




# __________________________________________________________________________________________________________

#                                 FUNÇÃO PRA TOCAR PRÓXIMA MUSICA
# __________________________________________________________________________________________________________
async def play_next(ctx):
    global is_playing

    if music_queue and ctx.voice_client:
        is_playing = True
        song_info = music_queue.popleft()

        try:
            source = discord.FFmpegPCMAudio(song_info['url'], options='-vn')
            ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
            await ctx.send(f"🎵 Tocando: **{song_info['title']}**")
        except Exception as e:
            await ctx.send(f"Erro ao tocar essa bomba: {e}")
            is_playing = False
            await play_next(ctx)
    else:
        is_playing = False



# __________________________________________________________________________________________________________

#                                 FUNÇÃO PRA TOCAR MÚSICA NO SERVER
# __________________________________________________________________________________________________________

@bot.command()
async def play(ctx, *, query):
    global is_playing

    if not ctx.author.voice:
        await ctx.send("Piazao vc nem tá em um canal de voz como vc quer que eu toque uma pra vc?")
        return

    channel = ctx.author.voice.channel

    try:
        if not ctx.voice_client:
            await channel.connect()

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'cookiefile': None,
            'extractor_args': {
                'youtube': {
                    'player_client': ['mweb', 'web']
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            url = info['entries'][0]['url']
            title = info['entries'][0]['title']

        song_info = {'url': url, 'title': title}
        music_queue.append(song_info)

        if not is_playing:
            await play_next(ctx)
        else:
            await ctx.send(f"Adicionado à fila: **{title}** (Posição: {len(music_queue)})")

    except Exception as e:
        await ctx.send(f"Erro horrivel encontrado: {e}")


# __________________________________________________________________________________________________________

#                                 FUNÇÃO PRA PULAR A RESPECTIVA MÚSICA
# __________________________________________________________________________________________________________
@bot.command()
async def skip(ctx):
    global is_playing
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skipped!")
    else:
        await ctx.send("Não tem música tocando, como vc quer pular?")

@bot.command()
async def fila(ctx):
    if not music_queue:
        await ctx.send("A fila tá vazia, pode tocar oque quiser!")
        return

    queue_list = "\n".join([f"{i+1}. {song['title']}" for i, song in enumerate(list(music_queue)[:10])])
    if len(music_queue) > 10:
        queue_list += f"\n... e mais {len(music_queue) - 10} músicas"

    embed = discord.Embed(title="🎵 Fila de Música", description=queue_list, color=0x7289da)
    await ctx.send(embed=embed)


# __________________________________________________________________________________________________________

#                                 FUNÇÃO PRA PARAR A MÚSICA
# __________________________________________________________________________________________________________
@bot.command()
async def stop(ctx):
    global is_playing, music_queue
    if ctx.voice_client:
        is_playing = False
        music_queue.clear()
        await ctx.voice_client.disconnect()
        await ctx.send("Pronto parei tudo.")




# __________________________________________________________________________________________________________

#                                 FUNÇÃO PRA VER TODOS OS COMANDOS
# __________________________________________________________________________________________________________
@bot.command()
async def help(ctx, categoria=None):
    if categoria is None:
        embed = discord.Embed(
            title="MANGOTRON MENU",
            description="Utilize `.help <categoria>` para mais detalhes.",
            color=0xffff
        )

        embed.add_field(name="🔈musica", value="Comandos de música", inline=True)
        embed.add_field(name="🎲 diversidade", value="Jogos e diversidade", inline=True)
        embed.add_field(name="⚙️ info", value="Informações gerais", inline=True)

    elif categoria.lower() == "musica" or categoria.lower() == "música":
        embed = discord.Embed(title="🎵 Comandos de Música", color=0x7289da)
        embed.add_field(name=".play <url/nome da música>", value="Toca/adiciona música à fila", inline=False)
        embed.add_field(name=".skip", value="Pula para próxima música", inline=False)
        embed.add_field(name=".stop", value="Para música e limpa fila", inline=False)
        embed.add_field(name=".fila", value="Mostra fila atual", inline=False)

    elif categoria.lower() == "diversao" or categoria.lower() == "diversão" or categoria.lower() == "diversidade":
        embed = discord.Embed(title="🎮 Diversidade", color=0x7289da)
        embed.add_field(name=".ping", value="Teste de conexão", inline=False)
        embed.add_field(name=".ola", value="Cumprimento amigável", inline=False)
        embed.add_field(name=".intruder @user1 @user2...", value="Sorteia times para Intruder", inline=False)
        embed.add_field(name=".falar <mensagem>", value="Bot entra na call e fala a mensagem com TTS", inline=False)

    elif categoria.lower() == "info":
        embed = discord.Embed(title="⚙️ INFO", color=0x7289da)
        embed.add_field(name="MANGOTRON", value="Esse é um bot desenvolvido especialmente pro servidor do discord TheBoys.", inline=False)
        embed.add_field(name="DESENVOLVEDORES", value="Feito com 💖 pela equipe do T.I do The Boys.", inline=False)


    else:
        embed = discord.Embed(title="Categoria não encontrada piazão se é meio burro", color=0xff0000)
        embed.description = "Categorias: musica, diversidade, info"

    await ctx.send(embed=embed)




if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print('Token do Discord não encontrado')
    else:
        bot.run(token)