# Using LlamaIndex to create a QA system over our documents using local Ollama models

from llama_index.core import GPTVectorStoreIndex, Document
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Set up our models:
# - Llama3 via Ollama for generating answers
# - BGE embeddings for semantic search
llm = Ollama(model="llama3", request_timeout=120.0)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

from llama_index.core import Settings

Settings.llm = llm
Settings.embed_model = embed_model
# response = llm.complete("What is the capital of France?")
# print(response)

def generate_answer(text: str, question: str) -> str:

    # Create a document from the input text
    document = Document(text=text)
    docs_list = [document]

    # Build a vector index for semantic search(Chunks the text)
    index = GPTVectorStoreIndex.from_documents(docs_list)
    
    query_engine = index.as_query_engine(similarity_top_k=3)

    response = query_engine.query(question)

    return response.response


