from openai import AsyncOpenAI

from geodle_chat.core.config import settings

api_key = settings.OPENAI_API_KEY

if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

client = AsyncOpenAI(api_key=api_key)

async def generate_answer_stream(conversation: list, model: str = "gpt-4.1-mini", temperature: float = 1) -> str:
    response = await client.chat.completions.create(
        model=model,
        messages=conversation,
        temperature=temperature,
        max_completion_tokens=80,
        stream=True # Make sure response is returned as stream
    )
    async for chunk in response:
        delta = chunk.choices[0].delta
        chunk_text = delta.content or ""
        yield chunk_text