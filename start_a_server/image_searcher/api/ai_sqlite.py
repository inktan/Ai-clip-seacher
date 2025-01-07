import sqlite3
import pickle
import os
import torch
from tqdm import tqdm
from typing import List
import struct
from functools import wraps
import io, time, yaml, logging

def check_table_exists(db,table_name):
    # 检查表是否存在的SQL语句
    # 执行查询
    cursor = db.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    # 检查查询结果
    table_exists = cursor.fetchone()
    # 如果表存在，则删除它
    if table_exists:
        return True
    return False

def del_table(db,table_name):
    if(check_table_exists(db,table_name)):
        db.execute(f"DROP TABLE {table_name};")
        print(f"Table '{table_name}' was deleted.")
    
def create_db():
    db = sqlite3.connect(db_path)

    if(not check_table_exists(db,'data_normal')):
        db.execute(f'''CREATE TABLE data_normal
            (ID INT PRIMARY KEY     NOT NULL,
             PATH           TEXT    NOT NULL);''')
    db.commit()

    return db

if __name__ == '__main__':
    
    stored_embeddings_path = r'Y:\GOA-AIGC\98-goaTrainingData\ArchOctopus\stored_embeddings.pickle'
    db_path = r'Y:\GOA-AIGC\98-goaTrainingData\ArchOctopus\stored_paths.db'
    db = create_db()

    embeddings = {}
    if os.path.isfile(stored_embeddings_path):
        with open(stored_embeddings_path, "rb") as file:
            embeddings = pickle.load(file)

    embedding_paths =  list(embeddings.keys())

    # Adding paths to the database
    cursor = db.cursor()
    for index, path in tqdm(enumerate(embedding_paths)):
        if index < 1591752:
            continue
        # 检查PATH是否已存在
        # print(index)
        # cursor.execute("SELECT PATH FROM data_normal WHERE PATH = ?", (path,))
        # result = cursor.fetchone()
        
        # 如果PATH不存在，则添加到数据库
        # if result is None:
        cursor.execute("INSERT INTO data_normal (ID, PATH) VALUES (?, ?)", (index, path))
            # if index==100:
            #     break
    db.commit()

    
    