"""
Generator: Calls DeepSeek-R1 for final response using augmented prompt.
"""
from openai import OpenAI
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class RAGGenerator:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.deepseek.com/v1",
            api_key=os.getenv("DEEPSEEK_API_KEY")
        )
        self.model = "deepseek-r1"

    def generate(self, augmented: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert and helpful e-commerce customer assistant."},
                    {"role": "user", "content": augmented["prompt"]}
                ],
                temperature=0.3,
                max_tokens=500
            )
            answer = response.choices[0].message.content.strip()

            return {
                "response": answer,
                "metadata": augmented["metadata"]
            }
        except Exception as e:
            return {
                "response": "Sorry, I'm having trouble answering right now.",
                "metadata": {"error": str(e), "sources": [], "confidence": 0.0}
            }