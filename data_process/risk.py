#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   risk.py
@Time    :   2024/07/17 01:34:17
@Author  :   yichi zhang
@Contact :   17866548902@163.com
@Desc    :   处理事故风险数据
'''

import pandas as pd 
import os
import time
import numpy as np
import pickle

# 记录程序运行时间
start_time = time.time()

def is_holiday(date):
    # 固定日期的假期
    fixed_holidays = [
        (1, 1),    # New Year's Day
        (7, 4),    # Independence Day
        (12, 25),  # Christmas Day
    ]
    month, day = date.month, date.day

    if (month, day) in fixed_holidays:
        return True
    if month == 9 and date.weekday() == 0 and (day <= 7):
        return True
    if month == 5 and date.weekday() == 0 and (day > 24):
        return True
    if month == 1 and date.weekday() == 0 and (15 <= day <= 21):
        return True
    if month == 2 and date.weekday() == 0 and (15 <= day <= 21):
        return True
    if month == 11 and date.weekday() == 3 and (22 <= day <= 28):
        return True
    if month == 10 and date.weekday() == 0 and (8 <= day <= 14):
        return True
    return False

city='chicago'
file_path = "/media/sunziwei/D1T/yichi/sparse_data_process/data/%s/accident.csv"%(city)
risk = pd.read_csv(file_path)

# 设定城市的经纬度范围（这里以纽约为例）
if city=='chicago':
    lat_min, lat_max = 41.6445, 42.0236
    lon_min, lon_max = -87.9400, -87.5230
elif city=='nyc':
    lat_min, lat_max = 40.4774, 40.9176
    lon_min, lon_max = -74.2591, -73.7004
elif city=='dc':
    lat_min, lat_max = 38.7910, 38.9950
    lon_min, lon_max = -77.1190, -76.9090

## step1: 确定时间范围和需要的格式
if city == 'nyc':
    risk['CRASH DATE TIME'] = risk['CRASH DATE'] +' '+ risk['CRASH TIME']
    risk['datetime'] = pd.to_datetime(risk['CRASH DATE TIME'], format='%m/%d/%Y %H:%M')
    risk['date'] = risk['datetime'].dt.date
    # risk['month'] = risk['datetime'].dt.month
    # risk['weekday']=risk['datetime'].dt.day_of_week
    # risk['holiday'] = risk['datetime'].apply(is_holiday)
    risk['hour'] = risk['datetime'].dt.hour

    risk_data = risk[['date','datetime','hour','LATITUDE','LONGITUDE','NUMBER OF PERSONS INJURED','NUMBER OF PERSONS KILLED']]
    risk_data = risk_data.dropna() # 去掉缺失值
    risk_data1 = risk_data[(risk_data['LONGITUDE']>=lon_min)&(risk_data['LATITUDE']>=lat_min)&(risk_data['LONGITUDE']<=lon_max)&(risk_data['LATITUDE']<=lat_max)]
    # 修改列名
    risk_data1 = risk_data1.rename(columns={
        'LONGITUDE': 'lon',
        'LATITUDE': 'lat',
        'NUMBER OF PERSONS INJURED': 'injuries_total',
        'NUMBER OF PERSONS KILLED': 'killed_total'
    }) 

elif city == 'chicago':
    # risk_data1 = risk[['CRASH_DATE','CRASH_MONTH','CRASH_DAY_OF_WEEK','CRASH_HOUR','LATITUDE','LONGITUDE','INJURIES_TOTAL','INJURIES_FATAL']]
    risk_data1 = risk[['CRASH_DATE','CRASH_HOUR','LATITUDE','LONGITUDE','INJURIES_TOTAL','INJURIES_FATAL']]
    risk_data1 = risk_data1.rename(columns={
        'LONGITUDE': 'lon',
        'LATITUDE': 'lat',
        'INJURIES_TOTAL': 'injuries_total',
        'INJURIES_FATAL': 'killed_total',
        # 'CRASH_MONTH':'month',
        # 'CRASH_DAY_OF_WEEK':'weekday', # 这里星期几是从1-7
        'CRASH_HOUR':'hour',
    })  # 2016.1.1-2016.6.30

    risk_data1['datetime'] = pd.to_datetime(risk_data1['CRASH_DATE'], format="%m/%d/%Y %I:%M:%S %p")
    risk_data1['date'] = risk_data1['datetime'].dt.date
    # risk_data1['holiday'] = risk_data1['datetime'].apply(is_holiday)
    # risk_data1['weekday'] = risk_data1['weekday'] - 1

elif city == 'dc':
    # risk_data = risk[['FROMDATE','LATITUDE', 'LONGITUDE',
    #                    'FATAL_BICYCLIST','FATAL_DRIVER','FATAL_PEDESTRIAN','FATALPASSENGER','FATALOTHER',
    #                    'MAJORINJURIES_BICYCLIST','MAJORINJURIES_DRIVER','MAJORINJURIES_PEDESTRIAN','MAJORINJURIESPASSENGER','MAJORINJURIESOTHER',
    #                    'MINORINJURIES_BICYCLIST','MINORINJURIES_DRIVER','MINORINJURIES_PEDESTRIAN','MINORINJURIESPASSENGER','MINORINJURIESOTHER']]
    risk['datetime'] = pd.to_datetime(risk['FROMDATE'])
    risk['date'] = risk['datetime'].dt.date
    # risk['holiday'] = risk['datetime'].apply(is_holiday)
    # risk['weekday'] = risk['datetime'].dt.day_of_week
    # risk['month'] = risk['datetime'].dt.month
    risk['hour'] = risk['datetime'].dt.hour

    # 指定时间范围
    start_time = '2016-01-01 00:00:00'
    end_time = '2016-06-30 23:59:59'

    risk_data = risk[(risk['LONGITUDE']>=lon_min)&(risk['LATITUDE']>=lat_min)&(risk['LONGITUDE']<=lon_max)&(risk['LATITUDE']<=lat_max)
                          &(risk['datetime']>=start_time)&(risk['datetime']<=end_time)]
    risk_data = risk_data[['FROMDATE','datetime','date','hour','LATITUDE', 'LONGITUDE',
                       'FATAL_BICYCLIST','FATAL_DRIVER','FATAL_PEDESTRIAN','FATALPASSENGER','FATALOTHER',
                       'MAJORINJURIES_BICYCLIST','MAJORINJURIES_DRIVER','MAJORINJURIES_PEDESTRIAN','MAJORINJURIESPASSENGER','MAJORINJURIESOTHER',
                       'MINORINJURIES_BICYCLIST','MINORINJURIES_DRIVER','MINORINJURIES_PEDESTRIAN','MINORINJURIESPASSENGER','MINORINJURIESOTHER']]
    risk_data = risk_data.fillna(0)

    risk_data['injuries_total'] = risk_data['MAJORINJURIES_BICYCLIST']+risk_data['MAJORINJURIES_DRIVER']+risk_data['MAJORINJURIES_PEDESTRIAN']+risk_data['MAJORINJURIESPASSENGER']+risk_data['MAJORINJURIESOTHER']
    +risk_data['MINORINJURIES_BICYCLIST']+risk_data['MINORINJURIES_DRIVER']+risk_data['MINORINJURIES_PEDESTRIAN']+risk_data['MINORINJURIESPASSENGER']+risk_data['MINORINJURIESOTHER']
    
    risk_data['killed_total']=risk_data['FATAL_BICYCLIST']+risk_data['FATAL_DRIVER']+risk_data['FATAL_PEDESTRIAN']+risk_data['FATALPASSENGER']+risk_data['FATALOTHER']
    
    risk_data1 = risk_data[['datetime','date','hour','LATITUDE', 'LONGITUDE','injuries_total','killed_total']]
    risk_data1 = risk_data1.rename(columns={
        'LONGITUDE': 'lon',
        'LATITUDE': 'lat'
    })

##step2: 网格化

# 网格划分参数
grid_size = 20  # 分为 20x20 网格
lat_bins = np.linspace(lat_min, lat_max, grid_size + 1)
lon_bins = np.linspace(lon_min, lon_max, grid_size + 1)

# 为每条事故数据分配到网格
risk_data1["grid_x"] = pd.cut(risk_data1["lon"], bins=lon_bins, labels=False, include_lowest=True)
risk_data1["grid_y"] = pd.cut(risk_data1["lat"], bins=lat_bins, labels=False, include_lowest=True)


## step3: 合并
# 指定时间范围
start_time = '2016-01-01'
end_time = '2016-06-30'
#step1: 创建完整的时间范围（2016年1月1日到2016年6月30日，每小时一个记录）
date_range = pd.date_range(start=start_time, end=end_time, freq='H')
time_data = pd.DataFrame(date_range, columns=['datetime'])
time_data['hour']=time_data['datetime'].dt.hour
time_data['date']=time_data['datetime'].dt.date
# 各个网格
node_num = grid_size*grid_size
num_time_points = len(time_data)
total_records = num_time_points * node_num  # 总记录数 = 时间点数 * 每时间点网格数
time_data2 = time_data.loc[time_data.index.repeat(node_num)].reset_index(drop=True)
grid_x = np.tile(np.arange(0, grid_size ), grid_size)  # 每个时间点横坐标
grid_y = np.repeat(np.arange(0, grid_size ), grid_size)  # 每个时间点纵坐标
# 将网格坐标扩展到所有时间点
time_data2['grid_x'] = np.tile(grid_x, num_time_points) # (1720620,5)
time_data2['grid_y'] = np.tile(grid_y, num_time_points)

time_data2 = time_data2.drop(columns=['datetime'])
risk_data2 = risk_data1.drop(columns=['datetime'])
risk_data3 = pd.merge(time_data2,risk_data2,on=['date','hour','grid_x','grid_y'],how='left')
risk_data3['date'] = pd.to_datetime(risk_data3['date'], format='%Y-%m-%d')
risk_data3['month']=risk_data3['date'].dt.month
risk_data3['weekday']=risk_data3['date'].dt.day_of_week
risk_data3['holiday']=risk_data3['date'].apply(is_holiday)
risk_data3.fillna(0, inplace=True) # 其他用0补全
risk_data4 = risk_data3.groupby(['date', 'month','weekday','holiday','hour','grid_x','grid_y']).agg(
    {'injuries_total':'sum','killed_total':'sum'}).reset_index()
risk_data4['holiday']=risk_data4['holiday'].astype(int)
risk_data4['accident_risk'] = risk_data4['injuries_total']*1+risk_data4['killed_total']*3
# 修正数据
feature_columns = ['accident_risk','month', 'hour' ,'weekday', 'holiday']
feature_dim = len(feature_columns)
times = date_range.shape[0]  # 假设每一行是一个时间步
all_data = risk_data4[feature_columns].values
all_data = all_data.reshape(times, grid_size, grid_size, feature_dim) # (4345,20,20,5)

# 保存文件
save_path = "./sparse_data_process/new_data1229/%s/risk_0103.csv"%(city)
risk_data4.to_csv(save_path, index=False)
print(save_path,'保存完毕。')

save_path1 = "./new_data/%s/risk.pkl"%(city)
with open(save_path1, 'wb') as f:
    pickle.dump(all_data, f)
print(all_data.shape)
print(save_path1,'保存完毕～')