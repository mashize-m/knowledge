# 掌柜智库项目


## 环境准备

```powershell
# 更新依赖
uv sync 

# 复制 `.env.example` 为 `.env`，填入你的 API Key。

# 设置python解释器路径

# 拉取项目时执行下面命令，激活虚拟环境。激活后终端路径前会有 （knowledge）显示
.\.venv\Scripts\Activate.ps1

# 设置src为根目录
```


## 切换python环境

```powershell
# 检查 pyproject.toml最低版本要求，是否满足新的python版本
requires-python = ">=3.12.15"

# 第 1 步：锁定新的 Python 版本
# 预期结果：终端显示类似 Updated .python-version from 3.12.15 -> 3.10.22 的提示。项目根目录下的 .python-version 文件内容已变为 3.10.22。此命令确保了后续所有 uv 操作都优先使用这个版本
uv python pin 3.10.22

# 修改锁定版本
uv lock

# 第 2 步：删除旧的虚拟环境
# 预期结果：项目根目录下的 .venv 文件夹已被删除。
Remove-Item -Recurse -Force .venv

# 第 3 步：根据锁定的版本重建环境与依赖
# 预期结果：终端会显示 Using CPython 3.10.22、Creating virtual environment at: .venv，并开始根据 uv.lock 重新安装所有依赖包。完成后，一个指向 Python 3.10.22 的新 .venv 就绪了。
uv sync

# 第 4 步：更新 PyCharm 的项目解释器

# 第 5 步：激活虚拟环境
# 预期结果：激活后终端路径前会有 （knowledge）显示
.\.venv\Scripts\Activate.ps1

# 第 6 步：验证命令行版本
# 预期结果：显示正确的python版本号
python --version
```


## 项目目录结构
```
knowledge/                                      # 项目根目录
├── data/                                       # 本地数据（知识库、PDF、txt）
│   └── .gitkeep                                # 占位文件，保持 data 目录纳入版本控制
├── notes/                                      # 项目笔记
│   └── 01_环境搭建.md                          
├── scratch/                                    # 临时验证性文件
│   ├── .gitkeep                                
│   └── 01_test_connections.py                  # 临时连接测试脚本
├── src/                                        # 源代码根目录
│   └── knowledge/                              # 知识库业务包
│       ├── processor/                          # 业务处理流程（LangGraph）
│       │   └── import_process/                 # 导入流程
│       │       ├── nodes/                      # 处理节点
│       │       │   ├── bge_embedding.py        # 向量嵌入
│       │       │   ├── document_split.py       # 文档切分
│       │       │   ├── entry.py                # 入口节点
│       │       │   ├── import_milvus.py        # Milvus 存储
│       │       │   ├── item_name_recognition.py # 商品识别
│       │       │   ├── md_img.py               # 图片处理
│       │       │   └── pdf_to_md.py            # PDF 转 MD
│       │       ├── base.py                     # 父节点模板代码
│       │       ├── config.py                   # 导入流程配置
│       │       ├── exceptions.py               # 导入流程异常类
│       │       ├── main_graph.py               # 导入流程图定义
│       │       └── state.py                    # 状态类型定义
│       └── utils/                              # 工具函数库
│           ├── client/                         # 客户端封装
│           │   ├── ai_clients.py               # LLM客户端、BGE-M3模型、Reranker模型
│           │   ├── base.py                     # 客户端管理器基类，双重检查锁模板方法
│           │   └── storage_clients.py          # MinIO、Milvus、Mongo客户端
│           ├── embedding_util.py               # 向量嵌入工具
│           ├── markdown_util.py                # Markdown 处理工具
│           ├── milvus_util.py                  # Milvus 向量库操作
│           ├── mongo_history_util.py           # MongoDB 历史记录
│           ├── sse_util.py                     # SSE 流式推送
│           └── task_util.py                    # 任务状态管理
├── .env                                        # 环境变量配置
├── .gitignore                                  # Git 忽略规则
├── README.md                                   # 项目说明文档
├── TODO.md                                     # 待办事项
├── pyproject.toml                              # Python 项目配置
└── uv.lock                                     # uv 依赖锁定文件
```

