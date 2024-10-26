import torch
from tqdm import tqdm
import sqlite3
from decorator import timer_decorator

from image_searcher.interfaces.image_loader import ImageLoader
from image_searcher.interfaces.result_interface import RankedImage
from image_searcher.interfaces.stored_embeddings import StoredEmbeddings
from image_searcher.embedders.clip_embedder import ClipEmbedder

# from pymilvus import MilvusClient, Collection, DataType
from tqdm import tqdm

# image_dir_path='Y:\GOA-AIGC\98-goaTrainingData\ArchOctopus\archcollege'
# stroed_embeddings_save_path='Y:\GOA-AIGC\98-goaTrainingData\ArchOctopus\archcollege-embedding'
# 
# image_dir_path=r'Y:\GOA-AIGC\98-goaTrainingData\ArchOctopus_thumbnail_200px'
# stroed_embeddings_save_path=r'Y:\GOA-AIGC\98-goaTrainingData\ArchOctopus_thumbnail_200px'
# image_dir_path='D:\Ai-clip-seacher\AiArchLib1k'
# stroed_embeddings_save_path='D:\Ai-clip-seacher\AiArchLib1k'
# traverse=True # true为迭代文件夹中的嵌套子文件夹
# include_faces=False
# reindex=False # false不判断图片库是否有更新，true判断保存的语义数据库与当前图片库是否一致，不一致则重新建立索引
# db_path = r'd:\Ai-clip-seacher\sqlite\stored_paths.db'

