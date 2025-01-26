import openai
from typing import List, Dict, Optional

class ChatInterface:
    def __init__(self, api_key: str, base_url: str = "https://api.fireworks.ai/inference/v1"):
        """Initialize the chat interface with API credentials."""
        self.client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
    
    def get_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "accounts/sentientfoundation/models/dobby-mini-unhinged-llama-3-1-8b#accounts/sentientfoundation/deployments/81e155fc",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """Get a chat completion from the API."""
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content