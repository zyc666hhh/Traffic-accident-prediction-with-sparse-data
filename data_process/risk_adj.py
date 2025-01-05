#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   risk_adj.py
@Time    :   2025/01/05 15:21:35
@Author  :   yichi zhang
@Contact :   17866548902@163.com
@Desc    :   每个网格中每个时刻的风险值 
'''

# here put the import lib
import pickle
from sklearn.metrics.pairwise import cosine_similarity

city = "dc"
file_path = "/media/sunziwei/D1T/yichi/new_data/%s/risk.pkl"%(city)
with open(file_path,'rb') as f:
    data = pickle.load(f)

time_dim,grid_size,_,_ = data.shape
risk_data = data[:,:,:,0].transpose(1,2,0).reshape(grid_size*grid_size,time_dim) #(20,20,4345)

similarity_matrix = cosine_similarity(risk_data)
print(similarity_matrix.shape)

save_path1 = "./new_data/%s/risk_adj.pkl"%(city)
with open(save_path1, 'wb') as f:
    pickle.dump(similarity_matrix, f)
print(save_path1,'保存完毕～')

