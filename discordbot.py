import asyncio
import discord
from discord.ext import commands
import os
import traceback
import urllib.parse
import re

prefix = os.getenv('DISCORD_BOT_PREFIX', default='🦑')
lang = os.getenv('DISCORD_BOT_LANG', default='ja')
token = os.environ['DISCORD_BOT_TOKEN']
client = commands.Bot(command_prefix=prefix)

#↓追加変数
# サーバ別に各値を保持
voice = {} # ボイスチャンネルID
channel = {} # テキストチャンネルID

@client.event
async def on_ready():
    presence = f'{prefix}ヘルプ | 0/{len(client.guilds)}サーバー'
    await client.change_presence(activity=discord.Game(name=presence))
 """
@client.command()
async def 接続(ctx):
    if ctx.message.guild:
        if ctx.author.voice is None:
            await ctx.send('ボイスチャンネルに接続してから呼び出してください。')
        else:
            if ctx.guild.voice_client:
                if ctx.author.voice.channel == ctx.guild.voice_client.channel:
                    await ctx.send('接続済みです。')
                else:
                    await ctx.voice_client.disconnect()
                    await asyncio.sleep(0.5)
                    await ctx.author.voice.channel.connect()
            else:
                await ctx.author.voice.channel.connect()
"""

@client.command()
async def 切断(ctx):
    if ctx.message.guild:
        if ctx.voice_client is None:
            await ctx.send('ボイスチャンネルに接続していません。')
        else:
            await ctx.voice_client.disconnect()

            
@client.event
async def on_message(message):
    if message.content.startswith(prefix):
        pass
 """
 ここから追加↓
 """
    elif targetTxtChannel:
        
 """
 ここまで追加↑
 """
    else:
        if message.guild.voice_client:
            text = message.content
            text = text.replace('\n', '、')
            pattern = r'^<@\d*>'
            if re.match(pattern, text):
                match = re.search(r'^<@(\d*)>', text)
                uid = match.group(1)
                user = await client.fetch_user(uid)
                username = user.name + '、'
                text = re.sub(pattern, username, text)
                pattern = r'https://tenor.com/view/[\w/:%#\$&\?\(\)~\.=\+\-]+'
                text = re.sub(pattern, '画像', text)
                pattern = r'https://[\w/:%#\$&\?\(\)~\.=\+\-]+(\.jpg|\.jpeg|\.gif|\.png|\.bmp)'
                text = re.sub(pattern, '、画像', text)
                pattern = r'https://[\w/:%#\$&\?\(\)~\.=\+\-]+'
                text = re.sub(pattern, '、URL', text)
                text = message.author.name + '、' + text
            if text[-1:] == 'w' or text[-1:] == 'W' or text[-1:] == 'ｗ' or text[-1:] == 'W':
                while text[-2:-1] == 'w' or text[-2:-1] == 'W' or text[-2:-1] == 'ｗ' or text[-2:-1] == 'W':
                    text = text[:-1]
                text = text[:-1] + '、ワラ'
            if message.attachments:
                text += '、添付ファイル'
            if len(text) < 100:
                s_quote = urllib.parse.quote(text)
                mp3url = f'http://translate.google.com/translate_tts?ie=UTF-8&q={s_quote}&tl={lang}&client=tw-ob'
                while message.guild.voice_client.is_playing():
                    await asyncio.sleep(0.5)
                message.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
            else:
                await message.channel.send('100文字以上は読み上げできません。')
        else:
            pass
    await client.process_commands(message)

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None:
        if member.id == client.user.id:
            presence = f'{prefix}ヘルプ | {len(client.voice_clients)}/{len(client.guilds)}サーバー'
            await client.change_presence(activity=discord.Game(name=presence))
        else:
            if member.guild.voice_client is None:
                await asyncio.sleep(0.5)
                await after.channel.connect()
            else:
                pass
 """
 ここからコメントアウト↓
                if member.guild.voice_client.channel is after.channel:
                    text = member.name + 'さんが入室しました'
                    s_quote = urllib.parse.quote(text)
                    mp3url = f'http://translate.google.com/translate_tts?ie=UTF-8&q={s_quote}&tl={lang}&client=tw-ob'
                    while member.guild.voice_client.is_playing():
                        await asyncio.sleep(0.5)
                    member.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
 ここまでコメントアウト↑
 """
    elif after.channel is None:
        if member.id == client.user.id:
            presence = f'{prefix}ヘルプ | {len(client.voice_clients)}/{len(client.guilds)}サーバー'
            await client.change_presence(activity=discord.Game(name=presence))
        else:
            if member.guild.voice_client.channel is before.channel:
                if len(member.guild.voice_client.channel.members) == 1:
                    await asyncio.sleep(0.5)
                    await member.guild.voice_client.disconnect()
                else:
"""
ここからコメントアウト↓
                    text = member.name + 'さんが退室しました'
                    s_quote = urllib.parse.quote(text)
                    mp3url = f'http://translate.google.com/translate_tts?ie=UTF-8&q={s_quote}&tl={lang}&client=tw-ob'
                    while member.guild.voice_client.is_playing():
                        await asyncio.sleep(0.5)
                    member.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
 ここまでコメントアウト↑
 """
    elif before.channel != after.channel:
        if member.guild.voice_client.channel is before.channel:
            if len(member.guild.voice_client.channel.members) == 1 or member.voice.self_mute:
                await asyncio.sleep(0.5)
                await member.guild.voice_client.disconnect()
                await asyncio.sleep(0.5)
                await after.channel.connect()

@client.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, 'original', error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@client.command()
async def 接続(ctx):
    global voice
    global channel
    
    guild_id = ctx.guild.id # サーバIDを取得
    vo_ch = ctx.author.voice # 召喚した人が参加しているボイスチャンネルを取得
    
   　# サーバを登録
    add_guild_db(ctx.guild)

    # サーバのプレフィックスを取得
    guild_deta = ctrl_db.get_guild(str(guild_id))
    if isinstance(guild_deta, type(None)):
        prefix = '$'
    else:
        prefix = guild_deta.prefix

    # 召喚された時、voiceに情報が残っている場合
    if guild_id in voice:
        await voice[guild_id].disconnect()
        del voice[guild_id] 
        del channel[guild_id]

    # 召喚した人がボイスチャンネルにいた場合
    if not isinstance(vo_ch, type(None)): 
        voice[guild_id] = await vo_ch.channel.connect()
        channel[guild_id] = ctx.channel.id
        noties = get_notify(ctx)
        await ctx.channel.send('モロッコ参上🌽"{}help"コマンドで使い方を表示します。'.format(prefix))
        for noty in noties:
            await ctx.channel.send(noty)
        if len(noties) != 0:
            await ctx.channel.send('なにかあれば、ちいちゃん🌽にいうてね')
    else :
        await ctx.channel.send('ボイスチャンネルに接続してから呼び出してください🌽')
        
    
@client.command()
async def ヘルプ(ctx):
    message = f'''◆◇◆{client.user.name}の使い方◆◇◆
　　{prefix}＋コマンドで命令できます。
　　{prefix}接続：ボイスチャンネルに接続します。
　　{prefix}切断：ボイスチャンネルから切断します。'''
   ctx.send(message)

client.run(token)
