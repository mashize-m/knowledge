"""
导入流程的 向量化 节点：

"""
from knowledge.processor.import_process.base import BaseNode
from knowledge.processor.import_process.state import ImportGraphState


class BgeEmbeddingChunksNode(BaseNode):
    """ 向量化 节点 """

    name: str = "bge_embedding_node"

    def process(self, state: ImportGraphState) -> ImportGraphState| dict:
        """ 节点处理流程"""
        return state