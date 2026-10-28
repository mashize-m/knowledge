"""
导入流程的pdf转md节点：

"""
import json
import subprocess
import time
from pathlib import Path
from typing import Tuple

from knowledge.processor.import_process.base import BaseNode, setup_logging
from knowledge.processor.import_process.exceptions import PdfConversionError, ValidationError, FileProcessingError
from knowledge.processor.import_process.state import ImportGraphState


class PdfToMdNode(BaseNode):
    """
    PDF 转 Markdown 节点

    调用 MinerU 命令行工具将 PDF 转换为 Markdown，
    支持实时输出转换日志。
    """

    name: str = "pdf_to_md_node"

    def process(self, state: ImportGraphState) -> ImportGraphState| dict:
        """pdf转md节点处理流程"""

        # 1.数据校验
        import_file_path_obj, file_dir_obj = self._validate_state_inputs_path(state)

        # 2.执行mineru 转换
        code = self._execute_mineru(import_file_path_obj, file_dir_obj)
        if code != 0:
            raise PdfConversionError("PDF转换Markdown失败", self.name)

        # 3.获取md路径
        md_path_obj = self._get_md_path(import_file_path_obj, file_dir_obj)

        # 4.更新state
        state['md_path'] = str(md_path_obj)

        # 5.返回
        return state

    def _validate_state_inputs_path(self, state) -> Tuple[Path, Path]:
        self.log_step("step1", "对状态的路径输入参数做校验")
        import_file_path = state.get("import_file_path", "")

        if not import_file_path:
            raise ValidationError("import_file_path参数不存在", self.name)

        import_file_path_obj = Path(import_file_path)
        if not import_file_path_obj.exists():  # 是否为有效路径
            raise FileProcessingError("PDF文件不存在", self.name)

        file_dir = state.get("file_dir", "")
        if not file_dir:
            file_dir = import_file_path_obj.parent  # 降级处理

        file_dir_obj = Path(file_dir)
        self.logger.info(f"上传文件的路径:{import_file_path}")
        self.logger.info(f"输出的目录:{file_dir}")
        return import_file_path_obj, file_dir_obj

    def _execute_mineru(self, import_file_path_obj, file_dir_obj) -> int:
        """利用mineru命令，将pdf转换为md"""

        # mineru -p input.pdf -o output_dir/ --source local  --backend  pipeline
        # -p 要解析的文件
        # -o 要输出的目录
        # --source local 本地模型
        # --backend 后台运行
        # pipeline 用原始推理模型，完成PDF解析，无需使用GPU

        self.log_step("step2", "执行MinerU解析PDF")

        process_start_time = time.time()

        # 这里没有 --source local ，是因为走的 系统的环境变量。
        proc = subprocess.Popen(
            args=["mineru", "-p", str(import_file_path_obj), "-o", str(file_dir_obj), "--backend", "pipeline"],
            stdout=subprocess.PIPE,  # 捕获标准输出
            stderr=subprocess.STDOUT,  # 合并错误到标准输出
            text=True,
            encoding="utf-8",
            errors="replace",  # 遇到乱码时替换
            bufsize=1  # 行缓冲，实时输出
        )

        for line in proc.stdout:
            self.logger.info(f"执行MinerU产生的日志：{line}")

        return_code = proc.wait()

        process_end_time = time.time()
        if return_code == 0:
            self.logger.info(
                f"MinerU成功解析PDF文件：{import_file_path_obj.name} "
                f"耗时:{process_end_time - process_start_time:.2f}s"
            )
        else:
            self.logger.error(f"MinerU解析PDF文件：{import_file_path_obj.name}失败")

        return return_code

    def _get_md_path(self, import_file_path_obj, file_dir_obj) -> Path:
        """获取pdf转换为md之后完整路径"""
        return file_dir_obj / import_file_path_obj.stem / "auto" / (import_file_path_obj.stem + ".md")

#测试
if __name__ == "__main__":
    setup_logging()

    input_state = {
        "import_file_path": r"E:/msz/AIAgent/shopkeeper_brain/knowledge/data/doc/万用表RS-12的使用.pdf",  # 导入文件路径（原始输入）
        "file_dir": r"E:/msz/AIAgent/shopkeeper_brain/knowledge/data/output/",  # 导入(出)文件目录
    }

    current_node = PdfToMdNode()

    node_state =  current_node(input_state)

    print(json.dumps(node_state,ensure_ascii=False,indent=4))