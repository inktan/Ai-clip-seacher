# pylint:disable=no-member
from typing import List, Tuple
import logging

import re
import numpy as np
import torch
from tqdm import tqdm

from image_searcher.interfaces.image_loader import ImageLoader
from image_searcher.interfaces.result_interface import RankedImage
from image_searcher.interfaces.stored_embeddings import StoredEmbeddings
from image_searcher.embedders.clip_embedder import ClipEmbedder

import timeit  
import random

class Search:
    def __init__(self,
                 image_dir_path: str = None,
                 traverse: bool = False,
                 save_path: str = None,
                 reindex: bool = True,
                 include_faces: bool = False,
                 face_model: str = "large",
                 face_num_jitters: int = 5):

        assert (image_dir_path is not None or save_path is not None), "At least one of the paths " \
                                                                      "(image and save path) needs to be specified"

        self.loader = ImageLoader(image_dir_path=image_dir_path, traverse=traverse)
        self.include_faces = include_faces

        logging.info("Loading CLIP Embedder")
        self.embedder = ClipEmbedder()

        logging.info("Loading pre-computed embeddings")
        self.stored_embeddings = StoredEmbeddings(save_path=save_path if save_path else image_dir_path)
        logging.info(f"{len(self.stored_embeddings.get_image_paths())} files are indexed.")

        self.image_path_prefix = "Y:\\GOA-AIGC\\98-goaTrainingData\\ArchOctopus\\"
        self.image_path_prefix = "D:\Ai-clip-seacher\AiArchLib1k"
        # self.image_path_prefix = ""
        logging.info("Waiting for server to start ...")
        if reindex:
            logging.info(f"Re-indexing the image files in {image_dir_path}")
            self.reindex()

        self.stored_embeddings.set_embedding_tensor()

        logging.info("Setup over, Searcher is ready to be queried")

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
            logging.warning(f"Image {image_path} has failed to process - adding it to fail list.")
            image_path = image_path.replace(self.image_path_prefix, "")
            self.stored_embeddings.add_embedding(image_path, torch.zeros((1, 512)))
            logging.warning(exception)

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
    
    def random_images(self, n: int = 300):
        '''随机选择300个图片'''
        image_embeds, image_paths = self.stored_embeddings.get_embedding_tensor()
        # 检查列表中的图片数量是否足够
        if len(image_paths) < 300:
            return image_paths
        else:
            # 生成300个随机整数索引
            random_indices = random.sample(range(len(image_paths)), n)
            # 使用这些索引从image_paths中提取一个新的列表
            random_image_paths = [image_paths[i] for i in random_indices]
            # 从列表中随机选择300个图片路径
            return random_image_paths
        
    def project_content(self, project_path):
        '''获取一个项目的所有相关信息'''
        image_embeds, image_paths = self.stored_embeddings.get_embedding_tensor()
        # 使用filter函数筛选出包含 "project_path" 的元素
        filtered_list = list(filter(lambda s: project_path in s, image_paths))
        return filtered_list
        