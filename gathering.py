import pandas as pd

import os

dir_list = os.listdir('./undergraduate research student/')
# print(dir_list)
dfs = list()

# for i in dir_list:
#     dfs.append(pd.read_csv(f'./undergraduate research student/{i}'))

for i in dir_list:
    df = pd.read_csv(f'./undergraduate research student/{i}')
    name = i[:3]
    week_hour = df['total_hour'].sum() + (df['total_min'].sum() // 60)
    week_min = df['total_min'].sum() % 60

    print(name,week_hour,week_min)