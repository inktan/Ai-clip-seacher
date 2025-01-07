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

if __name__ == '__main__':
    
    stored_embeddings_path = r'Y:\GOA-AIGC\98-goaTrainingData\Arch_200px_\stored_embeddings.pickle'

    embeddings = {}
    if os.path.isfile(stored_embeddings_path):
        with open(stored_embeddings_path, "rb") as file:
            embeddings = pickle.load(file)

    # embedding_paths =  list(embeddings.keys())

    # 遍历dict并添加宽度和高度
    for index, key in tqdm(enumerate(embeddings)):
        # if index < 1591752:
        #     continue
        try:
            img_path =os.path.join(r'Y:\GOA-AIGC\98-goaTrainingData\Arch_200px_',key)
            with Image.open(img_path) as img:
                width, height = img.size

                embeddings[key]["thumbnail_width"] = width
                embeddings[key]["thumbnail_height"] = height
                # print(f"图片路径: {img_path}, 尺寸: 宽度={width}, 高度={height}")
                # print(key,embeddings[key])
        except Exception as e:
            print(f"无法打开图片 {img_path}: {e}")

        if index%1000==0:
            print(index)
            # break

        if index%20000==0:
            print(index)
            with open(stored_embeddings_path, "wb") as file:
                pickle.dump(embeddings, file)
