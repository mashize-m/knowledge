2026/10/26 13:20:00

- [ ] .env环境中，服务器环境的地址未更改为本地电脑的IP
- [ ] ai_models里的四个模型都没有，需要看后面课程中，有没有给下载地址
- [ ] LLM API 还没有配置。
- [ ] test/01_**.py，连接服务器环境测试文件，这个还没有测试。

- [ ] processor/import_process/config.py，这个文件是个配置文件，为什么有的是直接赋值的，例如：max_content_length: int = 2000，而有的却是通过field(default_factory=lambda: ...)方式赋值呢？这2种方式有什么区别？应用场景分别是什么？
- [ ] config.py文件封装的是.env里的信息。我的