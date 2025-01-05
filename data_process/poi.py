#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   poi.py
@Time    :   2024/07/17 22:51:41
@Author  :   yichi zhang
@Contact :   17866548902@163.com
@Desc    :   处理poi数据
'''

# here put the import lib
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely import wkt
import pickle

city = 'chicago'
filenames = ['buildings','places','landuse','natural','points']
file_path = "./sparse_data_process/data/%s/road_poi_orldata/shape/points.shp"%(city) # FACILITY_T 1-13,FACI_DOM
poi_data = gpd.read_file(file_path)

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

category_mapping = {
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
}

facility_classification = {
    # scenic_spots
    'monument': 'scenic_spots',
    'theme_park': 'scenic_spots',
    'zoo': 'scenic_spots',
    'museum': 'scenic_spots',
    'viewpoint': 'scenic_spots',
    'attraction': 'scenic_spots',
    'artwork': 'scenic_spots',

    # medical_health_services
    'clinic': 'medical_health_services',
    'hospital': 'medical_health_services',
    'pharmacy': 'medical_health_services',
    'nursing_home': 'medical_health_services',
    'dentist': 'medical_health_services',
    'urgent_care': 'medical_health_services',

    # domestic_services
    'childcare': 'domestic_services',
    'nail_salon': 'domestic_services',
    'barbershop': 'domestic_services',
    'beauty': 'domestic_services',
    'dog_groomer': 'domestic_services',

    # residential_areas
    'apartment': 'residential_areas',
    'residential': 'residential_areas',
    'house': 'residential_areas',

    # financial_institutions
    'atm': 'financial_institutions',
    'bank': 'financial_institutions',
    'money_transfer': 'financial_institutions',
    'bureau_de_change': 'financial_institutions',

    # sports_leisure_services
    'gym': 'sports_leisure_services',
    'swimming_pool': 'sports_leisure_services',
    'sports_centre': 'sports_leisure_services',
    'dancing_school': 'sports_leisure_services',
    'spa': 'sports_leisure_services',

    # cultural_educational_services
    'school': 'cultural_educational_services',
    'college': 'cultural_educational_services',
    'university': 'cultural_educational_services',
    'library': 'cultural_educational_services',
    'theatre': 'cultural_educational_services',
    'museum': 'cultural_educational_services',

    # shopping
    'convenience': 'shopping',
    'marketplace': 'shopping',
    'shopping_centre': 'shopping',
    'store': 'shopping',

    # housing_services
    'hotel': 'housing_services',
    'hostel': 'housing_services',
    'guest_house': 'housing_services',

    # governments_organizations
    'police': 'governments_organizations',
    'fire_station': 'governments_organizations',
    'townhall': 'governments_organizations',
    'courthouse': 'governments_organizations',

    # corporations
    'office': 'corporations',
    'coworking_space': 'corporations',

    # catering
    'restaurant': 'catering',
    'fast_food': 'catering',
    'cafe': 'catering',
    'pub': 'catering',
    'bar': 'catering',

    # transportation
    'bus_stop': 'transportation',
    'train_station': 'transportation',
    'airport': 'transportation',
    'parking': 'transportation',
    'toll_gantry': 'transportation',

    # public_services
    'post_office': 'public_services',
    'waste_disposal': 'public_services',
    'recycling': 'public_services',
    'water_point': 'public_services',
    'motorway_junctio': 'transportation',
    'traffic_signals': 'transportation',
    'crossing': 'transportation',
    'give_way': 'transportation',
    'stop': 'transportation',
    'turning_circle': 'transportation',
    'yes': 'public_services',
    'derail': 'transportation',
    'switch': 'transportation',
    'traffic_signals;': 'transportation',
    'bench': 'public_services',
    'ferry_terminal': 'transportation',
    'station': 'transportation',
    'level_crossing': 'transportation',
    'buffer_stop': 'transportation',
    'parking_entrance': 'transportation',
    'priority': 'transportation',
    'turning_loop': 'transportation',
    'station_site': 'transportation',
    'signal': 'transportation',
    'milestone': 'public_services',
    'subway_entrance': 'transportation',
    'surveillance': 'public_services',
    'cannon': 'scenic_spots',
    'drinking_water': 'medical_health_services',
    'place_of_worship': 'scenic_spots',
    'arts_centre': 'cultural_educational_services',
    'street_lamp': 'public_services',
    'toilets': 'public_services',
    'water_tower': 'public_services',
    'social_facility': 'medical_health_services',
    'memorial': 'scenic_spots',
    'bicycle_parking': 'transportation',
    'tower': 'scenic_spots',
    'studio': 'cultural_educational_services',
    'mast': 'public_services',
    'district': 'residential_areas',
    'maritime': 'transportation',
    'grave_yard': 'scenic_spots',
    'reservoir': 'public_services',
    'post_box': 'public_services',
    'flagpole': 'public_services',
    'research_institu': 'cultural_educational_services',
    'doctors': 'medical_health_services',
    'ruins': 'scenic_spots',
    'cinema': 'cultural_educational_services',
    'gallery': 'cultural_educational_services',
    'community_centre': 'cultural_educational_services',
    'kindergarten': 'cultural_educational_services',
    'prison': 'governments_organizations',
    'dormitory': 'residential_areas',
    'information': 'public_services',
    'water_works': 'public_services',
    'aerodrome': 'transportation',
    'lighthouse': 'scenic_spots',
    'waste_basket': 'public_services',
    'ice_cream': 'catering',
    'bicycle_rental': 'transportation',
    'veterinary': 'medical_health_services',
    'public_bookcase': 'public_services',
    'telephone': 'public_services',
    'fountain': 'scenic_spots',
    'fuel': 'transportation',
    'gas': 'transportation',
    'archaeological_s': 'scenic_spots',
    'railway_crossing': 'transportation',
    'picnic_site': 'sports_leisure_services',
    'elevator': 'public_services',
    'motorcycle_parki': 'transportation',
    'stripclub': 'sports_leisure_services',
    'taxi': 'transportation',
    'vending_machine': 'public_services',
    'chimney': 'public_services',
    'bbq': 'sports_leisure_services',
    'environmental_ha': 'public_services',
    'windmill': 'scenic_spots',
    'disused:restaura': 'catering',
    'car_sharing': 'transportation',
    'events_venue': 'cultural_educational_services',
    'driving_school': 'cultural_educational_services',
    'biergarten': 'catering',
    'turntable': 'transportation',
    'beacon': 'scenic_spots',
    'railway_station': 'transportation',
    'tomb': 'scenic_spots',
    'motel': 'housing_services',
    'car_wash': 'transportation',
    'crossover': 'transportation',
    'car_rental': 'transportation',
    'prep_school': 'cultural_educational_services',
    'survey_point': 'public_services',
    'clock': 'public_services',
    'bus_station': 'transportation',
    'nightclub': 'sports_leisure_services',
    'dojo': 'cultural_educational_services',
    'animal_shelter': 'domestic_services',
    'shelter': 'public_services',
    'compressed_air': 'public_services',
    'animal_boarding': 'domestic_services',
    'music_school': 'cultural_educational_services',
    'language_school': 'cultural_educational_services',
    'gambling': 'sports_leisure_services',
    'hookah_lounge': 'catering',
    'monastery': 'scenic_spots',
    'fortune_teller': 'scenic_spots',
    'shoe': 'domestic_services',
    'hairdresser': 'domestic_services',
    'acting_school': 'cultural_educational_services',
    'food_court': 'catering',
    'public_bath': 'public_services',
    'boat_rental': 'sports_leisure_services',
    'music_venue': 'cultural_educational_services',
    'steps': 'public_services',
    'loading_dock': 'transportation',
    'meditation_centr': 'cultural_educational_services',
    'sightseeing': 'scenic_spots',
    'warehouse': 'corporations',
    'social_centre': 'cultural_educational_services',
    'manhole': 'public_services',
    'pole': 'public_services',
    'drain': 'public_services',
    'karaoke_box': 'sports_leisure_services',
    'sewer_grate': 'public_services',
    'internet_cafe': 'catering',
    'service_station': 'transportation',
    'site': 'scenic_spots',
    'yard': 'public_services',
    'camp_site': 'sports_leisure_services',
    'wreck': 'scenic_spots',
    'bicycle_repair_s': 'transportation',
    'junction': 'transportation',
    'parking_space': 'transportation',
    'disused': 'public_services',
    'parcel_locker': 'shopping',
    'charging_station': 'transportation',
    'satellite_dish': 'public_services',
    'pier': 'transportation',
    'watering_place': 'public_services',
    'wifi;telephone;d': 'public_services',
    'ranger_station': 'governments_organizations',
    'casino': 'sports_leisure_services',
    'crane': 'transportation',
    'chalet': 'housing_services',
    'binoculars': 'sports_leisure_services',
    'shower': 'public_services',
    'taxi_point': 'transportation',
    'torii': 'scenic_spots',
    'aquarium': 'scenic_spots',
    'planetarium': 'scenic_spots',
    'wayside_cross': 'scenic_spots',
    'track': 'transportation',
    'training': 'cultural_educational_services',
    'payment_terminal': 'financial_institutions',
    'works': 'public_services',
    'swingerclub': 'sports_leisure_services',
    'technical_monume': 'scenic_spots',
    'manor': 'residential_areas',
    'services': 'public_services',
    'Saint_Nicholas_"': 'scenic_spots',
    'disused:pub': 'catering',
    'pumping_station': 'public_services',
    'tram_stop': 'transportation',
    'platform': 'transportation',
    'vehicle_inspecti': 'transportation',
    'mini_roundabout': 'transportation',
    'waste_transfer_s': 'public_services',
    'boundary_stone': 'public_services',
    'speed_camera': 'transportation',
    'graphic_design': 'corporations',
    'bus_stop;street_': 'transportation',
    'street_cabinet': 'public_services',
    'concert_hall': 'cultural_educational_services',
    'lounge': 'catering',
    'tank': 'public_services',
    'water_tap': 'public_services',
    'dressing_room': 'public_services',
    'bakery': 'catering',
    'post_depot': 'public_services',
    'antenna': 'public_services',
    'animal_training': 'domestic_services',
    'traffic_mirror': 'transportation',
    'library_dropoff': 'cultural_educational_services',
    'device_charging_': 'transportation',
    'trade_school': 'cultural_educational_services',
    'smoking_area': 'public_services',
    'photo_booth': 'public_services',
    'beauty_school': 'cultural_educational_services',
    'cafe;bar': 'catering',
    'rescue_station': 'public_services',
    'proposed': 'public_services',
    'radio station': 'public_services',
    'wayside_shrine': 'scenic_spots',
    'video_wall': 'public_services',
    'beehive': 'public_services',
    'monitoring_stati': 'public_services',
    'relay_box': 'public_services',
    'social_club': 'sports_leisure_services',
    'payment_centre': 'financial_institutions',
    'conference_centr': 'cultural_educational_services',
    'lounger': 'sports_leisure_services',
    'polling_station': 'governments_organizations',
    'stop;crossing': 'transportation',
    'food_sharing': 'shopping',
    'building': 'residential_areas',
    'trolley_bay': 'public_services',
    'pump': 'public_services',
    'bell': 'scenic_spots',
    'mailroom': 'corporations',
    'utility_pole': 'public_services',
    'letter_box': 'public_services',
    'hand_sanitizing': 'public_services',
    'massage_chair': 'domestic_services',
    'stroller_rental': 'transportation',
    'postal_relay_box': 'public_services',
    'table': 'public_services',
    'anchor': 'scenic_spots',
    'observatory': 'scenic_spots',
    'spur_junction': 'transportation',
    'printer': 'corporations',
    'cross': 'transportation',
    'give_box': 'public_services',
    'planter': 'public_services',
    'karaoke': 'sports_leisure_services',
    'storage_tank': 'public_services',
    'advertising': 'corporations',
    'owner_change': 'public_services',
    'driver_training': 'cultural_educational_services',
    'footway': 'transportation',
    'tutoring': 'cultural_educational_services',
    'trailhead': 'scenic_spots',
    'wastewater_plant': 'corporations',
    'workshop':'corporations',
}

# 将 FACILITY_T 映射到类别
poi_data['category'] = poi_data['type'].map(facility_classification).map(category_mapping)
poi_data = poi_data.dropna(subset=['category'])

# 应用该函数
poi_data['latitude'] = poi_data['geometry'].y
poi_data['longitude'] = poi_data['geometry'].x
poi_data2 = poi_data[(poi_data['longitude']>=lon_min)&(poi_data['latitude']>=lat_min)&(poi_data['longitude']<=lon_max)&(poi_data['latitude']<=lat_max)]
print(poi_data2.shape)

##step2: 网格化
grid_size = 20  # 分为 20x20 网格
lat_bins = np.linspace(lat_min, lat_max, grid_size + 1)
lon_bins = np.linspace(lon_min, lon_max, grid_size + 1)
# 为每条事故数据分配到网格
poi_data2["grid_x"] = pd.cut(poi_data2["longitude"], bins=lon_bins, labels=False, include_lowest=True)
poi_data2["grid_y"] = pd.cut(poi_data2["latitude"], bins=lat_bins, labels=False, include_lowest=True)
all_grids = pd.DataFrame([(x, y) for x in range(grid_size) for y in range(grid_size)], columns=['grid_x', 'grid_y'])

## step3: 合并
poi_data2 = poi_data2[['category','grid_x','grid_y']]
poi_data3 = poi_data2.groupby([ 'category','grid_x','grid_y']).size().reset_index(name='poi_cnt')

# 设置poi向量
# categories = list(range(14))
# result = poi_data3.groupby(['grid_x', 'grid_y']).apply(
#     lambda group: [
#         group.loc[group['FACILITY_T'] == cat, 'poi_cnt'].sum() if cat in group['FACILITY_T'].values else 0
#         for cat in categories]).reset_index(name='poi_vector')
# 使用 pivot 将 FACILITY_T 的每种类型作为列
poi_data4 = poi_data3.pivot(index=['grid_x', 'grid_y'], columns='category', values='poi_cnt')
poi_data4.reset_index(inplace=True)
poi_data4.columns.name = None

# 合并所有网格的坐标与实际的结果，确保每个网格都有对应的poi_vector
result1 = pd.merge(all_grids, poi_data4, on=['grid_x', 'grid_y'], how='left')
# 对于缺失的网格，将poi_vector填充为0
# result1['poi_vector'] = result1['poi_vector'].apply(lambda x: x if isinstance(x, list) else [0] * len(categories))
result1 = result1.fillna(0)
feature_dim = [0.0,      1.0,      2.0,      3.0,      4.0,
            5.0,      6.0,      7.0,      8.0,      9.0,     10.0,     11.0,
           12.0,     13.0]
all_data = result1[feature_dim].values
all_data = all_data.reshape(grid_size, grid_size, 14)

# 保存文件
# save_path = "./sparse_data_process/new_data1229/%s/poi2.csv"%(city)
# result1.to_csv(save_path, index=False)
# print(save_path,'保存完毕。')
print(all_data.shape)
save_path1 = "./new_data/%s/poi.pkl"%(city)
with open(save_path1, 'wb') as f:
    pickle.dump(all_data, f)
print(save_path1,'保存完毕～')
