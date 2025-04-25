"""
Author: chenzuoming

File: reflection.py
Description: 
"""
from transformers import pipeline
from .translation import BaiDuTransTool
from settings import HUGGINGFACE_TOKEN
bd = BaiDuTransTool()
class ReflectionTool:
    def __init__(self, model_name: str, device: str, torch_dtype: str):
        self.text_emotion_pipe = pipeline(
            "text-classification",
            model=model_name,
            top_k=None,
            device=device,
            torch_dtype=torch_dtype,
            token=HUGGINGFACE_TOKEN
        )

    def classify_text_emotion(self, text: str) -> list:
        output = self.text_emotion_pipe(
            bd.trans_zh_to_en(text),
            truncation=True,
            max_length=self.text_emotion_pipe.model.config.max_position_embeddings,
        )[0]
        return sorted(output, key=lambda x: x["score"], reverse=True)