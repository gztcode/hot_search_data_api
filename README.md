# Hot Search API

一个获取各大网站热搜榜的 API 服务，使用 Python FastAPI 实现。

## 功能特点

- 支持多个主流网站的热搜数据获取
- 统一的 JSON 响应格式
- 简单易用的 RESTful API
- 支持热度值格式化

## 支持的网站

- 百度
- 哔哩哔哩
- 微博
- 知乎
- 360搜索
- AcFun
- CSDN
- 懂球帝
- 豆瓣
- 历史上的今天
- 虎扑
- IT之家
- 梨视频
- 搜狗
- 今日头条
- V2EX
- 网易新闻
- 新京报
- 夸克
- 搜狐
- 人民网
- 南方周末
- 360doc
- CCTV

## 快速开始

## Vercel 一键部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/gztcode/hot_search_data_api)

点击上方按钮，即可快速部署到 Vercel。请将 `<your_github_username>` 替换为你的 GitHub 用户名。


### 环境要求

- Python 3.8+
- FastAPI
- uvicorn

### 安装

1. 克隆项目
```bash
git clone <repository-url>
cd demo
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行服务
```bash
python main.py
```

服务将在 http://127.0.0.1:8000 启动

## API 使用

### 获取所有热搜

```
GET /all
```

### 获取指定网站热搜

```
GET /{platform}
```

platform 支持的值：
- baidu (百度)
- bilibili (哔哩哔哩)
- weibo (微博)
- zhihu (知乎)
- 360search (360搜索)
- acfun (AcFun)
- csdn (CSDN)
- dongqiudi (懂球帝)
- douban (豆瓣)
- history (历史上的今天)
- hupu (虎扑)
- ithome (IT之家)
- lishipin (梨视频)
- sougou (搜狗)
- toutiao (今日头条)
- v2ex (V2EX)
- wangyi (网易新闻)
- xinjingbao (新京报)
- quark (夸克)
- souhu (搜狐)
- renminwang (人民网)
- nanfangzhoumo (南方周末)
- 360doc (360doc)
- cctv (CCTV)

### 响应格式

```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "id": 1,
            "title": "热搜标题",
            "url": "链接地址",
            "hot_value": "热度值",
            "platform": "平台名称",
            "rank": 1,
            "created_at": "创建时间"
        }
    ]
}
```

## 开发

### 项目结构

```
demo/
├── main.py              # 主程序入口
├── models/             # 数据模型
│   └── models.py
├── services/          # 服务实现
│   └── platform_services.py
└── utils/            # 工具函数
    └── utils.py
```

### 添加新的平台

1. 在 `services/platform_services.py` 中创建新的服务类
2. 实现 `get_hot_search` 方法
3. 在 `main.py` 中注册新的路由

## License

Apache License 2.0

## 致谢

本项目参考了 [api-for-hot-search-golang](https://github.com/iiecho1/api-for-hot-search-golang) 的实现。
