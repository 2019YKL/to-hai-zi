# 海子诗歌集 🌾

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-121013?style=flat&logo=github&logoColor=white)](https://2019ykl.github.io/to-hai-zi/)

一个优雅的海子诗歌展示网站，致敬这位中国当代诗歌的传奇人物。

采用现代化设计理念，为读者提供沉浸式的诗歌阅读体验。

## ✨ 特性

- 🎨 **极简美学设计** - 纯净的阅读界面，让诗歌成为焦点
- 📱 **响应式布局** - 完美适配桌面端、平板和移动设备
- 🔍 **智能搜索** - 支持标题、内容、章节的全文搜索，实时高亮匹配结果
- 🖼️ **精美配图** - 每首诗歌配有对应精心挑选的高质量图片
- ⚡ **流畅交互** - 优雅的动画效果和玻璃态毛化设计
- ⌨️ **键盘导航** - 完整的键盘快捷键支持

## 🌊 在线预览

🔗 **[访问网站](https://haizi.jkaihub.com/)**

> "活在这珍贵的人间，太阳强烈，水波温柔" —— 海子

## 📚 收录内容

### 诗歌章节
- **短诗集 (1983-1986)** - 早期创作，共84首
- **长诗集 (1984-1985)** - 代表性长篇诗歌，共5首  
- **短诗集 (1987-1989)** - 成熟期作品，共118首

### 代表作品
- 《面朝大海，春暖花开》- 最广为流传的诗歌
- 《春天，十个海子》- 反映内心世界的杰作
- 《以梦为马》- 理想主义的颂歌
- 《麦地》系列 - 对土地的深情眷恋
- 《四姐妹》- 温柔的抒情诗

**共收录 207 首诗歌**

## 🛠️ 技术栈

- **前端技术**: HTML5, CSS3, Vanilla JavaScript
- **样式框架**: Tailwind CSS
- **字体**: 霞鹜文楷 (LXGWWenKai) - 专为中文优化
- **图片托管**: 聚合图床 - 国内访问更稳定
- **搜索功能**: 纯前端实现，支持正则表达式
- **部署平台**: GitHub Pages / Vercel / cloudflare page/支持静态页部署平台

## 🚀 快速开始

### 本地运行

```bash
# 克隆项目
git clone https://github.com/2019YKL/to-hai-zi.git
cd to-hai-zi

# 启动本地服务器 (任选一种)
# Python 3
python -m http.server 8000

# Node.js (需要安装 http-server)
npx http-server .

# 访问 http://localhost:8000
```

## 📁 项目结构

```
to-hai-zi/
├── index.html                 # 主页 - 诗歌列表和搜索
├── poem.html                  # 诗歌详情页
├── search.js                  # 搜索功能实现
├── assets/
│   ├── js/
│   │   ├── poems-data.js      # 诗歌数据 (207首)
│   │   └── content-manager.js # 内容管理系统
│   ├── images/
│   │   └── image-haizi.jpg    # 海子照片
│   └── content/
│       └── poems/             # 诗歌 Markdown 文件
│           ├── 00-preface/    # 序言
│           ├── 01-short-poems-1983-1986/  # 早期短诗
│           ├── 02-long-poems-1984-1985/   # 长诗
│           └── 03-short-poems-1987-1989/  # 晚期短诗
├── LXGWWenKai-Regular.ttf     # 中文字体文件
└── README.md
```

## 🎨 设计理念

### 诗意美学
- **极简主义**: 去除冗余元素，突出诗歌内容
- **意境营造**: 通过色彩、字体、布局营造诗意氛围

### 技术哲学
- **内容优先**: 技术服务于内容展示，不喧宾夺主
- **可维护性**: 模块化设计，易于扩展和维护

## 🌟 贡献指南

欢迎为项目做出贡献！你可以：

1. **报告问题**: 在 [Issues](https://github.com/2019YKL/to-hai-zi/issues) 中报告 bug 或提出建议
2. **完善内容**: 校对诗歌文本，补充缺失作品
3. **优化体验**: 改进界面设计或用户体验
4. **功能开发**: 添加新功能或优化现有功能

### 提交流程
```bash
# Fork 项目并克隆到本地
git clone https://github.com/your-username/to-hai-zi.git

# 创建功能分支
git checkout -b feature/your-feature

# 提交更改
git commit -m "Add: your feature description"

# 推送到你的仓库
git push origin feature/your-feature

# 创建 Pull Request
```

## 📄 版权说明

- **代码**: 采用 [MIT License](https://choosealicense.com/licenses/mit/) 开源协议
- **诗歌内容**: 海子诗歌作品版权归原作者所有
- **图片资源**: 来源于PexPel图库，遵循相应使用协议

## 🙏 致谢

- **海子** - 感谢诗人留下的珍贵作品
- **霞鹜文楷** - 优美的中文字体
- **Tailwind CSS** - 强大的CSS框架

---

> "从明天起，做一个幸福的人  
> 喂马、劈柴，周游世界  
> 从明天起，关心粮食和蔬菜  
> 我有一所房子，面朝大海，春暖花开"  
> 
> —— 海子《面朝大海，春暖花开》

**⭐ 如果这个项目对你有帮助，请给它一个星标！**