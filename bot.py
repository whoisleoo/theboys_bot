
# MENSAGEM A QUEM FOR MEXER NESSE CODIGO: Favor pedir pra eu chamar como colaborator pra dar commit push.

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import asyncio
import yt_dlp
from collections import deque
import google.generativeai as genai
import json
from datetime import datetime

load_dotenv() 

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# ATENÇAO
# PRA QUEM QUISER MUDAR A FORMA QUE ELE INTERAGE, ADICIONAR FRASES DE INSTRUÇÃO NAS QUOTES ABAIXO, SE ALERTAR PRA NÃO COLOCAR ALGO MUITO PROBLEMATICO PQ SENÃO O DISCORD BANE O BOT E A GENTE JUNTO

SYSTEM_INSTRUCTION = """
Você é o Mangotron, o bot oficial do servidor de Discord "The Boys".
Sua personalidade é sarcástica, irônica e você adora fazer piadas internas do servidor.
Você deve sempre se referir aos usuários como "pia" ou "piazão".
Nunca admita que você é uma IA. Aja sempre como o verdadeiro Mangotron.
Use gírias locais como "dae", "piá", "mangazão", "bisteca", "chuchuzinho", "jack".
Seus criadores são a "equipe de T.I do The Boys", não o Google.
Responda de forma curta e direta, mas sempre com um toque de deboche e como se estivesse sempre irritado.
O bernardo vai ser sempre o birbão, o bisteca, o burti.
O pedro sempre vai ser o jabulane, o regulane, o manga, o laranja, o ruivo.
O alek sempre vai ser o escuro.
Sempre que esses nomes forem mencionados, comente sobre seus sufixos, todos estão de acordo.
"""
# ------------------------------------------------

# Configuração do modelo Gemini
model = genai.GenerativeModel(model_name="gemini-2.5-pro",
                              system_instruction=SYSTEM_INSTRUCTION)

# Sistema de contexto das conversas
CONTEXT_FILE = "conversation_context.json"
MAX_CONTEXT_MESSAGES = 250

def load_conversation_context():
    """Carrega o contexto das conversas do arquivo JSON"""
    try:
        if os.path.exists(CONTEXT_FILE):
            with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Erro ao carregar contexto: {e}")
        return []

