# 工具函数
import re
import logging
from typing import List, Pattern, Match

logger = logging.getLogger(__name__)

def handle_error(err, message):
    """处理错误"""
    if err:
        logger.error(f"{message}: {str(err)}")
        raise err

def extract_matches(text: str, pattern: str) -> List[List[str]]:
    """提取正则表达式匹配结果"""
    try:
        matches = re.findall(pattern, text, re.DOTALL)
        return matches
    except Exception as e:
        logger.error(f"正则表达式匹配失败: {str(e)}")
        return []

def strip_html(html_string: str) -> str:
    """去除HTML标签"""
    try:
        clean = re.compile('<.*?>')
        return re.sub(clean, '', html_string)
    except Exception as e:
        logger.error(f"去除HTML标签失败: {str(e)}")
        return ""