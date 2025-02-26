# 所有平台处理器
from flask import jsonify, Blueprint, request
import logging

from models.models import ApiResponse
from services.all_service import AllService
from services.platform_services import (
    BaiduService, BilibiliService, WeiboHotService, ZhihuService,
    Search360Service, AcfunService, CSDNService, DongqiudiService,
    DoubanService, DouyinService, GithubService, GuojiadiliService,
    HistoryService, HupuService, IthomeService, LishipinService,
    PengpaiService, QqnewsService, ShaoshupaiService, SougouService,
    ToutiaoService, V2exService, WangyiNewsService, XinjingbaoService,
    QuarkService, SouhuService, RenminwangService, NanfangzhoumoService,
    Doc360Service, CCTVService
)

# 创建蓝图
all_bp = Blueprint('all', __name__)
all_service = AllService()
logger = logging.getLogger(__name__)

@all_bp.route('/', methods=['GET'])
def index():
    """首页"""
    return jsonify({
        "message": "热搜 API 服务",
        "apis_page": "/apis - 查看所有平台API（可视化界面）",
        "endpoints": [
            "/all - 获取所有平台热搜",
            "/baidu - 获取百度热搜",
            "/bilibili - 获取哔哩哔哩热搜",
            "/weibo - 获取微博热搜",
            "/zhihu - 获取知乎热搜",
            "/360search - 获取360搜索热搜",
            "/acfun - 获取AcFun热搜",
            "/csdn - 获取CSDN热搜",
            "/dongqiudi - 获取懂球帝热搜",
            "/douban - 获取豆瓣热搜",
            "/douyin - 获取抖音热搜",
            "/github - 获取GitHub热搜",
            "/guojiadili - 获取国家地理热搜",
            "/history - 获取历史上的今天",
            "/hupu - 获取虎扑热搜",
            "/ithome - 获取IT之家热搜",
            "/lishipin - 获取梨视频热搜",
            "/pengpai - 获取澎湃新闻热搜",
            "/qqnews - 获取腾讯新闻热搜",
            "/shaoshupai - 获取少数派热搜",
            "/sougou - 获取搜狗热搜",
            "/toutiao - 获取今日头条热搜",
            "/v2ex - 获取V2EX热搜",
            "/wangyi - 获取网易新闻热搜",
            "/xinjingbao - 获取新京报热搜",
            "/quark - 获取夸克热搜",
            "/souhu - 获取搜狐热搜",
            "/renminwang - 获取人民网热搜",
            "/nanfangzhoumo - 获取南方周末热搜",
            "/360doc - 获取360doc热搜",
            "/cctv - 获取CCTV新闻热搜",
            "/api/hot-search - 获取热搜数据"
        ]
    })

@all_bp.route('/all', methods=['GET'])
def get_all_hot_search():
    """获取所有平台热搜接口"""
    try:
        all_hot_search = all_service.get_all_hot_search()
        response = ApiResponse(data=all_hot_search)
        return jsonify(response.to_dict())
    except Exception as e:
        logger.error(f"获取所有平台热搜失败: {str(e)}")
        error_response = ApiResponse(code=500, message=f"服务器错误: {str(e)}", data=None)
        return jsonify(error_response.to_dict()), 500

# 通用处理函数生成器
def create_platform_handler(service_class, platform_name):
    def handler():
        try:
            service = service_class()
            hot_items = service.get_hot_search()
            
            if hot_items:
                response = ApiResponse(data=[item.to_dict() for item in hot_items])
            else:
                response = ApiResponse(code=404, message=f"未找到{platform_name}热搜数据", data=None)
            return jsonify(response.to_dict())
        except Exception as e:
            logger.error(f"获取{platform_name}热搜失败: {str(e)}")
            error_response = ApiResponse(code=500, message=f"服务器错误: {str(e)}", data=None)
            return jsonify(error_response.to_dict()), 500
    return handler

# 注册各平台路由
@all_bp.route('/baidu', methods=['GET'])
def get_baidu_hot_search():
    return create_platform_handler(BaiduService, "百度")()

