import pandas as pd

from datetime import datetime
import os

class PersonData():
    def __init__(self,name):
        self.name = name
        data = {'start_time': [],
                'end_time': [],
                'total_time': []}
        self.timetable = pd.DataFrame(data)
        self.class_time = 0
        self.isclassing = False
        
    def start(self,time: datetime.now):
        self.start_hour = time.hour
        self.start_min = time.minute

    def end(self,time: datetime.now):
        self.end_hour = time.hour
        self.end_min = time.minute

        total = ((self.end_hour * 60) + self.end_min) - ((self.start_hour * 60) + self.start_min)
        total -= self.class_time
        self.total_hour = total // 60
        self.total_min = total % 60

        data = {'year': [time.year],
                'month': [time.month],
                'day': [time.day],
                'week': [time.isocalendar()[1]],
                'start_hour': [self.start_hour],
                'start_min': [self.start_min],
                'end_hour': [self.end_hour],
                'end_min': [self.end_min],
                'total_hour': [self.total_hour],
                'total_min': [self.total_min]}
        
        # timetable = pd.DataFrame(data,index = [time.date()])
        timetable = pd.DataFrame(data)

        # 파일 저장 경로 확인
        if not os.path.exists(f'./undergraduate research student'):
            os.makedirs(f'./undergraduate research student')

        # 파일 저장
        try:
            pre = pd.read_csv(f'./undergraduate research student/{self.name}_working_table.csv',index_col=0)
            table = pd.concat([pre,timetable])
            table.reset_index(drop=True,inplace=True)
            table = table.astype('int')
            table.to_csv(f'./undergraduate research student/{self.name}_working_table.csv')
        except:
            timetable.to_csv(f'./undergraduate research student/{self.name}_working_table.csv')

    def class_start(self,time: datetime.now):
        self.start_class_hour = time.hour
        self.start_class_min = time.minute
        self.isclassing = True

    def class_end(self,time: datetime.now):
        self.end_class_hour = time.hour
        self.end_class_min = time.minute

        self.class_time += ((self.end_class_hour * 60) + self.end_class_min) - ((self.start_class_hour * 60) + self.start_class_min)
        self.isclassing = False
    
    def isClassing(self):
        return self.isclassing
    
    def get_total(self):
        return self.total_hour,self.total_min
    
    def get_weekly(self,name: str, time: datetime.now):
        pass

    def get_monthly(self,name: str, time: datetime.now):
        pass

        
if __name__ == '__main__':
    a = PersonData('woo')
    a.start(datetime.now())
    a.end(datetime.now())
