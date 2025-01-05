#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   poi_adj.py
@Time    :   2025/01/05 15:07:31
@Author  :   yichi zhang
@Contact :   17866548902@163.com
@Desc    :   计算每个网格之间的poi向量的相似度
'''

# here put the import lib
import pickle 
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.distance import cdist
from sklearn.metrics.pairwise import cosine_similarity

city = "chicago"
file_path = "/media/sunziwei/D1T/yichi/new_data/%s/poi.pkl"%(city)
with open(file_path,'rb') as f:
    poi_data = pickle.load(f)

grid_size = poi_data.shape[0] 
poi_features = poi_data.shape[2]
poi_feature_matrix = poi_data.reshape(grid_size * grid_size, poi_features)
similarity_matrix = cosine_similarity(poi_feature_matrix)
print(similarity_matrix.shape)

save_path1 = "./new_data/%s/poi_adj.pkl"%(city)
with open(save_path1, 'wb') as f:
    pickle.dump(similarity_matrix, f)
print(save_path1,'保存完毕～')