@all_bp.route('/bilibili', methods=['GET'])
def get_bilibili_hot_search():
    return create_platform_handler(BilibiliService, "哔哩哔哩")()

@all_bp.route('/weibo', methods=['GET'])
def get_weibo_hot_search():
    return create_platform_handler(WeiboHotService, "微博")()

@all_bp.route('/zhihu', methods=['GET'])
def get_zhihu_hot_search():
    return create_platform_handler(ZhihuService, "知乎")()

@all_bp.route('/360search', methods=['GET'])
def get_360search_hot_search():
    return create_platform_handler(Search360Service, "360搜索")()

@all_bp.route('/acfun', methods=['GET'])
def get_acfun_hot_search():
    return create_platform_handler(AcfunService, "AcFun")()

@all_bp.route('/csdn', methods=['GET'])
def get_csdn_hot_search():
    return create_platform_handler(CSDNService, "CSDN")()

@all_bp.route('/dongqiudi', methods=['GET'])
def get_dongqiudi_hot_search():
    return create_platform_handler(DongqiudiService, "懂球帝")()

@all_bp.route('/douban', methods=['GET'])
def get_douban_hot_search():
    return create_platform_handler(DoubanService, "豆瓣")()

@all_bp.route('/douyin', methods=['GET'])
def get_douyin_hot_search():
    return create_platform_handler(DouyinService, "抖音")()

@all_bp.route('/github', methods=['GET'])
def get_github_hot_search():
    return create_platform_handler(GithubService, "GitHub")()

@all_bp.route('/guojiadili', methods=['GET'])
def get_guojiadili_hot_search():
    return create_platform_handler(GuojiadiliService, "国家地理")()

@all_bp.route('/history', methods=['GET'])
def get_history_hot_search():
    return create_platform_handler(HistoryService, "历史上的今天")()

@all_bp.route('/hupu', methods=['GET'])
def get_hupu_hot_search():
    return create_platform_handler(HupuService, "虎扑")()

@all_bp.route('/ithome', methods=['GET'])
def get_ithome_hot_search():
    return create_platform_handler(IthomeService, "IT之家")()

@all_bp.route('/lishipin', methods=['GET'])
def get_lishipin_hot_search():
    return create_platform_handler(LishipinService, "梨视频")()

@all_bp.route('/pengpai', methods=['GET'])
def get_pengpai_hot_search():
    return create_platform_handler(PengpaiService, "澎湃新闻")()

@all_bp.route('/qqnews', methods=['GET'])
def get_qqnews_hot_search():
    return create_platform_handler(QqnewsService, "腾讯新闻")()

@all_bp.route('/shaoshupai', methods=['GET'])
def get_shaoshupai_hot_search():
    return create_platform_handler(ShaoshupaiService, "少数派")()

@all_bp.route('/sougou', methods=['GET'])
def get_sougou_hot_search():
    return create_platform_handler(SougouService, "搜狗")()

@all_bp.route('/toutiao', methods=['GET'])
def get_toutiao_hot_search():
    return create_platform_handler(ToutiaoService, "今日头条")()

@all_bp.route('/v2ex', methods=['GET'])
def get_v2ex_hot_search():
    return create_platform_handler(V2exService, "V2EX")()

@all_bp.route('/wangyi', methods=['GET'])
def get_wangyi_hot_search():
    return create_platform_handler(WangyiNewsService, "网易新闻")()

@all_bp.route('/xinjingbao', methods=['GET'])
def get_xinjingbao_hot_search():
    return create_platform_handler(XinjingbaoService, "新京报")()

@all_bp.route('/quark', methods=['GET'])
def get_quark_hot_search():
    return create_platform_handler(QuarkService, "夸克")()

@all_bp.route('/souhu', methods=['GET'])
def get_souhu_hot_search():
    return create_platform_handler(SouhuService, "搜狐")()

@all_bp.route('/renminwang', methods=['GET'])
def get_renminwang_hot_search():
    return create_platform_handler(RenminwangService, "人民网")()

@all_bp.route('/nanfangzhoumo', methods=['GET'])
def get_nanfangzhoumo_hot_search():
    return create_platform_handler(NanfangzhoumoService, "南方周末")()

