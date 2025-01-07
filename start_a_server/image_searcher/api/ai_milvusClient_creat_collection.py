
from pymilvus import DataType, MilvusClient, DataType
from tqdm import tqdm

client = MilvusClient(
    uri="http://localhost:19530",
    db_name="default"
)

print('client.list_collections',client.list_collections())

schema = MilvusClient.create_schema(
    auto_id=False,
    enable_dynamic_field=False,
)

schema.add_field(field_name="my_id", datatype=DataType.INT64, is_primary=True)
schema.add_field(field_name="my_vector", datatype=DataType.FLOAT_VECTOR, dim=512)

index_params = client.prepare_index_params()

index_params.add_index(
    field_name="my_id",
    index_type="STL_SORT"
)

index_params.add_index(
    field_name="my_vector", 
    index_type="IVF_FLAT",
    # metric_type="IP",
    metric_type="COSINE",
    params={"nlist": 1024}
)

client.create_collection(
    # collection_name="vec_table_IP",
    collection_name="vec_table_COSINE",
    schema=schema,
    index_params=index_params
)


