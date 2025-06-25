// 海子诗歌内容管理系统
class ContentManager {
    constructor() {
        this.poems = [];
        this.currentPage = 1;
        this.poemsPerPage = 6;
    }

    // 加载诗歌数据
    async loadPoems() {
        // 等待 poems-data.js 加载完成
        let attempts = 0;
        const maxAttempts = 50; // 最多等待5秒
        
        while (typeof poemsData === 'undefined' && attempts < maxAttempts) {
            await new Promise(resolve => setTimeout(resolve, 100));
            attempts++;
        }
        
        if (typeof poemsData !== 'undefined') {
            this.poems = [...poemsData];
        } else {
            throw new Error('诗歌数据加载超时，请刷新页面重试');
        }
        
        // 按章节顺序和标题排序
        this.poems.sort((a, b) => {
            if (a.section_order !== b.section_order) {
                return a.section_order - b.section_order;
            }
            return a.title.localeCompare(b.title, 'zh-CN');
        });
        
        return this.poems;
    }

    // 获取当前页的诗歌
    getCurrentPagePoems() {
        const startIndex = (this.currentPage - 1) * this.poemsPerPage;
        const endIndex = startIndex + this.poemsPerPage;
        return this.poems.slice(startIndex, endIndex);
    }

    // 获取总页数
    getTotalPages() {
        return Math.ceil(this.poems.length / this.poemsPerPage);
    }

    // 设置当前页
    setCurrentPage(page) {
        const totalPages = this.getTotalPages();
        if (page >= 1 && page <= totalPages) {
            this.currentPage = page;
            return true;
        }
        return false;
    }

    // 根据slug获取诗歌
    getPoemBySlug(slug) {
        return this.poems.find(poem => poem.slug === slug);
    }

    // 根据路径获取诗歌
    getPoemByPath(path) {
        return this.poems.find(poem => poem.path === path);
    }

    // 获取相邻诗歌（用于导航）
    getAdjacentPoems(slug) {
        const currentIndex = this.poems.findIndex(poem => poem.slug === slug);
        if (currentIndex === -1) {
            return { previous: null, next: null };
        }
        
        return {
            previous: currentIndex > 0 ? this.poems[currentIndex - 1] : null,
            next: currentIndex < this.poems.length - 1 ? this.poems[currentIndex + 1] : null
        };
    }

    // 按章节分组获取诗歌
    getPoemsBySection() {
        const sections = {};
        this.poems.forEach(poem => {
            const sectionName = poem.section;
            if (!sections[sectionName]) {
                sections[sectionName] = [];
            }
            sections[sectionName].push(poem);
        });
        return sections;
    }

    // 搜索诗歌
    searchPoems(query) {
        if (!query.trim()) {
            return this.poems;
        }
        
        const lowerQuery = query.toLowerCase();
        return this.poems.filter(poem => 
            poem.title.toLowerCase().includes(lowerQuery) ||
            poem.preview.toLowerCase().includes(lowerQuery) ||
            poem.section.toLowerCase().includes(lowerQuery)
        );
    }

    // 生成诗歌URL (SEO友好的英文slug)
    getPoemUrl(poem) {
        return `poem.html?slug=${poem.slug}`;
    }
    
    // 生成传统URL（向后兼容）
    getLegacyPoemUrl(poem) {
        return `poem.html?poem=${encodeURIComponent(poem.path)}`;
    }

    // 获取统计信息
    getStats() {
        const sections = this.getPoemsBySection();
        const stats = {
            total: this.poems.length,
            sections: {}
        };
        
        Object.keys(sections).forEach(sectionName => {
            stats.sections[sectionName] = sections[sectionName].length;
        });
        
        return stats;
    }
}

// 初始化内容管理器
const contentManager = new ContentManager();