@all_bp.route('/360doc', methods=['GET'])
def get_360doc_hot_search():
    return create_platform_handler(Doc360Service, "360doc")()

@all_bp.route('/cctv', methods=['GET'])
def get_cctv_hot_search():
    return create_platform_handler(CCTVService, "CCTV新闻")()

@all_bp.route('/apis', methods=['GET'])
def get_apis():
    """获取所有可用的API接口列表"""
    try:
        # 获取所有平台服务，使用更可靠的图标源
        platforms = [
            {"name": "百度", "endpoint": "/baidu", "icon": "https://www.baidu.com/favicon.ico"},
            {"name": "哔哩哔哩", "endpoint": "/bilibili", "icon": "https://www.bilibili.com/favicon.ico"},
            {"name": "微博", "endpoint": "/weibo", "icon": "https://h5.sinaimg.cn/m/weibo-lite/icon-default/weibo-lite-logo.png"},
            {"name": "知乎", "endpoint": "/zhihu", "icon": "https://static.zhihu.com/heifetz/favicon.ico"},
            {"name": "360搜索", "endpoint": "/360search", "icon": "https://p.ssl.qhimg.com/t01749f23f4e643346f.png"},
            {"name": "AcFun", "endpoint": "/acfun", "icon": "https://cdn.aixifan.com/ico/favicon.ico"},
            {"name": "CSDN", "endpoint": "/csdn", "icon": "https://g.csdnimg.cn/static/logo/favicon32.ico"},
            {"name": "懂球帝", "endpoint": "/dongqiudi", "icon": "https://static1.dqdgame.com/favicon.ico"},
            {"name": "豆瓣", "endpoint": "/douban", "icon": "https://img3.doubanio.com/favicon.ico"},
            {"name": "抖音", "endpoint": "/douyin", "icon": "https://lf1-cdn-tos.bytegoofy.com/goofy/ies/douyin_web/public/favicon.ico"},
            {"name": "GitHub", "endpoint": "/github", "icon": "https://github.githubassets.com/favicons/favicon.png"},
            {"name": "国家地理", "endpoint": "/guojiadili", "icon": "https://www.ngchina.com.cn/favicon.ico"},
            {"name": "历史上的今天", "endpoint": "/history", "icon": "https://cdn.todayonhistory.com/favicon.ico"},
            {"name": "虎扑", "endpoint": "/hupu", "icon": "https://w1.hoopchina.com.cn/images/pc/old/favicon.ico"},
            {"name": "IT之家", "endpoint": "/ithome", "icon": "https://img.ithome.com/m/images/logo.png"},
            {"name": "梨视频", "endpoint": "/lishipin", "icon": "https://static.pearvideo.com/public/assets/images/favicon.ico"},
            {"name": "澎湃新闻", "endpoint": "/pengpai", "icon": "https://file.thepaper.cn/wap/v3/img/logo_32.png"},
            {"name": "腾讯新闻", "endpoint": "/qqnews", "icon": "https://mat1.gtimg.com/qqcdn/qqindex2021/favicon.ico"},
            {"name": "少数派", "endpoint": "/shaoshupai", "icon": "https://cdn.sspai.com/sspai/assets/img/favicon/icon.ico"},
            {"name": "搜狗", "endpoint": "/sougou", "icon": "https://dlweb.sogoucdn.com/logo/images/2018/favicon.ico"},
            {"name": "今日头条", "endpoint": "/toutiao", "icon": "https://sf1-cdn-tos.douyinstatic.com/obj/eden-cn/pisces/favicon.ico"},
            {"name": "V2EX", "endpoint": "/v2ex", "icon": "https://www.v2ex.com/static/icon-192.png"},
            {"name": "网易新闻", "endpoint": "/wangyi", "icon": "https://static.ws.126.net/163/favicon.ico"},
            {"name": "新京报", "endpoint": "/xinjingbao", "icon": "https://i2.bjnews.com.cn/favicon.ico"},
            {"name": "夸克", "endpoint": "/quark", "icon": "https://b.bdstatic.com/searchbox/icms/searchbox/img/quark-logo.png"},
            {"name": "搜狐", "endpoint": "/souhu", "icon": "https://statics.itc.cn/web/static/images/pic/sohu-logo/favicon.ico"},
            {"name": "人民网", "endpoint": "/renminwang", "icon": "http://www.people.com.cn/img/2020people/images/favicon.ico"},
            {"name": "南方周末", "endpoint": "/nanfangzhoumo", "icon": "https://assets.infzm.com/frontend/assets/infzm-favicon.ico"},
            {"name": "360doc", "endpoint": "/360doc", "icon": "https://www.360doc.cn/favicon.ico"},
            {"name": "CCTV新闻", "endpoint": "/cctv", "icon": "https://tv.cctv.com/favicon.ico"}
        ]
        
        # 添加备用图标和错误处理
        html = """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>热搜 API 服务</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                h1 {
                    color: #333;
                    text-align: center;
                    margin-bottom: 30px;
                }
                .platform-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                    gap: 20px;
                }
                .platform-card {
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    padding: 15px;
                    text-align: center;
                    transition: transform 0.2s, box-shadow 0.2s;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                .platform-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }
                .platform-card a {
                    text-decoration: none;
                    color: #333;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    width: 100%;
                }
                .icon-wrapper {
                    width: 48px;
                    height: 48px;
                    margin-bottom: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                }
                .platform-icon {
                    max-width: 100%;
                    max-height: 100%;
                    width: auto;
                    height: auto;
                    object-fit: contain;
                }
                .platform-icon-fallback {
                    width: 48px;
                    height: 48px;
                    margin-bottom: 10px;
                    background-color: #f0f0f0;
                    border-radius: 50%;
                    display: none;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    color: #666;
                    font-size: 20px;
                }
                .platform-name {
                    font-weight: bold;
                    margin-top: 8px;
                    font-size: 14px;
                }
                .footer {
                    margin-top: 40px;
                    text-align: center;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <h1>热搜 API 服务</h1>
            <div class="platform-grid">
        """
        
        # 添加平台卡片，包含图标错误处理
        for platform in platforms:
            html += f"""
                <div class="platform-card">
                    <a href="{platform['endpoint']}" target="_blank">
                        <div class="icon-wrapper">
                            <img src="{platform['icon']}" alt="{platform['name']}" class="platform-icon" 
                                 onerror="this.style.display='none';this.nextElementSibling.style.display='flex';">
                            <div class="platform-icon-fallback">{platform['name'][0]}</div>
                        </div>
                        <div class="platform-name">{platform['name']}</div>
                    </a>
                </div>
            """
        
        html += """
            </div>
            <div class="footer">
                <p>热搜 API 服务 &copy; 2023</p>
                <p><a href="/all" target="_blank">获取所有平台热搜</a></p>
            </div>
            <script>
            // 改进的图标加载错误处理
            document.addEventListener('DOMContentLoaded', function() {
                const icons = document.querySelectorAll('.platform-icon');
                icons.forEach(icon => {
                    // 检查图片是否已经加载失败
                    if (icon.complete && icon.naturalHeight === 0) {
                        handleIconError(icon);
                    }
                    
                    // 添加加载错误事件监听器
                    icon.addEventListener('error', function() {
                        handleIconError(this);
                    });
                });
                
                function handleIconError(icon) {
                    icon.style.display = 'none';
                    const fallback = icon.nextElementSibling;
                    if (fallback) {
                        fallback.style.display = 'flex';
                    }
                }
            });
            </script>
        </body>
        </html>
        """
        
        return html
    except Exception as e:
        logger.error(f"获取APIs列表失败: {str(e)}")
        error_response = ApiResponse(code=500, message=f"服务器错误: {str(e)}", data=None)
        return jsonify(error_response.to_dict()), 500

