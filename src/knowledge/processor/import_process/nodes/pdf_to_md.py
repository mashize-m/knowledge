"""
导入流程的pdf转md节点：

"""
from knowledge.processor.import_process.base import BaseNode
from knowledge.processor.import_process.state import ImportGraphState


class PdfToMdNode(BaseNode):
    """ pdf转md节点 """

    name: str = "pdf_to_md_node"

    def process(self, state: ImportGraphState) -> ImportGraphState| dict:
        """pdf转md节点处理流程"""
        return state