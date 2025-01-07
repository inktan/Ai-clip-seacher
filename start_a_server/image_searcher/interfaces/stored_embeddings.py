# pylint:disable=no-member
import pickle
import os
from tqdm import tqdm

import torch

class StoredEmbeddings:
    def __init__(self, save_path: str):
        self.save_path = save_path
        if os.path.isdir(save_path):
            self.save_path = os.path.join(save_path, "stored_embeddings.pickle")

        self.embeddings = {}
        self.image_path_prefix = "Y:/GOA-AIGC/98-goaTrainingData/ArchOctopus/"
        if os.path.isfile(self.save_path):
            with open(self.save_path, "rb") as file:
                self.embeddings = pickle.load(file)
                # 现在遍历 embeddings 的所有键
                # for image_path in tqdm(list(self.embeddings.keys())):
                    # 检查文件是否存在  
                    # if not os.path.exists(self.image_path_prefix + image_path):
                        # 如果文件不存在，则删除对应的键值对  
                        # del self.embeddings[image_path]

        self.embedding_paths = []
        self.embedding_tensor = []
        
    def get_image_paths(self):
        return list(self.embeddings.keys())

    def add_embedding(self, image_path, embedding):
        assert embedding.shape == (1, 512)
        self.embeddings[image_path] = {"image_embedding": embedding}

    def set_embedding_tensor(self):
        self.embedding_tensor = torch.cat(tuple(x["image_embedding"] for x in self.embeddings.values()), dim=0)
        self.embedding_paths = self.get_image_paths()

    def get_embedding_tensor(self):
        return self.embedding_tensor, self.embedding_paths

    def get_all_face_embeddings(self):
        return self.face_embedding_tensor, self.face_embedding_paths

    def set_all_face_embeddings(self):
        # comprehension: torch.Tensor(np.array(list(x for y in self.embeddings.values() for x in y["face_embeddings"])))
        face_embeddings = []
        embedding_path = []

        for key, value in self.embeddings.items():
            if "face_embeddings" in value.keys():   # Normally, this line should not be needed
                for x in value["face_embeddings"]:
                    face_embeddings.append(x)
                    embedding_path.append(key)
        self.face_embedding_tensor = torch.Tensor(face_embeddings)
        self.face_embedding_paths = embedding_path

    def update_file(self, ignore_flag: bool = False):
        """This method should be called when reindex is done"""
        with open(self.save_path, "wb") as file:
            pickle.dump(self.embeddings, file)

