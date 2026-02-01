from abc import ABC, abstractmethod
from typing import Iterator


class LLMClient(ABC):
    """Abstract interface for LLM completion services."""
    
    @abstractmethod
    def stream_completion(
        self,
        question: str,
        context: str,
        model: str,
        system_prompt: str | None = None
    ) -> Iterator[str]:
        """
        Stream completion with context.
        
        Args:
            question: User's question
            context: Context string
            model: Model identifier to use
            system_prompt: Optional custom system prompt
            
        Yields:
            Chunks of the streaming response
        """
        pass
