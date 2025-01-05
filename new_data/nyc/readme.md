# risk.pkl

./new_data/%s/risk.pkl
shape = (4345,20,20,5)
'accident_risk','month', 'hour' ,'weekday', 'holiday'

# poi.pkl
./new_data/nyc/poi.pkl
实现路径：/media/sunziwei/D1T/yichi/sparse_data_process/poi.py
shape = (20,20,14)
poi顺序：
    'scenic_spots': 0,  # 景区
    'medical_health_services': 1,  # 医疗设施
    'domestic_services': 2,  # 家政服务
    'residential_areas': 3,  # 住宅区
    'financial_institutions': 4,  # 金融机构
    'sports_leisure_services': 5,  # 休闲运动
    'cultural_educational_services': 6,  # 文化教育
    'shopping': 7,  # 购物
    'housing_services': 8,  # 住房，酒店
    'governments_organizations': 9,  # 政府
    'corporations': 10,  # 公司企业
    'catering': 11,  # 餐饮
    'transportation': 12,  # 交通运输
    'public_services': 13  # 公共服务

# road_adj.pkl
提取道路的代表点：
质心（Centroid）：作为道路的代表点，用于确定其所属的网格。
起点和终点：可以将道路拆解为多个线段，并将每条线段映射到网格。

每个网格单元表示一个节点。
两个网格单元相邻（有共同边或角）时，视为连通。
如果两条道路有空间交集，也可认为它们的网格节点相连

./new_data/%s/road_adj.pkl
实现路径：/media/sunziwei/D1T/yichi/sparse_data_process/road_adj.py
shape=(400,400)

# poi_adj.pkl
/media/sunziwei/D1T/yichi/sparse_data_process/poi_adj.py
(400,400)

# risk_adj.pkl
./new_data/chicago/risk_adj.pkl
实现路径：/media/sunziwei/D1T/yichi/sparse_data_process/risk_adj.py
(400,400)