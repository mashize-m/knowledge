from minio import Minio

# 初始化服务端
client = Minio(
    "192.168.1.10:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False  # 是否使用https
)

# 如果minio中 不存在 mybucket 这个桶。就创建
if not client.bucket_exists("mybucket"):
    client.make_bucket("mybucket")

# 上传文件
client.fput_object(
    bucket_name="mybucket",
    object_name="images/1.答案生成.jpg",  # Object名称含路径
    file_path="D:/development/AIAgent/11_尚硅谷AI全能开发技术之项目【掌柜智库】/1.课件/images/1.答案生成.jpg",  # 上传的本地文件路径
    content_type="image/jpeg"  # MIME类型
)

# 上传后访问地址
url = f"http://192.168.1.10:9000/mybucket/images/p1.jpg"
print(url)


#  Access Denied.  默认创建桶是private   需要 修改为public