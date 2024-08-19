import sqlite3
import sqlite_vec
import pickle
import torch
from tqdm import tqdm
from typing import List
import struct
from functools import wraps
import io, time, yaml, logging

def timer_decorator(func):
    """装饰器，用于计算函数运行的时间"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 运行耗时: {end_time - start_time:.4f} 秒")
        return result
    return wrapper


def serialize_f32(vector: List[float]) -> bytes:
    """serializes a list of floats into a compact "raw bytes" format"""
    return struct.pack("%sf" % len(vector), *vector)

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

def get_embeddings():
    # 读取pickle数据库
    with open(stored_embeddings_path, "rb") as file:
        stored_embeddings = pickle.load(file)

        embedding_tensors = torch.cat(tuple(x["image_embedding"] for x in stored_embeddings.values()), dim=0)
        embedding_paths = list(stored_embeddings.keys())

        return embedding_paths, embedding_tensors
    
@timer_decorator
def handle_db():
    # db = sqlite3.connect(":memory:")
    db = sqlite3.connect(db_path)
    # db.enable_load_extension(True)
    # sqlite_vec.load(db)
    # db.enable_load_extension(False)

    # sqlite_version, vec_version = db.execute(
    #     "select sqlite_version(), vec_version()"
    # ).fetchone()

    # print(f"sqlite_version={sqlite_version}, vec_version={vec_version}")

    # 前置处理
    # table_name = 'vec_normal'
    # del_table(table_name)

    # 普通表
    del_table(db,table_name_data_normal)
    if(not check_table_exists(db,table_name_data_normal)):
        db.execute(f'''CREATE TABLE {table_name_data_normal}
            (ID INT PRIMARY KEY     NOT NULL,
             PATH           TEXT    NOT NULL);''')
    db.commit()

    # 向量表
    del_table(db,table_name_vec)
    # if(not check_table_exists(db,table_name_vec)):
    #     db.execute(f"CREATE VIRTUAL TABLE {table_name_vec} USING vec0(embedding float[{embedding_length}])")
    # db.commit()

    return db

@timer_decorator
def get_best_images(db):
    query = []
    for i in range(512):
        query.append(0.002)

    query_limit = 20
    rows = db.execute(
        f"""
          SELECT rowid, distance
          FROM {table_name_vec}
          WHERE embedding MATCH ?
          ORDER BY distance
          LIMIT {query_limit}
        """,
        [serialize_f32(query)],
    ).fetchall()

    print(rows)
    first_elements = [tup[0] for tup in rows]  
    print(first_elements)
    
    ids_str = ','.join(map(str, first_elements))  
    rows = db.execute(f"SELECT * FROM {table_name_data_normal} WHERE rowid IN ({ids_str})").fetchall()  
    print(rows)

    first_elements = [tup[1] for tup in rows]  
    print(first_elements)

def create_vec_db():
    db = handle_db()
    embedding_paths, embedding_tensors = get_embeddings()

    for index, item in tqdm(enumerate(embedding_paths), total=len(embedding_paths)):
        embedding_path = item
        # embedding_tensor = embedding_tensors[index]

        db.execute(f'''INSERT INTO {table_name_data_normal} (ID,PATH)
                    VALUES (?, ?)''', (index, embedding_path))

        # db.execute(f"INSERT INTO {table_name_vec} (rowid, embedding) VALUES (?, ?)",
        #         [index, serialize_f32(embedding_tensor.numpy().tolist())])

        # db.execute(f"INSERT INTO {table_name_vec} (rowid, embedding) VALUES (?, ?)",
        #         [index, embedding_tensor.numpy()])

        # if index>10000:
        #     db.commit()
        #     db.close()
        #     break
        #     continue

    db.commit()
    return db
    
if __name__ == '__main__':
    
    stored_embeddings_path = r'y:\GOA-AIGC\98-goaTrainingData\ArchOctopus_thumbnail_200px\stored_embeddings.pickle'
    db_path = r'D:\Ai-clip-seacher\sqlite\stored_paths_202408151104.db'
    table_name_data_normal = 'data_normal'

    table_name_vec = 'vec_table'
    embedding_length = 512

    db = create_vec_db()

    # db = sqlite3.connect(db_path)
    # db.enable_load_extension(True)
    # sqlite_vec.load(db)
    # db.enable_load_extension(False)

    # get_best_images(db)
