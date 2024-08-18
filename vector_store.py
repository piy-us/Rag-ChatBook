from typing import List, Any, Dict
from llama_index.core.vector_stores.types import BasePydanticVectorStore
from llama_index.core.schema import BaseNode
from llama_index.core.bridge.pydantic import Field
from llama_index.core.vector_stores import MetadataFilters
import os
from llama_index.core.vector_stores.types import BasePydanticVectorStore
from llama_index.core.vector_stores import (
    VectorStoreQuery,
    VectorStoreQueryResult,
)
from typing import List, Any, Optional, Dict
from llama_index.core.schema import TextNode, BaseNode
import os
from llama_index.core.bridge.pydantic import Field
from typing import Tuple
import numpy as np
from typing import cast
from llama_index.core.schema import BaseNode
from typing import List

class BaseVectorStore(BasePydanticVectorStore):
    stores_text: bool = True

    def get(self, text_id: str) -> List[float]:
        pass

    def add(self, nodes: List[BaseNode]) -> List[str]:
        pass

    def delete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        pass

    def query(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        pass

    def persist(self, persist_path, fs=None) -> None:
        pass

class VectorStore2(BaseVectorStore):
    stores_text: bool = True
    node_dict: Dict[str, BaseNode] = Field(default_factory=dict)

    def client(self):
        return None

    def get(self, text_id: str) -> List[float]:
        return self.node_dict[text_id]

    def add(self, nodes: List[BaseNode]) -> List[str]:
        for node in nodes:
            self.node_dict[node.node_id] = node

    def delete(self, node_id: str, **delete_kwargs: Any) -> None:
        del self.node_dict[node_id]

def get_top_k_embeddings(query_embedding, doc_embeddings, doc_ids, similarity_top_k=5):
    qembed_np = np.array(query_embedding)
    dembed_np = np.array(doc_embeddings)
    dproduct_arr = np.dot(dembed_np, qembed_np)
    norm_arr = np.linalg.norm(qembed_np) * np.linalg.norm(dembed_np, axis=1, keepdims=False)
    cos_sim_arr = dproduct_arr / norm_arr
    tups = [(cos_sim_arr[i], doc_ids[i]) for i in range(len(doc_ids))]
    sorted_tups = sorted(tups, key=lambda t: t[0], reverse=True)
    sorted_tups = sorted_tups[:similarity_top_k]
    result_similarities = [s for s, _ in sorted_tups]
    result_ids = [n for _, n in sorted_tups]
    return result_similarities, result_ids

class VectorStore3A(VectorStore2):
    def query(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        query_embedding = embed_model.get_text_embedding(query.query_str)
        doc_embeddings = [n.embedding for n in self.node_dict.values()]
        doc_ids = [n.node_id for n in self.node_dict.values()]
        similarities, node_ids = get_top_k_embeddings(query_embedding, doc_embeddings, doc_ids, query.similarity_top_k)
        result_nodes = [self.node_dict[node_id] for node_id in node_ids]
        return VectorStoreQueryResult(nodes=result_nodes, similarities=similarities, ids=node_ids)

def filter_nodes(nodes: List[BaseNode], filters: MetadataFilters) -> List[BaseNode]:
    filtered_nodes = []
    for node in nodes:
        matches = True
        for f in filters.filters:
            if f.key not in node.metadata:
                matches = False
                continue
            try:
                filter_value = int(f.value)
                node_value = int(node.metadata[f.key])
                if not (1 <= node_value <= filter_value):
                    matches = False
                    continue
            except ValueError:
                matches = False
                continue
        if matches:
            filtered_nodes.append(node)
    return filtered_nodes

def dense_search(query: VectorStoreQuery, nodes: List[BaseNode]):
    query_embedding = cast(List[float], query.query_embedding)
    doc_embeddings = [n.embedding for n in nodes]
    doc_ids = [n.node_id for n in nodes]
    return get_top_k_embeddings(query_embedding, doc_embeddings, doc_ids, query.similarity_top_k)

class VectorStore3B(VectorStore2):
    def query(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        nodes = self.node_dict.values()
        if query.filters is not None:
            nodes = filter_nodes(nodes, query.filters)
        if len(nodes) == 0:
            result_nodes = []
            similarities = []
            node_ids = []
        else:
            similarities, node_ids = dense_search(query, nodes)
            result_nodes = [self.node_dict[node_id] for node_id in node_ids]
        return VectorStoreQueryResult(nodes=result_nodes, similarities=similarities, ids=node_ids)
