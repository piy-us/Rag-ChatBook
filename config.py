from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core.embeddings import resolve_embed_model
# from llama_index.core import (
#     StorageContext, 
#     ServiceContext, 
#     load_index_from_storage
# )

Settings.llm = Groq(model="llama3-70b-8192", api_key="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")
#Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
#embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
# Settings.embed_model = HuggingFaceEmbedding(
#     model_name="BAAI/bge-m3"
# )
Settings.embed_model = resolve_embed_model("local:BAAI/bge-m3")
embed_model = resolve_embed_model("local:BAAI/bge-m3")