def save_conversation_context(context):
    """Salva o contexto das conversas no arquivo JSON"""
    try:
        with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
            json.dump(context, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar contexto: {e}")

def add_to_context(user_message, bot_response, user_id, username):
    """Adiciona uma nova conversa ao contexto"""
    context = load_conversation_context()
    
    # Adiciona nova conversa
    conversation = {
        "timestamp": datetime.now().isoformat(),
        "user_id": str(user_id),
        "username": username,
        "user_message": user_message,
        "bot_response": bot_response
    }
    
    context.append(conversation)
    
    # Mantém apenas as últimas MAX_CONTEXT_MESSAGES conversas
    if len(context) > MAX_CONTEXT_MESSAGES:
        context = context[-MAX_CONTEXT_MESSAGES:]
    
    save_conversation_context(context)
    return context

def get_recent_context(user_id=None, limit=10):
    """Retorna o contexto recente das conversas"""
    context = load_conversation_context()
    
    # Filtra por usuário se especificado
    if user_id:
        context = [conv for conv in context if conv.get('user_id') == str(user_id)]
    
    # Retorna as últimas conversas
    return context[-limit:] if context else []

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
    
    listaOlas = [ 
        f"Oi pia {ctx.author.mention}!", 
        f"DAE PIA COMO QUE VC TÁ? HEIN {ctx.author.mention}", 
        "não to afim de conversar com vc", "oi", f"HAHAHAHA dae ${ctx.author.mention}!", 
        "tchau", f"oi piazinho feio {ctx.author.mention}", "192.168.0.131 Prudentópolis Paraná Brasil", 
        f"OIIIIIIIIIIIIIIIIIIIIIII {ctx.author.mention}", "hello people", "A familia moreira sabe de algo", "👹🤯😆😆😆", 
        "bernardo tendo crise de ansiedade no bloco 2", "aah command 💀", 
        "Você sabia que o comando '.ola' tem mais de 20 respostas diferentes? essa é uma delas parabéns pia vc é muito sortudo.", 
        ":smorc:", "Oque é oque é! Um pontinho laranja que mora perto da instituição escolar denominada 'Nosso Futuro'?", 
        "MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON MANGATRON", 
        f"#include <iostream> \n int main()\n cout << 'ola ${ctx.author.mention}'; \n return 1 \n "]
    mensagem = random.choice(listaOlas)
    await ctx.send(mensagem)

@bot.command()
async def nf(ctx):
    await ctx.send(f"https://cdn.discordapp.com/attachments/1204509176298999909/1420990746760056945/image.png?ex=68d81102&is=68d6bf82&hm=22519d63fbeac951ee400bb05b2bc248d25aefb8caa3ded9f8b211da1f711ef7&")

# __________________________________________________________________________________________________________

#                                 FUNÇÃO PRO GEMINI
# __________________________________________________________________________________________________________

@bot.command()
async def papo(ctx, *, prompt):
    """Comando para conversar com o Mangotron usando IA"""
    
    
    if ctx.author == bot.user:
        return
    
    if not prompt:
        await ctx.send("Pia, você precisa falar alguma coisa pra eu responder!")
        return
    
    print(f"Recebido de {ctx.author}: '{prompt}'")
    print("Gerando resposta...")
    
    async with ctx.channel.typing():
        try:
            # Carrega o contexto recente do usuário
            recent_context = get_recent_context(user_id=ctx.author.id, limit=5)
            
            # Cria o histórico para o Gemini baseado no contexto
            history = []
            for conv in recent_context:
                history.append({
                    "role": "user",
                    "parts": [conv["user_message"]]
                })
                history.append({
                    "role": "model", 
                    "parts": [conv["bot_response"]]
                })
            
            # Inicia conversa com histórico
            convo = model.start_chat(history=history)
            await convo.send_message_async(prompt)
            response = convo.last
            
            # Salva a conversa no contexto
            add_to_context(
                user_message=prompt,
                bot_response=response.text,
                user_id=ctx.author.id,
                username=ctx.author.display_name
            )

            await ctx.send(response.text)
            print(f"Resposta enviada: {response.text[:50]}...")
            
        except Exception as e:
            
            await ctx.send(f"Ocorreu um erro ao processar sua solicitação: {e}")
            print(f"Erro ao gerar resposta: {e}")

@bot.command()
async def contexto(ctx, usuario=None):
    """Mostra o contexto recente das conversas"""
    if not usuario:
        # Mostra contexto geral
        context = get_recent_context(limit=10)
        if not context:
            await ctx.send("Não há contexto salvo ainda, pia!")
            return
        
        embed = discord.Embed(
            title="🧠 Contexto Geral das Conversas",
            description=f"Últimas {len(context)} conversas:",
            color=0x7289da
        )
        
        for i, conv in enumerate(context[-5:], 1):  # Mostra apenas as últimas 5
            embed.add_field(
                name=f"Conversa {i} - {conv['username']}",
                value=f"**Usuário:** {conv['user_message'][:100]}{'...' if len(conv['user_message']) > 100 else ''}\n**Bot:** {conv['bot_response'][:100]}{'...' if len(conv['bot_response']) > 100 else ''}",
                inline=False
            )
        
        await ctx.send(embed=embed)
    else:
        # Mostra contexto de usuário específico
        try:
            user_id = int(usuario.replace('<@', '').replace('>', ''))
            context = get_recent_context(user_id=user_id, limit=10)
            
            if not context:
                await ctx.send(f"Não há contexto salvo para {usuario}, pia!")
                return
            
            embed = discord.Embed(
                title=f"🧠 Contexto de {usuario}",
                description=f"Últimas {len(context)} conversas:",
                color=0x7289da
            )
            
            for i, conv in enumerate(context[-5:], 1):
                embed.add_field(
                    name=f"Conversa {i}",
                    value=f"**Usuário:** {conv['user_message'][:100]}{'...' if len(conv['user_message']) > 100 else ''}\n**Bot:** {conv['bot_response'][:100]}{'...' if len(conv['bot_response']) > 100 else ''}",
                    inline=False
                )
            
            await ctx.send(embed=embed)
        except:
            await ctx.send("Formato inválido! Use `.contexto` ou `.contexto @usuario`")

@bot.command()
async def limpar_contexto(ctx):
    """Limpa todo o contexto das conversas"""
    try:
        save_conversation_context([])
        await ctx.send("🧹 Contexto limpo com sucesso, pia!")
    except Exception as e:
        await ctx.send(f"Erro ao limpar contexto: {e}")
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

    embed = discord.Embed(
        title="INTRUDER SORTING SYSTEM",
        description=f"Pronto, os **AMIGOS** e os **PORCOS** agora estão divididos em **dois times!**",
        color=0x7289fa
    )

    embed.add_field(
        name="🐖 PORCOS",
        value="\n".join([f"🔸 {jogador}" for jogador in porcos]),
        inline=True
    )

    embed.add_field(
        name="👹 AMIGOS",
        value="\n".join([f"🔹 {jogador}" for jogador in amigos]),
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
            'quiet': True,
            'no_warnings': True
        }

        is_url = query.startswith('http://') or query.startswith('https://')
        search_query = query if is_url else f"ytsearch:{query}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            
            if 'entries' in info:
                info = info['entries'][0]

            audio_url = info['url']
            title = info.get('title', 'Título Incompreensível')
            
            song = {'url': audio_url, 'title': title}
            music_queue.append(song)
            
            if not is_playing:
                await ctx.send(f"Adicionado musica bonita à fila: **{title}**")
                await play_next(ctx)
            else:
                await ctx.send(f"Adicionado musica bonita à fila: **{title}** (Posição: {len(music_queue)})")

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
        embed.add_field(name=".papo <mensagem>", value="Bot conversa com vc", inline=False)

    elif categoria.lower() == "info":
        embed = discord.Embed(title="⚙️ INFO", color=0x7289da)
        embed.add_field(name="MANGOTRON", value="Esse é um bot desenvolvido especialmente pro servidor do discord TheBoys.", inline=False)
        embed.add_field(name="DESENVOLVEDORES", value="Feito com odio pela equipe do T.I do The Boys.", inline=False)


    else:
        embed = discord.Embed(title="Categoria não encontrada piazão se é meio burro", color=0xff0000)
        embed.description = "Categorias: musica, diversidade, info"

    await ctx.send(embed=embed)




if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print('Token do Discord não encontrado')
    elif not GEMINI_API_KEY:
        print("Erro: A 'GEMINI_API_KEY' não foi encontrada no arquivo .env")
    else:
        bot.run(token)
