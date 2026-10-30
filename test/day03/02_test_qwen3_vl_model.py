import os

from dotenv import load_dotenv
from openai import OpenAI
import base64

load_dotenv()

# 初始化客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url = "https://ws-wfidrx802w57h4di.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 图片转 Base64
with open("D:/download/google-download/云朵面包店.png", "rb") as f:
    base64_image = base64.b64encode(f.read()).decode("utf-8")
    # print(base64_image)
# 调用 VLM
response = client.chat.completions.create(
    model="qwen3.8-max",  # 视觉模型
    # model="qwen3-vl-plus", #视觉模型
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",        # 告诉 API：这是一段文字
                    "text": "请描述这张图片的内容"
                },
                {
                    "type": "image_url",   # 告诉 API：这是一张图片
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    max_tokens=100
)

summary = response
print(summary)

