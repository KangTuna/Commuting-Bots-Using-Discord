import discord
from discord.ext import commands
from discord import Interaction
from datetime import datetime
from Persondata import PersonData
from ButtonMenu import ButtonFunction

import pandas as pd

# 실제사용할땐 TestBot_TOKEN.txt -> RealBot_TOKEN.txt로 바꿔야됨
with open('./TOKEN/TestBot_TOKEN.txt','r') as f:
    TOKEN = f.readline()

client = commands.Bot(command_prefix="!", intents= discord.Intents.all())

chul = dict()

@client.event
async def on_ready():
    await client.tree.sync()
    await client.change_presence(activity = discord.activity.Game(name='Working'), # 플레이중인 게임 이름
                                 status = discord.Status.online) # 봇의 상태
    # print(f'{client.user.name} is loggen in.')

@client.tree.command(name="ping",description='it will show the ping!')
async def ping(interaction : Interaction):
    bot_latency = round(client.latency*1000)
    await interaction.response.send_message(f'Pong!...{bot_latency}ms')

@client.command()
async def 출근(ctx: commands.context.Context):
    now = datetime.now()
    name = ctx.author.display_name
    if name not in chul:
        chul[name] = PersonData(name)
        chul[name].start(now)
        await ctx.send(f'현재시간 : {now.hour}시 {now.minute}분 {name} 출근')
    else:
        await ctx.send(f'이미 출근했습니다. 출근시간 : {chul[name].start_hour}시 {chul[name].start_min}분')

@client.command()
async def 퇴근(ctx: commands.context.Context):
    now = datetime.now()
    name = ctx.author.display_name
    if name in chul:
        chul[name].end(now)
        total_hour,total_min = chul[name].get_total()
        del chul[name]
        await ctx.send(f'현재시간 : {now.hour}시 {now.minute}분 {name} 퇴근\n총 근무시간 : {total_hour}시 {total_min}분')
    else:
        await ctx.send('아직 출근하지 않았습니다.')

@client.command()
async def 수업시작(ctx: commands.context.Context):
    now = datetime.now()
    name = ctx.author.display_name
    if name in chul:
        if not chul[name].isClassing():
            chul[name].class_start(now)
            await ctx.send(f'{now.hour}시 {now.minute}분 수업시작')
        else:
            await ctx.send(f'이미 수업중입니다. 수업시작 시간 : {chul[name].start_class_hour}시 {chul[name].start_class_min}')    
    else:
        await ctx.send('아직 출근하지 않았습니다.')

@client.command()
async def 수업끝(ctx: commands.context.Context):
    now = datetime.now()
    name = ctx.author.display_name
    if name in chul:
        if chul[name].isClassing():
            chul[name].class_end(now)
            await ctx.send(f'{now.hour}시 {now.minute}분 수업끝')
        else:
            await ctx.send('아직 수업시작 하지 않았습니다.')
    else:
        await ctx.send('아직 출근하지 않았습니다.')

@client.command()
async def init(ctx: commands.context.Context):
    await ctx.send(ctx.author.name)

@client.command()
async def check(ctx: commands.context.Context, message):
    await ctx.send(f'{ctx.author.display_name} {message}')

@client.command()
async def 주간(ctx: commands.context.Context):
    now = datetime.now()
    name = ctx.author.display_name
    week = now.isocalendar()[1]
    try:
        df = pd.read_csv(f'./undergraduate research student/{name}_working_table.csv',index_col=0)
        df = df[df['week'] == week]
        week_hour = df['total_hour'].sum() + (df['total_min'].sum() // 60)
        week_min = df['total_min'].sum() % 60
        await ctx.send(f'이번주 총 근무 시간은 {week_hour}시 {week_min}분 입니다.')
    except:
        await ctx.send('이번주에 근무하신 기록이 없습니다.')

@client.command()
async def 월간(ctx: commands.context.Context):
    now = datetime.now()
    name = ctx.author.display_name
    month = now.month
    try:
        df = pd.read_csv(f'./undergraduate research student/{name}_working_table.csv',index_col=0)
        df = df[df['month'] == month]
        monthly_hour = df['total_hour'].sum() + (df['total_min'].sum() // 60)
        monthly_min = df['total_min'].sum() % 60
        await ctx.send(f'이번달 총 근무 시간은 {monthly_hour}시 {monthly_min}분 입니다.')
    except:
        await ctx.send('이번달에 근무하신 기록이 없습니다.')

@client.command()
async def 수정(ctx: commands.context.Context, text: str):
    hour = int(text[:2])
    note = text[2:].lstrip()
    print(note)
    time = datetime.now()
    name = ctx.author.display_name
    df = pd.read_csv(f'./undergraduate research student/{name}_working_table.csv',index_col=0)
    data = {'year': [time.year], # int
            'month': [time.month], # int
            'day': [time.day], # int
            'week': [time.isocalendar()[1]], # int
            'start_hour': [0], # int
            'start_min': [0], # int
            'end_hour': [0], # int
            'end_min': [0], # int
            'total_hour': [hour], # int
            'total_min': [0],
            'note' : [note]} # int
    ddf = pd.DataFrame(data)
    df = pd.concat([df,ddf])
    df.to_csv(f'./undergraduate research student/{name}_working_table.csv')
    if hour >= 0:
        await ctx.send(f'근무시간 {hour}시간 추가 했습니다.')
    else:
        await ctx.send(f'근무시간 {-hour}시간 감소 했습니다.')
    
    # 사용한 데이터프레임 삭제
    del df
    del ddf
    

@client.command()
async def button1(ctx):
    await ctx.send(view=ButtonFunction())

client.run(TOKEN)
