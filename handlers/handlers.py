# API 处理器
from flask import jsonify, Blueprint, request
import logging

from models.models import ApiResponse
# 从 all_service 导入 AllService 替代原来的 HotSearchService
from services.all_service import AllService

# 创建蓝图
api_bp = Blueprint('api', __name__)
# 使用 AllService 替代 HotSearchService
hot_search_service = AllService()
logger = logging.getLogger(__name__)

@api_bp.route('/hot-search', methods=['GET'])
def get_hot_search():
    """获取热搜接口"""
    try:
        # 使用 get_all_hot_search 方法获取所有平台的热搜
        all_hot_search = hot_search_service.get_all_hot_search()
        response = ApiResponse(data=all_hot_search)
        return jsonify(response.to_dict())
    except Exception as e:
        logger.error(f"获取热搜失败: {str(e)}")
        error_response = ApiResponse(code=500, message=f"服务器错误: {str(e)}", data=None)
        return jsonify(error_response.to_dict()), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({"status": "ok"}) 