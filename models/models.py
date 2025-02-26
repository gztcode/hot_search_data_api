# 数据模型
from datetime import datetime
from typing import List, Optional, Dict, Any

class HotSearchItem:
    """热搜项目模型"""
    
    def __init__(self, 
                 id: int = 0,
                 title: str = "",
                 url: str = "",
                 hot_value: int = 0,
                 platform: str = "",
                 rank: int = 0,
                 created_at: datetime = None):
        self.id = id
        self.title = title
        self.url = url
        self.hot_value = hot_value
        self.platform = platform
        self.rank = rank
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """将对象转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "hot_value": self.hot_value,
            "platform": self.platform,
            "rank": self.rank,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HotSearchItem':
        """从字典创建对象"""
        created_at = data.get("created_at")
        if created_at and isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        return cls(
            id=data.get("id", 0),
            title=data.get("title", ""),
            url=data.get("url", ""),
            hot_value=data.get("hot_value", 0),
            platform=data.get("platform", ""),
            rank=data.get("rank", 0),
            created_at=created_at
        )

class ApiResponse:
    """API 响应模型"""
    
    def __init__(self, 
                 code: int = 200,
                 message: str = "success",
                 data: Any = None):
        self.code = code
        self.message = message
        self.data = data
    
    def to_dict(self) -> Dict[str, Any]:
        """将对象转换为字典"""
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        } 