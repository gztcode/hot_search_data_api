# 平台服务模块
import requests
import re
import logging
import json
import time
from typing import List, Dict, Any
from datetime import datetime
import math

from models.models import HotSearchItem
from utils.utils import extract_matches, strip_html

class PlatformService:
    """平台热搜服务基类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    
    def extract_matches(self, text: str, pattern: str) -> List[List[str]]:
        """提取正则表达式匹配结果"""
        return extract_matches(text, pattern)
    
    def format_hot_value(self, value: Any) -> int:
        """格式化热度值为整数，保持精度"""
        try:
            if isinstance(value, (int, float)):
                return int(value)
            
            if not value:
                return 0
                
            # 处理字符串类型
            value = str(value).strip()
            
            # 知乎特殊处理
            if "万热度" in value:
                # 提取数字部分（包括小数点）
                num_str = ''.join(c for c in value.split('万热度')[0].strip() if c.isdigit() or c == '.')
                try:
                    # 将字符串转换为浮点数并乘以10000
                    return int(float(num_str) * 10000)
                except:
                    return 0
            
            # 其他情况的处理保持不变
            value = ''.join(c for c in value if c.isdigit() or c == '.')
            
            if '万' in value or 'w' in value.lower():
                value = float(value.replace('万', '').replace('w', '').replace('W', '')) * 10000
            elif '亿' in value:
                value = float(value.replace('亿', '')) * 100000000
                
            return int(float(value))
        except:
            return 0

class BaiduService(PlatformService):
    """百度热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取百度热搜"""
        try:
            url = "https://top.baidu.com/board?tab=realtime"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # 提取标题和热度
            title_pattern = r'<div\sclass="c-single-text-ellipsis">(.*?)</div>'
            hot_pattern = r'<div\sclass="hot-index_1Bl1a">(.*?)</div>'
            
            titles = self.extract_matches(response.text, title_pattern)
            hot_values = self.extract_matches(response.text, hot_pattern)
            
            hot_items = []
            for i, (title, hot_value) in enumerate(zip(titles, hot_values)):
                title = title.strip() if isinstance(title, str) else title[0].strip()
                hot_value = hot_value.strip() if isinstance(hot_value, str) else hot_value[0].strip()
                
                # 移除热度值中的非数字字符
                hot_value = ''.join(filter(str.isdigit, hot_value))
                
                hot_item = HotSearchItem(
                    id=i + 1,  # 使用索引作为ID
                    title=title,
                    url=f"https://www.baidu.com/s?wd={title}",
                    hot_value=int(hot_value) if hot_value else 0,
                    platform="baidu",
                    rank=i + 1
                )
                hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取百度热搜失败: {str(e)}")
            return []

class BilibiliService(PlatformService):
    """哔哩哔哩热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取哔哩哔哩热搜"""
        try:
            # 使用新的 API 地址
            url = "https://api.bilibili.com/x/web-interface/search/square?limit=50"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://www.bilibili.com/",
                "Origin": "https://www.bilibili.com"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data and "trending" in data["data"]:
                for i, item in enumerate(data["data"]["trending"]["list"]):
                    # 提取关键字和热度值
                    keyword = item.get("keyword", "")
                    show_name = item.get("show_name", keyword)
                    hot_value = item.get("heat_score", 0)  # 修改这里，使用 heat_score
                    
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=show_name,
                        url=f"https://search.bilibili.com/all?keyword={keyword}",
                        hot_value=self.format_hot_value(hot_value),  # 格式化热度值
                        platform="bilibili",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            # 如果上面的 API 失败，尝试备用 API
            if not hot_items:
                url = "https://api.bilibili.com/x/web-interface/popular?ps=50&pn=1"
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                if "data" in data and "list" in data["data"]:
                    for i, item in enumerate(data["data"]["list"]):
                        hot_item = HotSearchItem(
                            id=i + 1,
                            title=item.get("title", ""),
                            url=f"https://www.bilibili.com/video/{item.get('bvid', '')}",
                            hot_value=self.format_hot_value(item.get("heat", 0)),  # 备用 API 使用 heat 字段
                            platform="bilibili",
                            rank=i + 1
                        )
                        hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取哔哩哔哩热搜失败: {str(e)}")
            return []

class WeiboHotService(PlatformService):
    """微博热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取微博热搜"""
        try:
            url = "https://weibo.com/ajax/side/hotSearch"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data and "realtime" in data["data"]:
                for i, item in enumerate(data["data"]["realtime"]):
                    hot_item = HotSearchItem(
                        id=i + 1,  # 添加 id
                        title=item.get("word", ""),
                        url=f"https://s.weibo.com/weibo?q={item.get('word', '')}",
                        hot_value=int(item.get("num", 0)),
                        platform="weibo",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取微博热搜失败: {str(e)}")
            return []

class ZhihuService(PlatformService):
    """知乎热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取知乎热搜"""
        try:
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
            headers = {"User-Agent": self.user_agent}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data:
                for i, item in enumerate(data["data"]):
                    if "target" in item:
                        # 获取热度值并格式化
                        hot_value = item.get("detail_text", "0")
                        # 直接使用原始热度值字符串进行格式化
                        formatted_hot_value = self.format_hot_value(hot_value)
                        
                        hot_item = HotSearchItem(
                            id=i + 1,
                            title=item["target"].get("title", ""),
                            url=f"https://www.zhihu.com/question/{item['target'].get('id', '')}",
                            hot_value=formatted_hot_value,
                            platform="zhihu",
                            rank=i + 1
                        )
                        hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取知乎热搜失败: {str(e)}")
            return []

class Search360Service(PlatformService):
    """360搜索热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取360搜索热搜"""
        try:
            # 参考 Go 实现，使用正确的 API
            url = "https://trends.so.com/top/realtime"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://trends.so.com/",
                "Accept": "application/json"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data and "result" in data["data"]:
                for i, item in enumerate(data["data"]["result"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("query", ""),
                        url=f"https://www.so.com/s?q={item.get('query', '')}",
                        hot_value=self.format_hot_value(item.get("heat", 0)),
                        platform="360search",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取360搜索热搜失败: {str(e)}")
            return []

class AcfunService(PlatformService):
    """AcFun热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取AcFun热搜"""
        try:
            url = "https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=&subChannelId=&rankLimit=30&rankPeriod=DAY"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://www.acfun.cn/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "rankList" in data:
                for i, item in enumerate(data["rankList"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("contentTitle", ""),
                        url=item.get("shareUrl", ""),
                        hot_value=self.format_hot_value(item.get("viewCount", 0)),  # 添加热度值
                        platform="acfun",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取AcFun热搜失败: {str(e)}")
            return []

# 添加更多平台服务...
class CSDNService(PlatformService):
    """CSDN热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取CSDN热搜"""
        try:
            url = "https://blog.csdn.net/phoenix/web/blog/hot-rank?page=0&pageSize=25&type=1"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://blog.csdn.net/rank/list"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data:
                for i, item in enumerate(data["data"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("articleTitle", ""),
                        url=item.get("articleDetailUrl", ""),
                        hot_value=self.format_hot_value(item.get("hotRankScore", 0)),
                        platform="csdn",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取CSDN热搜失败: {str(e)}")
            return []

class DongqiudiService(PlatformService):
    """懂球帝热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取懂球帝热搜"""
        try:
            url = "https://api.dongqiudi.com/v3/archive/app/web/recommend/new"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://www.dongqiudi.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data and "articles" in data["data"]:
                for i, item in enumerate(data["data"]["articles"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("title", ""),
                        url=item.get("share", {}).get("url", ""),
                        hot_value=self.format_hot_value(item.get("read_count", 0)),  # 添加热度值
                        platform="dongqiudi",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取懂球帝热搜失败: {str(e)}")
            return []

# 继续添加其他平台服务...
class DoubanService(PlatformService):
    """豆瓣热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取豆瓣热搜"""
        try:
            url = "https://movie.douban.com/j/search_subjects?type=movie&tag=热门&page_limit=50&page_start=0"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://movie.douban.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "subjects" in data:
                for i, item in enumerate(data["subjects"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        hot_value=self.format_hot_value(item.get("rate", "0")),
                        platform="douban",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取豆瓣热搜失败: {str(e)}")
            return []

class DouyinService(PlatformService):
    """抖音热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取抖音热搜"""
        try:
            url = "https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "word_list" in data:
                for i, item in enumerate(data["word_list"]):
                    hot_value = item.get("hot_value", 0)
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("word", ""),
                        url=f"https://www.douyin.com/search/{item.get('word', '')}",
                        hot_value=self.format_hot_value(hot_value),
                        platform="douyin",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取抖音热搜失败: {str(e)}")
            return []

# 继续添加其他平台...
class GithubService(PlatformService):
    """GitHub热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取GitHub热搜"""
        try:
            url = "https://github.com/trending"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            pattern = r'<h2 class="h3 lh-condensed">\s*<a\s+href="([^"]+)"[^>]*>\s*<span[^>]*>([^<]+)</span>\s*<span[^>]*>([^<]+)</span>\s*</a>\s*</h2>\s*<p[^>]*>\s*([^<]*)'
            matched = self.extract_matches(response.text, pattern)
            
            hot_items = []
            for i, item in enumerate(matched):
                title = (item[1] + item[2]).strip().replace(" ", "")
                hot_item = HotSearchItem(
                    id=i + 1,  # 添加 id
                    title=title,
                    url=f"https://github.com{item[0]}",
                    desc=item[3].strip(),
                    platform="github",
                    rank=i + 1
                )
                hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取GitHub热搜失败: {str(e)}")
            return []

class GuojiadiliService(PlatformService):
    """国家地理热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取国家地理热搜"""
        try:
            url = "http://www.dili360.com/"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "http://www.dili360.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 参考 Go 代码中的正则表达式
            pattern = r'<div class="pic">\s*<a href="([^"]+)"[^>]*>\s*<img[^>]*>\s*</a>\s*</div>\s*<div class="text">\s*<h3>\s*<a[^>]*>([^<]+)</a>\s*</h3>'
            matched = self.extract_matches(response.text, pattern)
            
            hot_items = []
            for i, item in enumerate(matched):
                url = item[0]
                if not url.startswith('http'):
                    url = f"http://www.dili360.com{url}"
                
                hot_item = HotSearchItem(
                    id=i + 1,
                    title=item[1].strip(),
                    url=url,
                    platform="guojiadili",
                    rank=i + 1
                )
                hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取国家地理热搜失败: {str(e)}")
            return []

class HistoryService(PlatformService):
    """历史上的今天服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取历史上的今天"""
        try:
            # 获取当前日期
            today = datetime.now()
            month = today.month
            day = today.day
            
            url = f"https://baike.baidu.com/cms/home/eventsOnHistory/{month:02d}.json"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://baike.baidu.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json().get(f"{month:02d}")
            hot_items = []
            
            date_key = f"{month:02d}{day:02d}"
            if date_key in data:
                for i, item in enumerate(data[date_key]):
                    year = item.get("year", "")
                    title = strip_html(item.get("title", ""))
                    # 将描述信息合并到标题中
                    full_title = f"{year}年：{title}"
                    
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=full_title,
                        url=item.get("link", ""),
                        platform="history",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取历史上的今天失败: {str(e)}")
            return []

class HupuService(PlatformService):
    """虎扑热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取虎扑热搜"""
        try:
            url = "https://bbs.hupu.com/all-gambia"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://bbs.hupu.com/",
                "Cookie": "sajssdk_2015_cross_new_user=1"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 使用与 Go 代码相同的正则表达式模式
            pattern = r'<div class="post-title">\s*<a[^>]*href="([^"]+)"[^>]*>\s*<span[^>]*>([^<]+)</span>'
            matched = self.extract_matches(response.text, pattern)
            
            hot_items = []
            for i, item in enumerate(matched):
                url = item[0]
                if not url.startswith('http'):
                    url = f"https://bbs.hupu.com{url}"
                
                hot_item = HotSearchItem(
                    id=i + 1,
                    title=item[1].strip(),
                    url=url,
                    platform="hupu",
                    rank=i + 1
                )
                hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取虎扑热搜失败: {str(e)}")
            return []

class IthomeService(PlatformService):
    """IT之家热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取IT之家热搜"""
        try:
            url = "https://www.ithome.com/block/api/getlist"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://www.ithome.com/",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {
                "type": "rank",
                "name": "24h"
            }
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data:
                for i, item in enumerate(data["data"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("title", ""),
                        url=item.get("link", ""),
                        hot_value=self.format_hot_value(item.get("comment", 0)),
                        platform="ithome",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取IT之家热搜失败: {str(e)}")
            return []

class LishipinService(PlatformService):
    """梨视频热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取梨视频热搜"""
        try:
            url = "https://www.pearvideo.com/popular_loading.jsp"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://www.pearvideo.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            pattern = r'<a href="([^"]+)"[^>]*>\s*<h2[^>]*>([^<]+)</h2>'
            matched = self.extract_matches(response.text, pattern)
            
            hot_items = []
            for i, item in enumerate(matched):
                url = item[0]
                if not url.startswith('http'):
                    url = f"https://www.pearvideo.com/{url}"
                
                hot_item = HotSearchItem(
                    id=i + 1,
                    title=item[1].strip(),
                    url=url,
                    platform="lishipin",
                    rank=i + 1
                )
                hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取梨视频热搜失败: {str(e)}")
            return []

class PengpaiService(PlatformService):
    """澎湃新闻热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        try:
            url = "https://www.thepaper.cn/load_chosen.jsp"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://www.thepaper.cn/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            pattern = r'<a href="([^"]+)"[^>]*>\s*<h2[^>]*>([^<]+)</h2>\s*<div[^>]*>(\d+)</div>'
            matched = self.extract_matches(response.text, pattern)
            
            hot_items = []
            for i, item in enumerate(matched):
                url = item[0]
                if not url.startswith('http'):
                    url = f"https://www.thepaper.cn{url}"
                
                hot_item = HotSearchItem(
                    id=i + 1,
                    title=item[1].strip(),
                    url=url,
                    hot_value=self.format_hot_value(item[2]),
                    platform="pengpai",
                    rank=i + 1
                )
                hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取澎湃新闻热搜失败: {str(e)}")
            return []

