// Content Management System for Haizi Poetry
class ContentManager {
    constructor() {
        this.poems = [];
        this.currentPage = 1;
        this.poemsPerPage = 6;
    }

    // Parse markdown front matter
    parseMarkdown(content) {
        const frontMatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/;
        const match = content.match(frontMatterRegex);
        
        if (!match) {
            throw new Error('Invalid markdown format');
        }

        const frontMatter = this.parseFrontMatter(match[1]);
        const body = match[2].trim();
        
        return {
            ...frontMatter,
            content: body
        };
    }

    // Parse YAML front matter
    parseFrontMatter(yamlText) {
        const result = {};
        const lines = yamlText.split('\n');
        
        for (let line of lines) {
            line = line.trim();
            if (!line || line.startsWith('#')) continue;
            
            const colonIndex = line.indexOf(':');
            if (colonIndex === -1) continue;
            
            const key = line.substring(0, colonIndex).trim();
            let value = line.substring(colonIndex + 1).trim();
            
            // Remove quotes
            if ((value.startsWith('"') && value.endsWith('"')) || 
                (value.startsWith("'") && value.endsWith("'"))) {
                value = value.slice(1, -1);
            }
            
            // Handle multiline values (preview)
            if (value === '|') {
                const nextLines = [];
                let i = lines.indexOf(line) + 1;
                while (i < lines.length && lines[i].startsWith('  ')) {
                    nextLines.push(lines[i].substring(2));
                    i++;
                }
                value = nextLines.join('\n');
            }
            
            // Convert numeric values
            if (!isNaN(value) && value !== '') {
                value = parseInt(value);
            }
            
            result[key] = value;
        }
        
        return result;
    }

    // Load poems from embedded data
    async loadPoems() {
        // 检查是否有外部诗歌数据
        if (typeof poemsData !== 'undefined') {
            this.poems = [...poemsData];
        } else {
            // 回退方案：尝试从 content 目录加载
            await this.loadPoemsFromFiles();
        }
        
        // Sort by order
        this.poems.sort((a, b) => (a.order || 0) - (b.order || 0));
        
        return this.poems;
    }

    // 从文件加载的回退方案
    async loadPoemsFromFiles() {
        const poemFiles = [
            'facing-sea', 'spring', 'answer', 'diary', 
            'wheat', 'village', 'horse', 'autumn', 
            'motherland', 'night-poem', 'september', 'asian-copper',
            'rebuild-home', 'four-sisters', 'history'
        ];
        
        this.poems = [];
        
        for (const file of poemFiles) {
            try {
                const response = await fetch(`content/poems/${file}.md`);
                if (response.ok) {
                    const content = await response.text();
                    const poem = this.parseMarkdown(content);
                    this.poems.push(poem);
                }
            } catch (error) {
                console.error(`Error loading ${file}.md:`, error);
            }
        }
    }

    // Get poems for current page
    getCurrentPagePoems() {
        const startIndex = (this.currentPage - 1) * this.poemsPerPage;
        const endIndex = startIndex + this.poemsPerPage;
        return this.poems.slice(startIndex, endIndex);
    }

    // Get total pages
    getTotalPages() {
        return Math.ceil(this.poems.length / this.poemsPerPage);
    }

    // Set current page
    setCurrentPage(page) {
        const totalPages = this.getTotalPages();
        if (page >= 1 && page <= totalPages) {
            this.currentPage = page;
            return true;
        }
        return false;
    }

    // Get poem by slug
    getPoemBySlug(slug) {
        return this.poems.find(poem => poem.slug === slug);
    }

    // Get next/previous poem for navigation
    getAdjacentPoems(slug) {
        const currentIndex = this.poems.findIndex(poem => poem.slug === slug);
        return {
            previous: currentIndex > 0 ? this.poems[currentIndex - 1] : null,
            next: currentIndex < this.poems.length - 1 ? this.poems[currentIndex + 1] : null
        };
    }
}

// Initialize content manager
const contentManager = new ContentManager();