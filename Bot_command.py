import discord
from discord.ext import commands
from discord import Interaction
from datetime import datetime

from Persondata import PersonData
from ButtonMenu import ButtonFunction
import custom_functions
import Gmail 

import pandas as pd
import asyncio

# 실제사용할땐 TestBot_TOKEN.txt -> RealBot_TOKEN.txt로 바꿔야됨
with open('./TOKEN/RealBot_TOKEN.txt','r') as f:
    TOKEN = f.readline()

client = commands.Bot(command_prefix="!", intents= discord.Intents.all())

chul = dict()

# 사용자가 퇴근을 안했을 때 경고를 보내기 위한 함수
async def my_task(bot: commands.Bot):
    while True:
        now = datetime.now()
        if now.hour >= 21 and chul:
            # 원하는 일을 합니다.
            for v in chul.values():
                if not v.get_night_shift():
                    await test_channel.send(f'{v.get_author().mention} 퇴근 확인하세요.')                    
        
        # Channel id : 출퇴근부 경고 위치
        test_channel = bot.get_channel(1224606472177057813) # 채널ID는 int형으로 입력합니다. 
        await asyncio.sleep(60)

# 봇이 켜지면 바로 발생하는 함수
@client.event
async def on_ready():
    await client.tree.sync()
    await client.change_presence(activity = discord.activity.Game(name='Working'), # 플레이중인 게임 이름
                                 status = discord.Status.online) # 봇의 상태
    # 매분 현재시간 체크해서 9시 이후 퇴근 안눌렀으면 경고 보내기
    client.loop.create_task(my_task(client))

######################## 테스트용 명령어 ######################################
@client.tree.command(name="ping",description='it will show the ping!')
async def ping(interaction : Interaction):
    bot_latency = round(client.latency*1000)
    await interaction.response.send_message(f'Pong!...{bot_latency}ms')

@client.command(name= 'init')
async def init(ctx: commands.context.Context):
    await ctx.send(ctx.author.name)

@client.command()
async def check(ctx: commands.context.Context):
    pass
    
##############################################################################
####################### 실제 사용하는 명령어 ###################################

# 근무를 시작할 때 사용
# 양식 : !출근
@client.command(name= '출근')
async def start_work(ctx: commands.context.Context):
    now = datetime.now()
    name = ctx.author.display_name
    if name not in chul:
        chul[name] = PersonData(ctx.author)
        chul[name].start(now)
        await ctx.send(f'현재시간 : {now.hour}시 {now.minute}분 {name} 출근')
    else:
        await ctx.send(f'이미 출근했습니다. 출근시간 : {chul[name].start_hour}시 {chul[name].start_min}분')

# 근무가 끝났고 총 근무시간을 저장하기 위해 사용
# 양식 : !퇴근
@client.command(name= '퇴근')
async def finish_work(ctx: commands.context.Context):
    now = datetime.now()
    name = ctx.author.display_name
    if name in chul:
        chul[name].end(now)
        total_hour,total_min = chul[name].get_total()
        del chul[name]
        await ctx.send(f'현재시간 : {now.hour}시 {now.minute}분 {name} 퇴근\n총 근무시간 : {total_hour}시 {total_min}분')
    else:
        await ctx.send('아직 출근하지 않았습니다.')

# 수업이 시작했을 때 사용
# 양식 : !수업시작
@client.command(name= '수업시작')
async def class_started(ctx: commands.context.Context):
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

# 수업이 끝났을 때 사용
# 양식 : !수업끝
@client.command(name= '수업끝')
async def class_finished(ctx: commands.context.Context):
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

# 본인의 주간 근무 시간을 확인하기 위해 사용
# 양식 : !주간
@client.command(name= '주간')
async def my_weekly(ctx: commands.context.Context):
    name = ctx.author.display_name
    week_hour,week_min = custom_functions.weekly(name)
    await ctx.send(f'이번주 총 근무 시간은 {week_hour}시 {week_min}분 입니다.')

# 본인의 월간 근무 시간을 확인하기 위해 사용
# 양식 : !월간
@client.command(name= '월간')
async def my_monthly(ctx: commands.context.Context):
    name = ctx.author.display_name
    monthly_hour, monthly_min = custom_functions.monthly(name)
    await ctx.send(f'이번달 총 근무 시간은 {monthly_hour}시 {monthly_min}분 입니다.')

# 사용자의 실수나 시스템상 오류로 발생한 에러를 해결하기 위해 사용하는 명령어
# 양식 : !수정 시간 사유 ## 사유 작성시 띄어쓰기 해도 됨
@client.command(name= '수정')
async def update(ctx: commands.context.Context, *, message: str):
    hour = message.split()[0]
    note = message[len(hour)+1:]
    hour = int(hour)
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
    df.reset_index(drop=True, inplace=True)
    df.to_csv(f'./undergraduate research student/{name}_working_table.csv',encoding='utf-8-sig')
    if hour >= 0:
        await ctx.send(f'근무시간 {hour}시간 추가 했습니다.')
    else:
        await ctx.send(f'근무시간 {-hour}시간 감소 했습니다.')
    
    # 사용한 데이터프레임 삭제
    del df
    del ddf

# 사용자가 퇴근 안했을 때 야근 여부를 확인 하기 위함
# 양식 : !야근
@client.command(name= '야근')
async def night_shift(ctx: commands.context.Context):
    name = ctx.author.display_name
    if name in chul:
        chul[name].night_shift_mode()
        await ctx.send('야근 모드로 전환했습니다.')
    else:
        await ctx.send('아직 출근하지 않았습니다.')

##############################################################################
######################## 관리자용 명령어 ######################################

# 유저의 시간을 확인하기 위해 사용
# 양식 : !확인 이름 주(월)간 주(월)차 ## 0(기본값) : 이번주(월) 1 : 전주(월) 2 : 전전주(월) ...
@client.command(name= '확인')
async def check_working_time(ctx: commands.context.Context,*,message: str) -> None:
    name = message.split()[0]
    MW = message.split()[1]
    try:
        when = int(message.split()[2]) # 주(월)간 위치 정해주면 가져오고
    except:
        when = 0 # 안정했으면 이번주(월)

    if custom_functions.role_check(ctx,'관리자'):
        if MW == '주간':
            week_hour,week_min = custom_functions.weekly(name,when)
            await ctx.send(f'{name}의 총 근무 시간은 {week_hour}시 {week_min}분 입니다.')
        elif MW == '월간':
            monthly_hour, monthly_min = custom_functions.monthly(name,when)
            await ctx.send(f'{name}의 총 근무 시간은 {monthly_hour}시 {monthly_min}분 입니다.')
    else:
        await ctx.send('권한이 없습니다.')

# 유저의 모든 데이터를 메일로 보내기
# 양식 : !메일 이메일
@client.command(name= '메일')
async def send_email(ctx: commands.context.Context,*, message: str) -> None:
    if custom_functions.role_check(ctx,'관리자'):
        Gmail.send_email(message)
        await ctx.send('메일 발송했습니다.')
    else:
        await ctx.send('권한이 없습니다.')

##############################################################################
############################### 안쓰는 명령어 #################################
@client.command()
async def button1(ctx):
    await ctx.send(view=ButtonFunction())

client.run(TOKEN)
