from vector_store import VectorStore3B
from llama_index.core.vector_stores import MetadataFilters
from llama_index.core import VectorStoreIndex
temp=0
filters=''
index=''
def build_vector_store(nodes):
    vector_store = VectorStore3B()
    vector_store.add(nodes)
    return vector_store

def build_index(vector_store,page_number):
    global temp
    global filters
    global index
    if page_number>temp:
        temp=page_number
        filters = MetadataFilters.from_dict({"source": f"{temp}"})
        index = VectorStoreIndex.from_vector_store(vector_store)
        return index
    else:
        return index

def query_index(index, query_str):
    query = VectorStoreQuery(query_str=query_str, similarity_top_k=5)
    result = index.query(query)
    return result
