import json

from langgraph.constants import END
from langgraph.graph.state import CompiledStateGraph, StateGraph

from knowledge.processor.import_process.base import setup_logging
from knowledge.processor.import_process.nodes.bge_embedding import BgeEmbeddingChunksNode
from knowledge.processor.import_process.nodes.document_split import DocumentSplitNode
from knowledge.processor.import_process.nodes.entry import EntryNode
from knowledge.processor.import_process.nodes.import_milvus import ImportMilvusNode
from knowledge.processor.import_process.nodes.item_name_recognition import ItemNameRecognitionNode
from knowledge.processor.import_process.nodes.md_img import MarkDownImageNode
from knowledge.processor.import_process.nodes.pdf_to_md import PdfToMdNode
from knowledge.processor.import_process.state import ImportGraphState, create_default_state


def load_file_route(state: ImportGraphState):
    """ 根据上传的文件，判断不同的节点 """
    if state.get('is_md_read_enabled'):
        return "md_img_node"
    if state.get('is_pdf_read_enabled'):
        return "pdf_to_md_node"
    return "END"  # 安全降级

def create_import_graph() -> CompiledStateGraph:
    """
        创建导入流程图

        Returns:
            编译后的 StateGraph 实例

        流程结构:
            entry_node
                  │
                  ├── (PDF) ──> pdf_to_md_node ──┐
                  │                              │
                  └── (MD) ─────────────────────>├──> md_img_node
                                                  │
                                                  v
                                          document_split_node
                                                  │
                                                  v
                                          item_name_rec_node
                                                  │
                                                  v
                                            bge_embedding_node
                                                  │
                                                  v
                                            import_milvus_node
                                                  │
                                                  v
                                                 END
    """

    # 创建状态。ImportGraphState

    # 创建节点。 单独文件

    # 创建graph实例
    import_graph = StateGraph(ImportGraphState)

    # 添加节点
    nodes = {
        "entry_node": EntryNode(),
        "pdf_to_md_node": PdfToMdNode(),
        "md_img_node": MarkDownImageNode(),
        "document_split_node": DocumentSplitNode(),
        "item_name_rec_node": ItemNameRecognitionNode(),
        "bge_embedding_node": BgeEmbeddingChunksNode(),
        "import_milvus_node": ImportMilvusNode(),
    }

    for key, value in nodes.items():
        import_graph.add_node(key, value)

    # 添加边
    import_graph.set_entry_point("entry_node") # 设置入口节点，
    import_graph.add_conditional_edges(
        "entry_node",
        load_file_route,
        {
            "pdf_to_md_node": "pdf_to_md_node",
            "md_img_node": "md_img_node",
            "END":END
        }
    )
    import_graph.add_edge("pdf_to_md_node", "md_img_node")
    import_graph.add_edge("md_img_node", "document_split_node")
    import_graph.add_edge("document_split_node", "item_name_rec_node")
    import_graph.add_edge("item_name_rec_node", "bge_embedding_node")
    import_graph.add_edge("bge_embedding_node", "import_milvus_node")
    import_graph.add_edge("import_milvus_node", END)


    # 编译实例
    compiled_graph = import_graph.compile()

    return compiled_graph

    # 运行实例。invoke 或者 stream

# 创建全局图实例
compiled_graph = create_import_graph()

def run_import_graph(import_file_path: str, file_dir: str):

    # 创建状态 state
    state = {
        "import_file_path": import_file_path,
        "file_dir": file_dir
    }
    init_state = create_default_state(**state)

    # 运行实例，流式
    final_state = None
    for event in compiled_graph.stream(init_state):
        for node_name, state in event.items():
            final_state = state

    return final_state


if __name__ == '__main__':
    setup_logging()

    import_file_path = r"D:\development\AIAgent\shopkeeper_brain\knowledge\data\test_data\万用表的使用.pdf"
    file_dir = r"D:\development\AIAgent\shopkeeper_brain\knowledge\data\test_data"

    # 1. 测试编排流程
    final_state = run_import_graph(
        import_file_path=import_file_path,
        file_dir=file_dir
    )
    #
    print("结果输出：", json.dumps(final_state, indent=2, ensure_ascii=False))

    # 2. 打印图结构（ASCII 可视化）
    print("-" * 50)
    print("图结构:")
    compiled_graph.get_graph().print_ascii()
