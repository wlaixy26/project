from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    """
    配置中心：所有可调参数放这里，支持通过环境变量覆盖。
    这样工程化后更容易部署到不同环境(dev/test/prod)。
    """

    app_name: str = "local-rag-service"
    env: str = "dev"
    debug: bool = True

    # 数据文件/索引相关（骨架示例；如果你做“按文件路径建索引”，可以放到rag_service里）
    data_path: str = r"D:\python\Scripts\test.pdf"
    index_root: str = "indexes"

    # 模型配置
    embed_model: str = "paraphrase-multilingual-MiniLM-L12-v2"
    llm_model: str = "Qwen/Qwen2-1.5B-Instruct"

    # 检索配置
    top_k: int = 8

    # 启用 .env（可选）
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )