from openai import OpenAI
import logging
from typing import List, Dict, Any, Optional
from secrets import OPENROUTER_API_KEY, OPENROUTER_API_BASE

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class LanguageModel:
    def __init__(self, model_name: str,
                 temperature: float = 0.0, 
                 openrouter_api_key: str=OPENROUTER_API_KEY, 
                 openrouter_api_base: str=OPENROUTER_API_BASE,
                 **kwargs):
        try:
            self.client = OpenAI(
                base_url=openrouter_api_base,
                api_key=openrouter_api_key,
            )
            self.model_name = model_name
            self.temperature = temperature
            self.kwargs = kwargs
        except Exception as e:
            logger.error(f"Failed to initialize LanguageModel: {str(e)}")
            raise

    def ask(self, prompt: str = None, temperature: float = None):
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                "role": "user",
                "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content
    
    def __call__(self, prompt: str):
        try:
            return self.ask(prompt)
        except Exception as e:
            logger.error(f"Failed to process prompt: {str(e)}")
            raise
