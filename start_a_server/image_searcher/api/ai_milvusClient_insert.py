from pymilvus import __version__
print(__version__)

from pymilvus import MilvusClient
import pickle
import os
from tqdm import tqdm

# 1. Set up a milvus client
client = MilvusClient(
    uri="http://localhost:19530",
    db_name="default"
)

save_path = r'y:\GOA-AIGC\98-goaTrainingData\Arch_200px_\stored_embeddings.pickle'
if os.path.isfile(save_path):
    with open(save_path, "rb") as file:
        embeddings = pickle.load(file)

for index,embedding in tqdm(enumerate(embeddings.values())):
    if index < 0:
        continue

    res = client.insert(
        collection_name="vec_table_COSINE",
        data={
            'my_id': index,
            'my_vector': embedding["image_embedding"].squeeze().tolist()
        }
    )

# 2. Close the client
client.close()

