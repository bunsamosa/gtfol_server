from openai import AsyncOpenAI as OpenAI
from openai import types as openai_types

from utils.processor import preprocess_embedding


# create openai client
client = OpenAI()


async def embed_text(
    text: str,
    model="text-embedding-3-small",
) -> openai_types.CreateEmbeddingResponse:
    # preprocess text for generating embeddings
    text = await preprocess_embedding(text)

    # generate embeddings
    embedding = await client.embeddings.create(input=text, model=model)

    return embedding