class QqnewsService(PlatformService):
    """腾讯新闻热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        try:
            url = "https://i.news.qq.com/trpc.qqnews_web.pc_base_srv.base_http_proxy/NinjaPageContentSync?pull_urls=news_top_2018"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://news.qq.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data and "news_top_2018" in data["data"]:
                for i, item in enumerate(data["data"]["news_top_2018"]["children"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        hot_value=self.format_hot_value(item.get("view_count", 0)),
                        platform="qqnews",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取腾讯新闻热搜失败: {str(e)}")
            return []

class ShaoshupaiService(PlatformService):
    """少数派热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取少数派热搜"""
        try:
            url = "https://sspai.com/api/v1/article/tag/page/get?limit=50&tag=热门文章"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://sspai.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data:
                for i, item in enumerate(data["data"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("title", ""),
                        url=f"https://sspai.com/post/{item.get('id', '')}",
                        hot_value=self.format_hot_value(item.get("like_count", 0)),  # 添加热度值
                        platform="shaoshupai",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取少数派热搜失败: {str(e)}")
            return []

class SougouService(PlatformService):
    """搜狗热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取搜狗热搜"""
        try:
            url = "https://sa.sogou.com/new/getRankData"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://sa.sogou.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data and "topwords" in data["data"]:
                for i, item in enumerate(data["data"]["topwords"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("word", ""),
                        url=f"https://www.sogou.com/web?query={item.get('word', '')}",
                        hot_value=self.format_hot_value(item.get("number", 0)),
                        platform="sougou",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取搜狗热搜失败: {str(e)}")
            return []

class ToutiaoService(PlatformService):
    """今日头条热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取今日头条热搜"""
        try:
            url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc&_signature=_02B4Z6wo00901IjN4-gAAIDBvqPRadqvS7RD.5pAAO.YwY"
            headers = {
                "User-Agent": self.user_agent,
                "Cookie": "tt_webid=7254553744002524715",
                "Referer": "https://www.toutiao.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data:
                for i, item in enumerate(data["data"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("Title", ""),
                        url=item.get("Url", ""),
                        hot_value=self.format_hot_value(item.get("HotValue", 0)),
                        platform="toutiao",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取今日头条热搜失败: {str(e)}")
            return []

class V2exService(PlatformService):
    """V2EX热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取V2EX热搜"""
        try:
            url = "https://www.v2ex.com/?tab=hot"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            pattern = r'<span\s+class="item_title">\s*<a\s+href="([^"]+)"[^>]*>([^<]+)</a>'
            matched = self.extract_matches(response.text, pattern)
            
            hot_items = []
            for i, item in enumerate(matched):
                hot_item = HotSearchItem(
                    id=i + 1,  # 添加 id
                    title=item[1],
                    url=f"https://www.v2ex.com{item[0]}",
                    platform="v2ex",
                    rank=i + 1
                )
                hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取V2EX热搜失败: {str(e)}")
            return []

class WangyiNewsService(PlatformService):
    """网易新闻热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取网易新闻热搜"""
        try:
            url = "https://m.163.com/fe/api/hot/news/flow"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://www.163.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data and "list" in data["data"]:
                for i, item in enumerate(data["data"]["list"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        hot_value=self.format_hot_value(item.get("clickCount", 0)),
                        platform="wangyi",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取网易新闻热搜失败: {str(e)}")
            return []

class XinjingbaoService(PlatformService):
    """新京报热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取新京报热搜"""
        try:
            url = "https://www.bjnews.com.cn/api/articles/top"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://www.bjnews.com.cn/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data and "list" in data["data"]:
                for i, item in enumerate(data["data"]["list"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("title", ""),
                        url=f"https://www.bjnews.com.cn/detail/{item.get('id', '')}",
                        hot_value=self.format_hot_value(item.get("views", 0)),
                        platform="xinjingbao",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取新京报热搜失败: {str(e)}")
            return []

class QuarkService(PlatformService):
    """夸克热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取夸克热搜"""
        try:
            url = "https://quark.sm.cn/api/rest?method=quark.home.getHomeData&format=json"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://quark.sm.cn/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data and "hot_search" in data["data"]:
                for i, item in enumerate(data["data"]["hot_search"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        hot_value=self.format_hot_value(item.get("hot_score", 0)),
                        platform="quark",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取夸克热搜失败: {str(e)}")
            return []

class SouhuService(PlatformService):
    """搜狐热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取搜狐热搜"""
        try:
            url = "https://v2.sohu.com/integration-api/mix/region/6156"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://www.sohu.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_items = []
            
            if "data" in data and "data" in data["data"]:
                for i, item in enumerate(data["data"]["data"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        hot_value=self.format_hot_value(item.get("readCount", 0)),
                        platform="souhu",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取搜狐热搜失败: {str(e)}")
            return []

class RenminwangService(PlatformService):
    """人民网热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取人民网热搜"""
        try:
            url = "http://news.people.com.cn/210801/211150/index.js"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "http://www.people.com.cn/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            # 处理JSONP格式
            text = response.text.strip()
            text = text.replace("news_callback(", "").rstrip(");")
            
            data = json.loads(text)
            hot_items = []
            
            if "items" in data:
                for i, item in enumerate(data["items"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        platform="renminwang",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取人民网热搜失败: {str(e)}")
            return []

class NanfangzhoumoService(PlatformService):
    """南方周末热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取南方周末热搜"""
        try:
            url = "https://www.infzm.com/contents"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://www.infzm.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            pattern = r'<a href="/contents/(\d+)"[^>]*>\s*<h2[^>]*>([^<]+)</h2>'
            matched = self.extract_matches(response.text, pattern)
            
            hot_items = []
            for i, item in enumerate(matched):
                hot_item = HotSearchItem(
                    id=i + 1,
                    title=item[1].strip(),
                    url=f"https://www.infzm.com/contents/{item[0]}",
                    platform="nanfangzhoumo",
                    rank=i + 1
                )
                hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取南方周末热搜失败: {str(e)}")
            return []

class Doc360Service(PlatformService):
    """360doc热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取360doc热搜"""
        try:
            url = "http://www.360doc.com/index.html"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "http://www.360doc.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            pattern = r'<div class="hot_box">\s*<a href="([^"]+)"[^>]*>\s*<div[^>]*>\s*<div[^>]*>([^<]+)</div>'
            matched = self.extract_matches(response.text, pattern)
            
            hot_items = []
            for i, item in enumerate(matched):
                hot_item = HotSearchItem(
                    id=i + 1,
                    title=item[1].strip(),
                    url=item[0],
                    platform="360doc",
                    rank=i + 1
                )
                hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取360doc热搜失败: {str(e)}")
            return []

class CCTVService(PlatformService):
    """CCTV新闻热搜服务"""
    
    def get_hot_search(self) -> List[HotSearchItem]:
        """获取CCTV新闻热搜"""
        try:
            url = "https://news.cctv.com/data/index.json"
            headers = {
                "User-Agent": self.user_agent,
                "Referer": "https://news.cctv.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            data = response.json()
            hot_items = []
            
            if "rollData" in data:
                for i, item in enumerate(data["rollData"]):
                    hot_item = HotSearchItem(
                        id=i + 1,
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        platform="cctv",
                        rank=i + 1
                    )
                    hot_items.append(hot_item)
            
            return hot_items
        except Exception as e:
            self.logger.error(f"获取CCTV新闻热搜失败: {str(e)}")
            return [] 
            return [] 