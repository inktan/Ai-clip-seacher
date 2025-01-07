
from pymilvus import DataType, MilvusClient, DataType
from tqdm import tqdm

client = MilvusClient(
    uri="http://localhost:19530",
    db_name="default"
)

print('client.list_collections',client.list_collections())

# client.drop_collection(collection_name="vec_table_L2")
# client.drop_collection(collection_name="vec_table_IP")
# client.drop_collection(collection_name="vec_table_COSINE")

# client.load_collection('vec_table') 
  
# res = client.query(
#     collection_name="vec_table",
#     filter="",
#     limit=50,
# ) 
# print(len(res))

res = client.describe_collection(collection_name="vec_table_COSINE")
print(res)
# 获取集合中的向量总数  
# total_count = client.get_collection_stats(collection_name="vec_table_L2")  
# total_count = client.get_collection_stats(collection_name="vec_table_IP")  
total_count = client.get_collection_stats(collection_name="vec_table_COSINE")  
  
print(f"Total number of vectors : {total_count}")
