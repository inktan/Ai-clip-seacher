import sqlite3
import sqlite_vec
import pickle
import torch
from tqdm import tqdm
from typing import List
import struct

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


def handle_db():
    # db = sqlite3.connect(":memory:")
    db = sqlite3.connect(db_path)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)

    sqlite_version, vec_version = db.execute(
        "select sqlite_version(), vec_version()"
    ).fetchone()

    print(f"sqlite_version={sqlite_version}, vec_version={vec_version}")

    # 前置处理
    # table_name = 'vec_normal'
    # del_table(table_name)

    # 普通表
    del_table(db,table_name_data_normal)
    if(not check_table_exists(db,table_name_data_normal)):
        db.execute(f'''CREATE TABLE {table_name_data_normal}
            (ID INT PRIMARY KEY     NOT NULL,
             PATH           BLOB    NOT NULL);''')
    db.commit()

    # 向量表
    del_table(db,table_name_vec)
    if(not check_table_exists(db,table_name_vec)):
        db.execute(f"CREATE VIRTUAL TABLE {table_name_vec} USING vec0(embedding float[{embedding_length}])")
    db.commit()

    return db

def main():
    db = handle_db()
    
    embedding_path=r'\\goa_4\\lVqVmp02Km\\38_044-house-in-troia-by-miguel-marcelino.jpeg'
    db.execute(f'''INSERT INTO {table_name_data_normal} (ID,PATH)
                VALUES (?, ?)''', (1, embedding_path))

    db.commit()
    
    # with db:
    #     for item in items:
    #         db.execute(
    #             f"INSERT INTO {table_name}(rowid, embedding) VALUES (?, ?)",
    #             [item[0], serialize_f32(item[1])],
    #         )

    # query_limit = 2
    # rows = db.execute(
    #     f"""
    #       SELECT
    #         rowid,
    #         distance
    #       FROM {table_name_vec}
    #       WHERE embedding MATCH ?
    #       ORDER BY distance
    #       LIMIT {query_limit}
    #     """,
    #     [serialize_f32(query)],
    # ).fetchall()

    # print(rows)
    
    
if __name__ == '__main__':
    
    db_path = r'D:\Ai-clip-seacher\stored_embeddings.db'
    table_name_data_normal = 'data_normal'

    table_name_vec = 'vec_table'
    embedding_length = 512

    stored_embeddings_path = r'd:\Ai-clip-seacher\stored_embeddings.pickle'
    
    main()