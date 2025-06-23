# 海子诗集爬虫系统

## 目录结构
```
scraper/
├── haizi_scraper.py          # 完整版爬虫（功能齐全但较慢）
├── haizi_simple_scraper.py   # 简化版爬虫（推荐使用）
├── md_to_html.py            # Markdown转HTML转换器
├── templates/
│   └── template.html        # HTML模板文件
├── output/
│   ├── haizi_poems.md       # 爬取的诗歌（Markdown格式）
│   └── haizi_poems.html     # 生成的HTML页面
└── README.md               # 本说明文件
```

## 使用方法

### 1. 爬取诗歌
```bash
# 使用简化版爬虫（推荐）
python haizi_simple_scraper.py

# 使用完整版爬虫（功能更全但较慢）
python haizi_scraper.py
```

### 2. 转换为HTML
```bash
python md_to_html.py
```

## 功能特点

- **数据来源**: https://haizi.huhaitai.com/
- **爬取内容**: 海子诗集，按时间分类
- **输出格式**: Markdown + HTML
- **样式设计**: 适配中文诗歌阅读的优雅样式
- **响应式**: 支持移动端访问

## 注意事项

- 爬虫包含请求延迟，避免对目标网站造成压力
- 目前版本爬取前50首诗歌，可修改代码增加数量
- HTML模板支持自定义样式调整