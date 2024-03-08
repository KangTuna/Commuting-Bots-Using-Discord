import pandas as pd

from datetime import datetime
import random as ran

# n = 100
# year = [2024 for i in range(n)]
# month = [(i//12)+1 for i in range(n)]
# day = [(i//30)+1 for i in range(n)]
# week= [(i//7)+1 for i in range(n)]
# start_hour = [ran.randint(0,3) for _ in range(n)]
# start_min = [ran.randint(0,60) for _ in range(n)]
# end_hour = [ran.randint(0,3) for _ in range(n)]
# end_min = [ran.randint(0,60) for _ in range(n)]
# total_hour = [ran.randint(0,3) for _ in range(n)]
# total_min = [ran.randint(0,60) for _ in range(n)]

# data = {'year': year,
#                 'month': month,
#                 'day': day,
#                 'week':week,
#                 'start_hour': start_hour,
#                 'start_min': start_min,
#                 'end_hour': end_hour,
#                 'end_min': end_min,
#                 'total_hour': total_hour,
#                 'total_min': total_min}

# df = pd.DataFrame(data,index = [i for i in range(n)])

# df.to_csv('test.csv')

# week = 3
# df = pd.read_csv(f'./undergraduate research student/강참치_working_table.csv',index_col=0)
# df = df[df['week'] == week]
# print(df)

t = datetime.now().isocalendar()[1]
print(t)