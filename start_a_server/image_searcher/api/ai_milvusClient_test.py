
from pymilvus import DataType, MilvusClient, DataType
from tqdm import tqdm

client = MilvusClient(
    uri="http://localhost:19530",
    db_name="default"
)

print('client.list_collections',client.list_collections())

# client.drop_collection(collection_name="vec_table")
# client.drop_collection(collection_name="vec_table_IP")
# client.drop_collection(collection_name="vec_table_COSINE")

# client.load_collection('vec_table') 
  
# res = client.query(
#     collection_name="vec_table",
#     filter="",
#     limit=50,
# ) 
# print(len(res))

# res = client.describe_collection(collection_name="vec_table")
# print(res)
# 获取集合中的向量总数  
# total_count = client.get_collection_stats(collection_name="vec_table")  
# total_count = client.get_collection_stats(collection_name="vec_table_IP")  
# total_count = client.get_collection_stats(collection_name="vec_table_COSINE")  
  
# print(f"Total number of vectors : {total_count}")

# for i in tqdm(range(total_count['row_count'])):
#     client.delete(
#         collection_name="vec_table_IP",
#         ids=[i]
#     )
# client.refresh_load(collection_name="vec_table_IP")

# start_id = 0  # 或者从某个已知的最大ID开始  
# batch_size = 16300  
# for i in tqdm(range(0, total_count['row_count'], batch_size)):  
#     end_id = min(i + batch_size, total_count['row_count'])  
#     ids_to_query = list(range(start_id + i, start_id + end_id)) 
#     print(ids_to_query)
    # res = client.query(
    #     collection_name="vec_table",
    #     filter=f"my_id in {ids_to_query}",
    #     limit=batch_size,
    #     output_fields=["my_id", "my_vector"],
    # )

    # client.insert(
    #     collection_name="vec_table_COSINE",
    #     data=res
    # )

    # client.insert(
    #     collection_name="vec_table_IP",
    #     data=res
    # )

    # print(len(res))
    # print((res[0]))
    # print(type(res[0]))
    # print(type(res))
    # break

# schema = MilvusClient.create_schema(
#     auto_id=False,
#     enable_dynamic_field=False,
# )

# schema.add_field(field_name="my_id", datatype=DataType.INT64, is_primary=True)
# schema.add_field(field_name="my_vector", datatype=DataType.FLOAT_VECTOR, dim=512)

# index_params = client.prepare_index_params()

# index_params.add_index(
#     field_name="my_id",
#     index_type="STL_SORT"
# )

# index_params.add_index(
#     field_name="my_vector", 
#     index_type="IVF_FLAT",
#     metric_type="IP",
    # metric_type="COSINE",
#     params={"nlist": 1024}
# )

# client.create_collection(
#     collection_name="vec_table_IP",
    # collection_name="vec_table_COSINE",
#     schema=schema,
#     index_params=index_params
# )

# schema = MilvusClient.create_schema(
#     auto_id=True,
#     enable_dynamic_field=False,
# )


