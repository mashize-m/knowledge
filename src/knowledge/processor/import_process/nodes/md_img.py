"""
导入流程的 md的img处理 节点：

"""
from knowledge.processor.import_process.base import BaseNode
from knowledge.processor.import_process.state import ImportGraphState


class MarkDownImageNode(BaseNode):
    """ md的img处理节点 """

    name: str = "md_img_node"

    def process(self, state: ImportGraphState) -> ImportGraphState| dict:
        """ 节点处理流程"""
        return state