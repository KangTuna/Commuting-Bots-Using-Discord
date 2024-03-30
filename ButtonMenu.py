import discord
from discord.ext import commands

import pandas as pd

def read_my_dataframe(name,time):
    df = pd.read_csv(f'./undergraduate research student/{name}_working_table.csv',index_col=0)
    l = len(df)-1
    df.loc[l,'total_hour'] = df.loc[l,'total_hour'] + time
    df.loc[l,'end_hour'] = df.loc[l,'end_hour'] + time
    df.to_csv(f'./undergraduate research student/{name}_working_table.csv')

class ButtonFunction(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
        # self.add_item(discord.ui.Button(label='Click Here', url="http://aochfl.tistory.com"))
 
    @discord.ui.button(label='-2시간', style=discord.ButtonStyle.primary, row=1)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        name = interaction.user.nick
        read_my_dataframe(name,-2)
 
    @discord.ui.button(label='-1시간', style=discord.ButtonStyle.secondary, row=1)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        name = interaction.user.nick
        read_my_dataframe(name,-1)
 
    @discord.ui.button(label='+1시간', style=discord.ButtonStyle.success, row=1)
    async def button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        name = interaction.user.nick
        read_my_dataframe(name,1)
 
    @discord.ui.button(label='+2시간', style=discord.ButtonStyle.danger, row=1)
    async def button4(self, interaction: discord.Interaction, button: discord.ui.Button):
        name = interaction.user.nick
        read_my_dataframe(name,2)