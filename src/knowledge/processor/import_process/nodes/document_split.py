"""
导入流程的 文档切片 节点：

"""
from knowledge.processor.import_process.base import BaseNode
from knowledge.processor.import_process.state import ImportGraphState


class DocumentSplitNode(BaseNode):
    """ 文档切片 节点 """

    name: str = "document_split_node"

    def process(self, state: ImportGraphState) -> ImportGraphState| dict:
        """ 节点处理流程"""
        return state