from typing import Iterator
from openai import OpenAI
from src.infrastructure.config import settings

class OpenAIClient:
    """Generic OpenAI client for streaming completions."""
    
    def __init__(self, api_key: str | None = None):
        self.client = OpenAI(api_key=api_key or settings.openai_api_key)
    
    def stream_completion(
        self,
        question: str,
        context: str,
        model: str = settings.openai_chat_model,
        system_prompt: str | None = None
    ) -> Iterator[str]:
        """
        Stream completion with context.
        
        Args:
            question: User's question
            context: Context string (formatted by application layer)
            model: OpenAI model to use
            system_prompt: Optional custom system prompt
            
        Yields:
            Chunks of the streaming response
        """
        default_system_prompt = (
            "You are a helpful assistant. Answer questions based on the provided context. "
            "If the context doesn't contain relevant information, say so."
        )
        
        messages = [
            {"role": "system", "content": system_prompt or default_system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
        
        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content