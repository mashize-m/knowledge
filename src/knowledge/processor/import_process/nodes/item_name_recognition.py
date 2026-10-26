"""
导入流程的 商品标题处理 节点：

"""
from knowledge.processor.import_process.base import BaseNode
from knowledge.processor.import_process.state import ImportGraphState


class ItemNameRecognitionNode(BaseNode):
    """ 商品标题处理 节点 """

    name: str = "item_name_rec_node"

    def process(self, state: ImportGraphState) -> ImportGraphState| dict:
        """ 节点处理流程"""
        return state