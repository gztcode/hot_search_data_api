# 配置模块
import os

class Config:
    """应用配置类"""
    
    def __init__(self):
        # 服务器配置
        self.server_port = os.getenv("SERVER_PORT", "8080")
        
        # API 配置
        self.api_timeout = int(os.getenv("API_TIMEOUT", "10"))
        
        # 数据库配置
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_user = os.getenv("DB_USER", "postgres")
        self.db_password = os.getenv("DB_PASSWORD", "password")
        self.db_name = os.getenv("DB_NAME", "hotsearch")

# 创建全局配置实例
config = Config() 