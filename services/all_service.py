# 聚合服务模块
import logging
from typing import Dict, List, Any
import concurrent.futures
from threading import Lock

from models.models import HotSearchItem
from services.platform_services import (
    BaiduService, BilibiliService, WeiboHotService, ZhihuService,
    Search360Service, AcfunService, CSDNService, DongqiudiService,
    DoubanService, DouyinService
    # 导入其他平台服务...
)

class AllService:
    """聚合所有平台热搜的服务"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.services = {
            "百度": BaiduService(),
            "哔哩哔哩": BilibiliService(),
            "微博": WeiboHotService(),
            "知乎": ZhihuService(),
            "360搜索": Search360Service(),
            "AcFun": AcfunService(),
            "CSDN": CSDNService(),
            "懂球帝": DongqiudiService(),
            "豆瓣": DoubanService(),
            "抖音": DouyinService(),
            # 添加其他平台服务...
        }
    
    def get_all_hot_search(self) -> Dict[str, List[Dict[str, Any]]]:
        """获取所有平台的热搜"""
        result = {}
        mutex = Lock()
        
        def fetch_platform_data(platform_name, service):
            try:
                hot_items = service.get_hot_search()
                if hot_items:
                    with mutex:
                        result[platform_name] = [item.to_dict() for item in hot_items]
            except Exception as e:
                self.logger.error(f"获取 {platform_name} 热搜失败: {str(e)}")
        
        # 使用线程池并发获取各平台数据
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(fetch_platform_data, name, service): name 
                for name, service in self.services.items()
            }
            concurrent.futures.wait(futures)
        
        self.logger.info(f"成功获取 {len(result)} 个平台的热搜数据")
        return result 