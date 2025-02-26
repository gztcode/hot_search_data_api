# 主程序入口
from flask import Flask
import logging
import os

from config.config import config
from handlers.handlers import api_bp
from handlers.all_handlers import all_bp

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """创建 Flask 应用"""
    app = Flask(__name__)
    
    # 注册蓝图
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(all_bp, url_prefix='/')
    
    # 打印所有注册的路由
    print("注册的路由:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")
    
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", config.server_port))
    
    logger.info(f"服务启动在端口 {port}")
    app.run(host="0.0.0.0", port=port, debug=False) 