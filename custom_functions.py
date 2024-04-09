import discord
from discord.ext import commands
import pandas as pd

from datetime import datetime

def role_check(ctx: commands.context.Context):
    roles_name = []
    for i in range(len(ctx.author.roles)):
        roles_name.append(ctx.author.roles[i].name)
    if '관리자' in roles_name:
        # TODO: 주간 월간 조정하는 함수 추가
        return True
    else:
        return False
    
def weekly(name: str, when = 0) -> tuple:
    now = datetime.now()
    week = now.isocalendar()[1] - when
    try:
        df = pd.read_csv(f'./undergraduate research student/{name}_working_table.csv',index_col=0)
        df = df[df['week'] == week]
        week_hour = df['total_hour'].sum() + (df['total_min'].sum() // 60)
        week_min = df['total_min'].sum() % 60
        return week_hour,week_min
    except:
        return 0,0
    
def monthly(name: str, when = 0) -> tuple:
    now = datetime.now()
    month = now.month - when
    try:
        df = pd.read_csv(f'./undergraduate research student/{name}_working_table.csv',index_col=0)
        df = df[df['month'] == month]
        monthly_hour = df['total_hour'].sum() + (df['total_min'].sum() // 60)
        monthly_min = df['total_min'].sum() % 60
        return monthly_hour,monthly_min
    except:
        return 0,0