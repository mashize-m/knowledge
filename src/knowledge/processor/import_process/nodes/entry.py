"""
导入流程的入口节点：
    判断文件是 pdf还是 md文档。

"""
from knowledge.processor.import_process.base import BaseNode
from knowledge.processor.import_process.state import ImportGraphState


class EntryNode(BaseNode):
    """ 入口节点 """

    name: str = "entry_node"

    def process(self, state: ImportGraphState) -> ImportGraphState| dict:
        """入口节点处理流程"""
        return state