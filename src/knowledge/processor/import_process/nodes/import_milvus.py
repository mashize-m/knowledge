"""
导入流程的 存储 节点：

"""
from knowledge.processor.import_process.base import BaseNode
from knowledge.processor.import_process.state import ImportGraphState


class ImportMilvusNode(BaseNode):
    """ 存储 节点 """

    name: str = "import_milvus_node"

    def process(self, state: ImportGraphState) -> ImportGraphState| dict:
        """ 节点处理流程"""
        return state