@all_bp.route('/apis.json', methods=['GET'])
def get_apis_json():
    """获取所有可用的API接口列表（JSON格式）"""
    try:
        # 获取所有平台服务，更新图标URL
        platforms = [
            {"name": "百度", "endpoint": "/baidu", "icon": "https://www.baidu.com/favicon.ico"},
            {"name": "哔哩哔哩", "endpoint": "/bilibili", "icon": "https://www.bilibili.com/favicon.ico"},
            {"name": "微博", "endpoint": "/weibo", "icon": "https://weibo.com/favicon.ico"},
            {"name": "知乎", "endpoint": "/zhihu", "icon": "https://static.zhihu.com/heifetz/favicon.ico"},
            {"name": "360搜索", "endpoint": "/360search", "icon": "https://p.ssl.qhimg.com/t01749f23f4e643346f.png"},
            {"name": "AcFun", "endpoint": "/acfun", "icon": "https://www.acfun.cn/favicon.ico"},
            {"name": "CSDN", "endpoint": "/csdn", "icon": "https://g.csdnimg.cn/static/logo/favicon32.ico"},
            {"name": "懂球帝", "endpoint": "/dongqiudi", "icon": "https://www.dongqiudi.com/favicon.ico"},
            {"name": "豆瓣", "endpoint": "/douban", "icon": "https://www.douban.com/favicon.ico"},
            {"name": "抖音", "endpoint": "/douyin", "icon": "https://www.douyin.com/favicon.ico"},
            {"name": "GitHub", "endpoint": "/github", "icon": "https://github.githubassets.com/favicons/favicon.png"},
            {"name": "国家地理", "endpoint": "/guojiadili", "icon": "http://www.dili360.com/favicon.ico"},
            {"name": "历史上的今天", "endpoint": "/history", "icon": "https://baike.baidu.com/favicon.ico"},
            {"name": "虎扑", "endpoint": "/hupu", "icon": "https://www.hupu.com/favicon.ico"},
            {"name": "IT之家", "endpoint": "/ithome", "icon": "https://www.ithome.com/favicon.ico"},
            {"name": "梨视频", "endpoint": "/lishipin", "icon": "https://page.pearvideo.com/webres/img/logo.png"},
            {"name": "澎湃新闻", "endpoint": "/pengpai", "icon": "https://www.thepaper.cn/favicon.ico"},
            {"name": "腾讯新闻", "endpoint": "/qqnews", "icon": "https://mat1.gtimg.com/qqcdn/qqindex2021/favicon.ico"},
            {"name": "少数派", "endpoint": "/shaoshupai", "icon": "https://cdn-static.sspai.com/favicon/sspai.ico"},
            {"name": "搜狗", "endpoint": "/sougou", "icon": "https://www.sogou.com/favicon.ico"},
            {"name": "今日头条", "endpoint": "/toutiao", "icon": "https://www.toutiao.com/favicon.ico"},
            {"name": "V2EX", "endpoint": "/v2ex", "icon": "https://www.v2ex.com/favicon.ico"},
            {"name": "网易新闻", "endpoint": "/wangyi", "icon": "https://www.163.com/favicon.ico"},
            {"name": "新京报", "endpoint": "/xinjingbao", "icon": "https://www.bjnews.com.cn/favicon.ico"},
            {"name": "夸克", "endpoint": "/quark", "icon": "https://gw.alicdn.com/imgextra/i3/O1CN018r2tKf28YP7ev0fPF_!!6000000007944-2-tps-48-48.png"},
            {"name": "搜狐", "endpoint": "/souhu", "icon": "https://www.sohu.com/favicon.ico"},
            {"name": "人民网", "endpoint": "/renminwang", "icon": "http://www.people.com.cn/favicon.ico"},
            {"name": "南方周末", "endpoint": "/nanfangzhoumo", "icon": "https://www.infzm.com/favicon.ico"},
            {"name": "360doc", "endpoint": "/360doc", "icon": "http://www.360doc.com/favicon.ico"},
            {"name": "CCTV新闻", "endpoint": "/cctv", "icon": "https://news.cctv.com/favicon.ico"}
        ]
        
        response = ApiResponse(data=platforms)
        return jsonify(response.to_dict())
    except Exception as e:
        logger.error(f"获取APIs列表失败: {str(e)}")
        error_response = ApiResponse(code=500, message=f"服务器错误: {str(e)}", data=None)
        return jsonify(error_response.to_dict()), 500 