class Search:
    def __init__(self,
                 image_dir_path: str = None,
                 traverse: bool = False,
                 save_path: str = None,
                 reindex: bool = True,
                 include_faces: bool = False,
                 face_model: str = "large",
                 face_num_jitters: int = 5):

        # assert (image_dir_path is not None or save_path is not None), "At least one of the paths " \
        #                                                               "(image and save path) needs to be specified"

        self.loader = ImageLoader(image_dir_path=image_dir_path, traverse=traverse)
        self.include_faces = include_faces

        print("Loading CLIP Embedder")
        self.embedder = ClipEmbedder()

        print("Loading pre-computed embeddings")
        self.stored_embeddings = StoredEmbeddings(save_path=save_path if save_path else image_dir_path)
        print(f"{len(self.stored_embeddings.get_image_paths())} files are indexed.")

        self.image_path_prefix = r"Y:\GOA-AIGC\98-goaTrainingData\ArchOctopus\\"
        # self.image_path_prefix = r"D:\Ai-clip-seacher\AiArchLib1k"
        # self.image_path_prefix = ""
        print("Waiting for server to start ...")
        if reindex:
            print(f"Re-indexing the image files in {image_dir_path}")
            self.reindex()
        if len(self.stored_embeddings.embeddings)>0:
            self.stored_embeddings.set_embedding_tensor()
        
        # sqlite3
        # db_path = r'd:\Ai-clip-seacher\sqlite\stored_embeddings_202408141501.db'
        # self.db = sqlite3.connect(db_path)
        # self.db.enable_load_extension(True)
        # sqlite_vec.load(self.db)
        # self.db.enable_load_extension(False)

        # sqlite_version, vec_version = self.db.execute(
        #     "select sqlite_version(), vec_version()"
        # ).fetchone()

        # print(f"sqlite_version={sqlite_version}, vec_version={vec_version}")

        # sqlite3
        # self.db = sqlite3.connect(db_path)

        # self.table_name_data_normal = 'data_normal'
        # self.count = self.db.execute(f'SELECT COUNT(PATH) FROM {self.table_name_data_normal} WHERE path IS NOT NULL').fetchone()[0]

        # self.client = MilvusClient(
        #     uri="http://localhost:19530",
        #     db_name="default"
        # )

        # print('client.list_collections',self.client.list_collections())

        # vec_table_COSINE
        # vec_table_IP
        # vec_table

        # self.table_name_vec = 'vec_table_COSINE'
        # self.client.release_collection(collection_name="vec_table_IP")
        # self.client.load_collection(collection_name=self.table_name_vec)
        
        print("Setup over, Searcher is ready to be queried")

    def reindex(self):
        image_paths_stored = [self.image_path_prefix + i for i in self.stored_embeddings.get_image_paths()]
        waiting_list = set(self.loader.search_tree()) - set(image_paths_stored)
        if not waiting_list:
            return
        
        for idx, image_path in enumerate(tqdm(waiting_list)):
            self.index_image(image_path)
            
            if idx % 30000 == 0:
                self.stored_embeddings.update_file()
        self.stored_embeddings.update_file()

    def index_image(self, image_path):
        try:
            images = [self.loader.open_image(image_path)]
            image_path = image_path.replace(self.image_path_prefix, "")
            self.stored_embeddings.add_embedding(image_path, self.embedder.embed_images(images))
            if self.include_faces:
                print('==')

        except Exception as exception:
            image_path = image_path.replace(self.image_path_prefix, "")
            self.stored_embeddings.add_embedding(image_path, torch.zeros((1, 512)))

    def rank_images_by_query_image(self, imageWeight,query: str, qury_image, n01,n02):
        '''基于图片和提示词进行搜索'''
        image_embeds, image_paths = self.stored_embeddings.get_embedding_tensor()

        query_embed = self.embedder.embed_text(query)
        if imageWeight!=0:
            iamge_embeds = self.embedder.embed_images(qury_image)
            query_embed = imageWeight * iamge_embeds + (1-imageWeight) * query_embed

        scores = (torch.matmul(query_embed, image_embeds.t()) * 100).softmax(dim=1).squeeze().numpy().astype(float)
        best_images = sorted(list(zip(image_paths, scores)), key=lambda x: x[1], reverse=True)[n01:n02]
        ranked_images = [RankedImage(image_path=path, score=score) for path, score in best_images]
        image_paths_list = [image.image_path for image in ranked_images]
        return image_paths_list
    
    @timer_decorator
    def rank_images_by_query_sqlite_image(self, imageWeight,query: str, qury_image, n01,n02):
        '''基于图片和提示词进行搜索'''

        query_embed = self.embedder.embed_text(query)
        if imageWeight!=0:
            iamge_embeds = self.embedder.embed_images(qury_image)
            query_embed = imageWeight * iamge_embeds + (1-imageWeight) * query_embed

        # query_limit = n02
        # rows = self.db.execute(
        #     f"""
        #     SELECT rowid, distance
        #     FROM {self.table_name_vec}
        #     WHERE embedding MATCH ?
        #     ORDER BY distance
        #     LIMIT {query_limit}
        #     """,
        #     [query_embed.numpy()[0]],
        # ).fetchall()
        # print(rows)

        # first_elements = [tup[0] for tup in rows]  
        # ids_str = ','.join(map(str, first_elements))  
        # rows = self.db.execute(f"SELECT * FROM {self.table_name_data_normal} WHERE rowid IN ({ids_str})").fetchall()  

        # first_elements = [tup[1] for tup in rows]  
        # return first_elements[n01:n02]

        vectors_to_search = [query_embed.numpy()[0].tolist()]
        search_params = {
            # "metric_type": "L2", # L2 (欧几里得距离) 指两个向量在欧几里得空间中的直线距离。
            # "metric_type": "IP", # IP (内积，也称为点积) IP度量是指两个向量的内积，它衡量了两个向量在方向上的相似度。
            "metric_type": "COSINE", # COSINE (余弦相似度) COSINE度量衡量的是两个向量方向上的相似度，而不是它们的欧几里得距离或大小。
            "params": {},
        }
        res = self.client.search(
            collection_name=self.table_name_vec,
            data=vectors_to_search,
            limit=n02,
            search_params=search_params,
            output_fields=['my_id']
        )
        ids = [dict_['id'] for dict_ in res[0]]
        ids_str = ','.join(map(str, ids))  
        rows = self.db.execute(f'''
            SELECT * 
            FROM {self.table_name_data_normal} 
            WHERE ID IN ({ids_str})
            ''').fetchall() 

        order_dict = {val: idx for idx, val in enumerate(ids)}
        sorted_tuples = sorted(rows, key=lambda x: order_dict[x[0]])  
        random_image_paths = [tup[1] for tup in sorted_tuples]  
        
        return random_image_paths        

        