"""
exceptions.py 关于异常的使用场景
"""

# 使用示例：
"""
try:
    # 可能失败的操作
    result = milvus_client.insert(data)
except Exception as e:
    raise MilvusError(
        message="向量写入失败",
        node_name="import_milvus",
        cause=e
    )
"""

# 输出效果：
"""
MilvusError: [import_milvus] 向量写入失败 (原因: ConnectionError: ...)
"""