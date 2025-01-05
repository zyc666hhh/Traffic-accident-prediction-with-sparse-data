#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   road_adj.py
@Time    :   2025/01/05 10:46:43
@Author  :   yichi zhang
@Contact :   17866548902@163.com
@Desc    :   绘制道路邻接图
'''

# here put the import lib
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely import wkt
import pickle
from scipy.spatial import cKDTree
from scipy.spatial.distance import cdist
from sklearn.metrics.pairwise import cosine_similarity


city = 'nyc'
file_path = "./sparse_data_process/data/%s/road_poi_orldata/shape/roads.shp"%(city) # FACILITY_T 1-13,FACI_DOM
poi_data = gpd.read_file(file_path)
"""
['osm_id', 'name', 'ref', 'type', 'oneway', 'bridge', 'maxspeed',
       'geometry', 'centroid', 'latitude', 'longitude']
"""

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

# step1: 数据预处理
# 提取质心作为道路的代表点
poi_data["centroid"] = poi_data["geometry"].centroid
poi_data["latitude"] = poi_data["centroid"].apply(lambda x: x.y)
poi_data["longitude"] = poi_data["centroid"].apply(lambda x: x.x)

# 过滤在研究区域范围内的道路
poi_data2 = poi_data[
    (poi_data["longitude"] >= lon_min) & (poi_data["latitude"] >= lat_min) &
    (poi_data["longitude"] <= lon_max) & (poi_data["latitude"] <= lat_max)
]

##step2: 网格化
grid_size = 20  # 分为 20x20 网格
lat_bins = np.linspace(lat_min, lat_max, grid_size + 1)
lon_bins = np.linspace(lon_min, lon_max, grid_size + 1)
# 为每条事故数据分配到网格
poi_data2["grid_x"] = pd.cut(poi_data2["longitude"], bins=lon_bins, labels=False, include_lowest=True)
poi_data2["grid_y"] = pd.cut(poi_data2["latitude"], bins=lat_bins, labels=False, include_lowest=True) # (289450, 13)

# step3: 构建邻接图
grid_features = poi_data2.groupby(["grid_x", "grid_y"]).agg({
    "type": lambda x: x.value_counts().idxmax(),  # 最常见的道路类型
    "oneway": "sum",                             # 单行道数量
    "bridge": "sum",                             # 桥梁数量
}).reset_index()

# 填充缺失值
all_grids = pd.DataFrame([(x, y) for x in range(grid_size) for y in range(grid_size)], columns=['grid_x', 'grid_y']) # 所有网格的空表
grid_features = pd.merge(all_grids,grid_features,on=['grid_x','grid_y'],how='left')
grid_features.fillna(0, inplace=True)

# 计算网格中心点的欧氏距离，转化为几何相似性
grid_features["center_lat"] = (lat_bins[grid_features["grid_y"]] + lat_bins[grid_features["grid_y"] + 1]) / 2
grid_features["center_lon"] = (lon_bins[grid_features["grid_x"]] + lon_bins[grid_features["grid_x"] + 1]) / 2  #(352,7)

# 获取网格中心点坐标
grid_coords = grid_features[["center_lat", "center_lon"]].values
# 计算欧氏距离
distances = cdist(grid_coords, grid_coords, metric="euclidean")
# 距离转换为相似性
epsilon = 1e-5
spatial_similarity = 1 / (distances + epsilon)  # 距离越近，相似度越高

# 属性相似性
feature_matrix = grid_features[["oneway", "bridge"]].values
attribute_similarity = cosine_similarity(feature_matrix) # (352,352)

# 综合相似性
alpha = 0.5  # 几何和属性相似性的权重
similarity_matrix = alpha * spatial_similarity + (1 - alpha) * attribute_similarity # similarity_matrix.shape=(352,352)


all_data = similarity_matrix.reshape(grid_size*grid_size, grid_size*grid_size)

save_path1 = "./new_data/%s/road_adj.pkl"%(city)
with open(save_path1, 'wb') as f:
    pickle.dump(all_data, f)
print(all_data.shape)
print(save_path1,'保存完毕～')
