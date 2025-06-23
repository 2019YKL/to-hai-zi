# 海子诗歌集

一个美观、极简的海子诗歌展示网站，采用现代化设计理念和内容管理系统，致敬这位伟大的诗人。

## ✨ 特性

- 🎨 **极简美学**：纯白背景，优雅排版，诗意十足
- 📱 **响应式设计**：完美适配桌面端和移动端
- 🖼️ **精美配图**：每首诗配有来自 Unsplash 的高质量图片
- ⚡ **流畅动画**：淡入效果和悬停交互
- 📄 **分页功能**：每页展示 6 首诗歌，支持键盘导航
- 🔄 **内容管理**：Markdown 驱动的内容系统，易于维护
- 🔗 **智能导航**：诗歌间的前后导航，键盘快捷键支持
- 🎭 **沉浸式体验**：专为诗歌阅读优化的用户界面

## 📚 收录诗歌

### 代表作品
- 面朝大海，春暖花开 (1989年1月) - 海子最著名的诗歌之一
- 春天，十个海子 (1989年) - 反映诗人内心分裂与痛苦
- 以梦为马 (1987年) - 诗人的理想与追求

### 早期作品
- 亚洲铜 (1984年) - 海子早期的代表作
- 村庄 (1986年) - 对故乡的眷恋
- 九月 (1986年) - 充满神秘主义色彩
- 重建家园 (1986年) - 对家园的思考

### 成熟期作品
- 秋日黄昏 (1987年) - 抒情诗的典范
- 祖国（或以梦为马）(1987年) - 爱国情怀的表达
- 黑夜的献诗 (1987年) - 对黑夜与光明的思考
- 历史 (1987年) - 对历史的反思

### 晚期作品
- 回答 (1988年) - 对麦地的质问
- 麦地 (1988年) - 麦地系列诗歌
- 日记 (1988年) - 孤独与漂泊
- 四姐妹 (1988年) - 对女性的颂歌

**共收录 15 首经典诗歌**

## 🛠️ 技术栈

- **前端框架**：HTML5 + CSS3 + Vanilla JavaScript
- **样式库**：Tailwind CSS
- **字体**：Noto Serif SC (Google Fonts)
- **图片服务**：Unsplash API
- **内容管理**：Markdown + YAML Front Matter
- **部署平台**：Vercel

## 🚀 本地开发

```bash
# 克隆项目
git clone <your-repo-url>
cd haizi-poetry

# 安装依赖
npm install

# 启动开发服务器
npm run dev
# 或者指定端口
npm run preview
```

## 📝 内容管理

### 添加新诗歌

1. 在 `content/poems/` 目录下创建新的 `.md` 文件
2. 使用以下格式：

```markdown
---
title: "诗歌标题"
date: "创作年份"
slug: "url-slug"
image: "https://images.unsplash.com/photo-xxx"
order: 数字排序
preview: |
  诗歌预览
  几行即可
---

完整的诗歌内容
可以包含空行
用于分段
```

3. 在相应的 HTML 文件中创建对应页面，或复制现有模板

### 修改内容

- 编辑 `content/poems/*.md` 文件即可
- 首页和详情页会自动同步内容
- 支持实时预览

## 🌐 部署到 Vercel

### 方法一：GitHub 集成

1. 将代码推送到 GitHub 仓库
2. 在 Vercel 控制台中导入项目
3. 选择静态网站部署
4. 完成自动部署

### 方法二：CLI 部署

```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录 Vercel
vercel login

# 部署
vercel

# 生产环境部署
vercel --prod
```

## 📁 项目结构

```
├── index.html              # 首页（支持分页）
├── poems/                  # 诗歌详情页
│   ├── facing-sea.html     # 面朝大海，春暖花开
│   ├── spring.html         # 春天，十个海子
│   ├── answer.html         # 回答
│   ├── diary.html          # 日记
│   ├── wheat.html          # 麦地
│   ├── village.html        # 村庄
│   ├── horse.html          # 以梦为马
│   └── autumn.html         # 秋日黄昏
├── content/                # 内容管理
│   └── poems/              # 诗歌 Markdown 文件
│       ├── facing-sea.md
│       ├── spring.md
│       ├── answer.md
│       ├── diary.md
│       ├── wheat.md
│       ├── village.md
│       ├── horse.md
│       └── autumn.md
├── js/                     # JavaScript 文件
│   └── content-manager.js  # 内容管理系统
├── vercel.json             # Vercel 配置
├── package.json            # 项目配置
├── .gitignore              # Git 忽略文件
└── README.md               # 项目说明
```

## ⌨️ 键盘快捷键

- **首页**：
  - `←` / `→` 切换页面
- **诗歌详情页**：
  - `←` 上一首诗
  - `→` 下一首诗

## 🎯 设计理念

本项目致力于创造一个纯净、优雅的诗歌阅读体验：

- **内容为王**：突出诗歌本身，减少干扰元素
- **诗意美学**：每个设计细节都体现诗歌的意境
- **技术服务内容**：先进的技术栈服务于内容展示
- **可持续发展**：易于维护和扩展的架构设计

## 📄 许可证

MIT License

---

> "活在这珍贵的人间，太阳强烈，水波温柔"  
> —— 海子