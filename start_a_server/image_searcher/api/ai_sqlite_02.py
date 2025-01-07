import sqlite3
import pickle
import os
import torch
from tqdm import tqdm
from typing import List
import struct
from functools import wraps
import io, time, yaml, logging
from PIL import Image

db_path = r'y:\GOA-AIGC\98-goaTrainingData\Arch_200px_\stored_paths.db'
db = sqlite3.connect(db_path)
table_name_data_normal = 'data_normal'
# count = db.execute(f'SELECT COUNT(PATH) FROM {table_name_data_normal} WHERE path IS NOT NULL').fetchone()[0]
# image_paths = db.execute(f"SELECT PATH FROM {table_name_data_normal}").fetchall()  

# 检索所有路径
cursor = db.cursor()
cursor.execute(f"SELECT id, path FROM {table_name_data_normal} WHERE path IS NOT NULL")
rows = cursor.fetchall()

# 处理每个路径
for index, row in tqdm(enumerate(rows)):
    image_id, image_path = row
    # print(image_id)
    # if image_id%1000==0:
    #     db.commit()
    #     print(image_id)
        # break
    try:
        img_path =os.path.join(r'Y:\GOA-AIGC\98-goaTrainingData\Arch_200px_',image_path)
        with Image.open(img_path) as img:
            width, height = img.size

            # 更新数据库中的尺寸
            cursor.execute(f"""
                UPDATE {table_name_data_normal}
                SET thumbnail_width = ?, thumbnail_height = ?
                WHERE id = ?
            """, (width, height, image_id))

            # print(f"图片路径: {img_path}, 尺寸: 宽度={width}, 高度={height}")
    except Exception as e:
        print(f"无法打开图片 {img_path}: {e}")

    if image_id%1000==0:
        db.commit()
        print(image_id)

# db.execute(f"ALTER TABLE {table_name_data_normal} ADD COLUMN thumbnail_width INTEGER")
# db.execute(f"ALTER TABLE {table_name_data_normal} ADD COLUMN thumbnail_height INTEGER")


db.commit()
db.close()

# large_width
# xlarge_width
# medium_width
# small_width
# thumbnail_width

# large_height 
# xlarge_height 
# medium_height 
# small_height 
# thumbnail_height

# "image_large_url": "https://i.pinimg.com/140x140_RS/eb/41/8b/eb418bb630ba39d04a904c853672c3ab.jpg",
# "image_xlarge_url": "https://i.pinimg.com/280x280_RS/eb/41/8b/eb418bb630ba39d04a904c853672c3ab.jpg",
# "image_small_url": "https://i.pinimg.com/30x30_RS/eb/41/8b/eb418bb630ba39d04a904c853672c3ab.jpg",
# "image_medium_url": "https://i.pinimg.com/75x75_RS/eb/41/8b/eb418bb630ba39d04a904c853672c3ab.jpg",
# "image_thumbnail_url": "https://i.pinimg.com/upload/4011155857531882_board_thumbnail_2024-11-19-04-00-23_64119_60.jpg",
# "node_id": "Qm9hcmQ6NDAxMTE1NTg1NzUzMTg4Mg==",
             
# "images": {
#     "170x": [
#         {
#             "url": "https://i.pinimg.com/170x/27/9b/57/279b5736ff590b8528a881463d5fb189.jpg",
#             "width": 170,
#             "height": 226,
#             "dominant_color": "#B88364"
#         },
#         {
#             "url": "https://i.pinimg.com/170x/a1/c8/ea/a1c8ea356201fcf97e752fbec1bc6f15.jpg",
#             "width": 170,
#             "height": 95,
#             "dominant_color": "#75715F"
#         },
#         {
#             "url": "https://i.pinimg.com/170x/8e/cd/1c/8ecd1c61f8f1a5fa500c1f415386c5e0.jpg",
#             "width": 170,
#             "height": 114,
#             "dominant_color": "#111407"
#         },
#         {
#             "url": "https://i.pinimg.com/170x/fb/71/3d/fb713d54802fc622b7b0ebda746ce898.jpg",
#             "width": 170,
#             "height": 113,
#             "dominant_color": "#000000"
#         },
#         {
#             "url": "https://i.pinimg.com/170x/93/2d/fe/932dfe2aa6455808f065a9b1d83f8bf3.jpg",
#             "width": 170,
#             "height": 106,
#             "dominant_color": "#25262B"
#         },
#         {
#             "url": "https://i.pinimg.com/170x/6e/79/e0/6e79e087228b36f36ff69c1576d55172.jpg",
#             "width": 170,
#             "height": 212,
#             "dominant_color": "#89897B"
#         },
#         {
#             "url": "https://i.pinimg.com/170x/d4/e5/54/d4e5548af5c51dabef2476f986164730.jpg",
#             "width": 170,
#             "height": 302,
#             "dominant_color": "#121315"
#         },
#         {
#             "url": "https://i.pinimg.com/170x/a7/ad/7a/a7ad7ab16925be03286142928b15afeb.jpg",
#             "width": 170,
#             "height": 216,
#             "dominant_color": "#050805"
#         },
#         {
#             "url": "https://i.pinimg.com/170x/4e/1a/6b/4e1a6be5231cd285da47a3626339d25b.jpg",
#             "width": 170,
#             "height": 212,
#             "dominant_color": "#0E1B28"
#         },
#         {
#             "url": "https://i.pinimg.com/170x/fc/2a/ac/fc2aac4d43ad54a7056bb1045bde323d.jpg",
#             "width": 170,
#             "height": 246,
#             "dominant_color": "#212122"
#         }
#     ]
# },

# "aggregated_pin_data": {
#     "node_id": "QWdncmVnYXRlZFBpbkRhdGE6NTI1NTM4MjA5NDAxNzc3OTQ3Ng==",
#     "has_xy_tags": false
# },
# "images": {
#     "170x": {
#         "width": 236,
#         "height": 134,
#         "url": "https://i.pinimg.com/236x/05/91/6f/05916f11f83b51961fdc20659a92b91e.jpg"
#     },
#     "236x": {
#         "width": 236,
#         "height": 134,
#         "url": "https://i.pinimg.com/236x/05/91/6f/05916f11f83b51961fdc20659a92b91e.jpg"
#     },
#     "474x": {
#         "width": 474,
#         "height": 271,
#         "url": "https://i.pinimg.com/474x/05/91/6f/05916f11f83b51961fdc20659a92b91e.jpg"
#     },
#     "564x": {
#         "width": 564,
#         "height": 322,
#         "url": "https://i.pinimg.com/564x/05/91/6f/05916f11f83b51961fdc20659a92b91e.jpg"
#     },
#     "736x": {
#         "width": 626,
#         "height": 358,
#         "url": "https://i.pinimg.com/736x/05/91/6f/05916f11f83b51961fdc20659a92b91e.jpg"
#     },
#     "orig": {
#         "width": 626,
#         "height": 358,
#         "url": "https://i.pinimg.com/originals/05/91/6f/05916f11f83b51961fdc20659a92b91e.jpg"
#     }
# }