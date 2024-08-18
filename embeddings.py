from llama_index.core.node_parser import SentenceSplitter
from config import embed_model
from llama_index.core import Settings

def generate_embeddings(documents):
    node_parser = SentenceSplitter(chunk_size=512)
    nodes = node_parser.get_nodes_from_documents(documents)
    
    for node in nodes:
        node_embedding = embed_model.get_text_embedding(node.get_content(metadata_mode="all"))
        node.embedding = node_embedding

    return nodes
