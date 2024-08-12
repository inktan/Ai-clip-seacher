import os
from typing import List
import logging
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
Image.MAX_IMAGE_PIXELS = None  # 这将移除像素数量的限制

class ClipEmbedder:
    def __init__(self):
        # self.model_name = "openai/clip-vit-base-patch32"

        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        self.model_name = f"{current_directory}/openai/clip-vit-base-patch32"

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f"device： {self.device}")
        
        self.model = CLIPModel.from_pretrained(self.model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(self.model_name)

    def embed_images(self, images: List[Image.Image]):
        with torch.no_grad():
            inputs = self.processor(text=None, images=images, return_tensors="pt", padding=True)
            image_embeds = self.model.get_image_features(**inputs.to(self.device)).to("cpu")
            image_embeds = image_embeds / image_embeds.norm(dim=-1, keepdim=True)

        return image_embeds

    def embed_text(self, text: str):
        """
        Embed the query in a 512 dim vector.

        :param text: The search query - A single text string
        :return: The feature vector
        """
        with torch.no_grad():
            inputs = self.processor(text=text, images=None, return_tensors="pt", padding=True)
            text_embeds = self.model.get_text_features(**inputs.to(self.device)).to("cpu")
            text_embeds = text_embeds / text_embeds.norm(dim=-1, keepdim=True)
        return text_embeds
