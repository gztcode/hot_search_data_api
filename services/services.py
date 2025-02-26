# 服务层
# 此文件作为服务层的入口，导入并重新导出所有服务
from services.platform_services import *
from services.all_service import AllService

# 导出所有服务
__all__ = [
    'AllService',
    'BaiduService',
    'BilibiliService',
    'WeiboHotService',
    'ZhihuService',
    'Search360Service',
    'AcfunService',
    'CSDNService',
    'DongqiudiService',
    'DoubanService',
    'DouyinService',
    'GithubService',
    'GuojiadiliService',
    'HistoryService',
    'HupuService',
    'IthomeService',
    'LishipinService',
    'PengpaiService',
    'QqnewsService',
    'ShaoshupaiService',
    'SougouService',
    'ToutiaoService',
    'V2exService',
    'WangyiNewsService',
    'XinjingbaoService',
    'QuarkService',
    'SouhuService',
    'RenminwangService',
    'NanfangzhoumoService',
    'Doc360Service',
    'CCTVService'
] 