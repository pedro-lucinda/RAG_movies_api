"""Server-Sent Events (SSE) formatting utilities."""
import json
from typing import Iterator
from datetime import datetime

SSE_HEADERS = {
    "Connection": "keep-alive",
    "Cache-Control": "no-cache"
}

def format_sse(chunk: str) -> str:
    """Format chunk as Server-Sent Events (SSE) format."""
    return f"data: {chunk}\n\n"

def format_sse_error(error: str) -> str:
    """Format error as SSE event."""
    error_data = json.dumps({"error": error})
    return f"data: {error_data}\n\n"

def format_sse_heartbeat() -> str:
    """Format SSE heartbeat comment."""
    return ": keep-alive\n\n"

def create_error_stream(error_message: str) -> Iterator[str]:
    """Create a stream with a single error event."""
    yield format_sse_error(error_message)

def sse_stream_iterator(iterator: Iterator[str], heartbeat_interval: int = 15) -> Iterator[str]:
    """
    Wrap content stream with SSE heartbeats, completion event, and error handling.
    
    Args:
        iterator: Iterator that yields content chunks
        heartbeat_interval: Seconds between heartbeats (default 15)
    
    Yields:
        SSE-formatted events including heartbeats, data, completion, or errors
    """
    last_heartbeat = datetime.now()
    has_data = False
    
    try:
        for chunk in iterator:
            has_data = True
            current_time = datetime.now()
            
            time_since_heartbeat = (current_time - last_heartbeat).total_seconds()
            if time_since_heartbeat >= heartbeat_interval:
                yield format_sse_heartbeat()
                last_heartbeat = current_time
            
            yield format_sse(chunk)
        
        if has_data:
            yield format_sse("[DONE]")
            
    except Exception as e:
        yield format_sse_error(str(e))
