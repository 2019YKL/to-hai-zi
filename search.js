class PoemSearcher {
    constructor() {
        this.poems = [];
        this.searchResults = [];
        this.isSearchMode = false;
        this.init();
    }

    async init() {
        // 等待诗歌数据加载
        if (typeof poemsData !== 'undefined') {
            this.poems = poemsData;
        } else {
            // 等待数据加载
            const checkData = setInterval(() => {
                if (typeof poemsData !== 'undefined') {
                    this.poems = poemsData;
                    clearInterval(checkData);
                }
            }, 100);
        }
        this.setupSearchEvents();
    }

    setupSearchEvents() {
        const searchInput = document.getElementById('search-input');
        const searchBtn = document.getElementById('search-btn');
        const clearBtn = document.getElementById('clear-search');

        if (searchInput && searchBtn) {
            // 搜索按钮点击
            searchBtn.addEventListener('click', () => {
                this.performSearch();
            });

            // 回车搜索
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.performSearch();
                }
            });

            // 清空搜索
            if (clearBtn) {
                clearBtn.addEventListener('click', () => {
                    this.clearSearch();
                });
            }

            // 实时搜索（可选）
            searchInput.addEventListener('input', (e) => {
                if (e.target.value.trim() === '') {
                    this.clearSearch();
                }
            });
        }
    }

    performSearch() {
        const searchInput = document.getElementById('search-input');
        const query = searchInput.value.trim();

        if (!query) {
            this.clearSearch();
            return;
        }

        console.log(`搜索: "${query}"`);
        
        // 执行搜索
        this.searchResults = this.searchPoems(query);
        this.isSearchMode = true;
        
        // 显示搜索结果
        this.displaySearchResults(query);
        
        // 显示清空按钮
        const clearBtn = document.getElementById('clear-search');
        if (clearBtn) {
            clearBtn.style.display = 'block';
        }
    }

    searchPoems(query) {
        const results = [];
        const queryLower = query.toLowerCase();

        this.poems.forEach(poem => {
            let score = 0;
            let matchInfo = {
                titleMatch: false,
                contentMatch: false,
                sectionMatch: false
            };

            // 标题匹配（权重最高）
            if (poem.title.toLowerCase().includes(queryLower)) {
                score += 100;
                matchInfo.titleMatch = true;
            }

            // 正文内容匹配
            if (poem.full_content && poem.full_content.toLowerCase().includes(queryLower)) {
                score += 50;
                matchInfo.contentMatch = true;
            }

            // 章节匹配
            if (poem.section && poem.section.toLowerCase().includes(queryLower)) {
                score += 30;
                matchInfo.sectionMatch = true;
            }

            // 预览内容匹配
            if (poem.preview && poem.preview.toLowerCase().includes(queryLower)) {
                score += 25;
            }

            // 如果有匹配，添加到结果中
            if (score > 0) {
                results.push({
                    ...poem,
                    score,
                    matchInfo
                });
            }
        });

        // 按评分排序
        return results.sort((a, b) => b.score - a.score);
    }

    displaySearchResults(query) {
        // 检查是否在诗歌详情页
        const isInPoemPage = window.location.pathname.includes('poem.html');
        
        if (isInPoemPage) {
            this.displaySearchResultsInPanel(query);
        } else {
            this.displaySearchResultsInMain(query);
        }
    }

    displaySearchResultsInMain(query) {
        const container = document.getElementById('poems-container');
        const pagination = document.getElementById('pagination');
        const loading = document.getElementById('loading');
        const heroSection = document.querySelector('header');

        // 隐藏hero区域、分页和加载状态
        if (heroSection) heroSection.style.display = 'none';
        if (pagination) {
            pagination.style.display = 'none';
            pagination.classList.add('hidden');
        }
        if (loading) {
            loading.style.display = 'none';
            loading.classList.add('hidden');
        }

        if (!container) return;

        // 重写整个容器内容
        container.innerHTML = `
            <div class="max-w-6xl mx-auto px-8 py-8">
                <!-- 搜索结果标题 -->
                <div class="text-center mb-8">
                    <h2 class="text-2xl md:text-3xl font-bold text-gray-800 mb-3 poem-font">
                        搜索结果
                    </h2>
                    <div class="flex justify-center mb-4">
                        <div class="w-24 h-px bg-gradient-to-r from-transparent via-gray-400 to-transparent"></div>
                    </div>
                    <p class="text-lg text-gray-600 poem-font font-light">
                        关键词 "<span class="font-medium text-gray-800">${query}</span>" · 找到 <span class="font-medium text-gray-800">${this.searchResults.length}</span> 首相关诗歌
                    </p>
                </div>
                
                <!-- 搜索结果网格 -->
                <div id="search-results-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4 lg:gap-5" style="grid-auto-rows: 480px;">
                    <!-- 搜索结果卡片将在这里生成 -->
                </div>
            </div>
        `;

        const searchGrid = container.querySelector('#search-results-grid');
        
        if (this.searchResults.length === 0) {
            // 没有结果时显示海子的诗句
            this.displayNoResults(searchGrid);
        } else {
            // 显示搜索结果
            this.searchResults.forEach((poem, index) => {
                const poemCard = this.createPoemCard(poem, index, query);
                searchGrid.appendChild(poemCard);
            });
        }

        // 确保容器可见并滚动到顶部
        container.style.display = 'block';
        container.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    displaySearchResultsInPanel(query) {
        const searchResults = document.getElementById('search-results');
        if (!searchResults) return;

        searchResults.classList.remove('hidden');
        const resultsContainer = searchResults.querySelector('.glass-bg-premium');
        if (!resultsContainer) return;

        resultsContainer.innerHTML = '';

        // 添加搜索结果标题
        const searchHeader = document.createElement('div');
        searchHeader.className = 'mb-4 text-center border-b border-gray-200 pb-3';
        searchHeader.innerHTML = `
            <h3 class="text-base font-bold text-gray-800 mb-1 poem-font">
                搜索结果：${query}
            </h3>
            <p class="text-xs text-gray-600">
                找到 ${this.searchResults.length} 首相关诗歌
            </p>
        `;
        resultsContainer.appendChild(searchHeader);

        if (this.searchResults.length === 0) {
            // 没有结果时显示海子的诗句
            this.displayNoResultsInPanel(resultsContainer);
        } else {
            // 显示搜索结果
            this.searchResults.forEach((poem, index) => {
                const poemItem = this.createSearchResultItem(poem, index, query);
                resultsContainer.appendChild(poemItem);
            });
        }
    }

    displayNoResults(container) {
        const noResults = document.createElement('div');
        noResults.className = 'col-span-full flex flex-col items-center justify-center py-16';
        noResults.innerHTML = `
            <div class="text-center max-w-4xl mx-auto">
                <div class="poem-font text-3xl md:text-4xl lg:text-5xl text-gray-600 mb-6 leading-relaxed tracking-wide opacity-80">
                    "远方除了遥远一无所有"
                </div>
                <div class="w-32 h-px bg-gradient-to-r from-transparent via-gray-300 to-transparent mx-auto mb-6"></div>
                <p class="text-lg text-gray-500 poem-font font-light mb-4">
                    没有找到相关的诗歌内容
                </p>
                <p class="text-sm text-gray-400 font-light">
                    尝试使用其他关键词，或浏览<a href="#" onclick="window.poemSearcher.clearSearch()" class="text-blue-500 hover:text-blue-700 underline">所有诗歌</a>
                </p>
            </div>
        `;
        container.appendChild(noResults);
    }

    displayNoResultsInPanel(container) {
        const noResults = document.createElement('div');
        noResults.className = 'flex flex-col items-center justify-center py-12';
        noResults.innerHTML = `
            <div class="text-center">
                <div class="poem-font text-xl text-gray-600 mb-4 leading-relaxed opacity-80">
                    "远方除了遥远一无所有"
                </div>
                <div class="w-16 h-px bg-gradient-to-r from-transparent via-gray-300 to-transparent mx-auto mb-4"></div>
                <p class="text-sm text-gray-500 poem-font font-light">
                    没有找到相关的诗歌内容
                </p>
            </div>
        `;
        container.appendChild(noResults);
    }

    createSearchResultItem(poem, index, query) {
        const item = document.createElement('div');
        item.className = 'border-b border-gray-100 pb-2 mb-2 last:border-b-0 last:mb-0 cursor-pointer hover:bg-gray-50 rounded p-2 transition-colors';
        item.onclick = () => {
            if (typeof contentManager !== 'undefined') {
                window.location.href = contentManager.getPoemUrl(poem);
            } else {
                window.location.href = `poem.html?poem=${encodeURIComponent(poem.path)}`;
            }
        };

        // 高亮搜索词
        const highlightedTitle = this.highlightSearchTerm(poem.title, query);
        const highlightedPreview = this.highlightSearchTerm(poem.preview || '', query);

        // 添加匹配标识
        let matchBadges = '';
        if (poem.matchInfo.titleMatch) {
            matchBadges += '<span class="inline-block bg-blue-100 text-blue-800 text-xs px-1 py-0.5 rounded mr-1">标题</span>';
        }
        if (poem.matchInfo.contentMatch) {
            matchBadges += '<span class="inline-block bg-green-100 text-green-800 text-xs px-1 py-0.5 rounded mr-1">内容</span>';
        }

        item.innerHTML = `
            <div class="flex items-start space-x-2">
                <img src="${poem.image}" alt="${poem.title}" class="w-10 h-10 object-cover rounded flex-shrink-0">
                <div class="flex-1 min-w-0">
                    <h4 class="font-medium text-gray-900 poem-font mb-1 text-sm truncate">
                        ${highlightedTitle}
                    </h4>
                    ${matchBadges ? `<div class="mb-1">${matchBadges}</div>` : ''}
                    <p class="text-xs text-gray-600 poem-font leading-relaxed line-clamp-2">
                        ${this.getFirstTwoLines(highlightedPreview)}
                    </p>
                </div>
            </div>
        `;

        return item;
    }

    getFirstTwoLines(text) {
        if (!text) return '';
        
        // 按换行符分割，取前两行
        const lines = text.split('\n').filter(line => line.trim());
        return lines.slice(0, 2).join(' ');
    }

    createPoemCard(poem, index, query) {
        const article = document.createElement('article');
        article.className = `poem-card glass-bg-premium rounded-xl overflow-hidden shadow-lg hover:shadow-2xl cursor-pointer group h-full`;
        article.onclick = () => {
            if (typeof contentManager !== 'undefined') {
                window.location.href = contentManager.getPoemUrl(poem);
            } else {
                window.location.href = `poem.html?poem=${encodeURIComponent(poem.path)}`;
            }
        };

        // 完全复制首页的卡片HTML结构
        article.innerHTML = `
            <div class="relative overflow-hidden flex flex-col h-full">
                <!-- 精美的图片区域 -->
                <div class="h-48 relative group-hover:scale-105 transition-transform duration-700 overflow-hidden">
                    <img src="${poem.image}" 
                         alt="${poem.title}" 
                         class="w-full h-full object-cover">
                    <div class="absolute inset-0 bg-black/40"></div>
                    
                    <!-- 匹配标识 -->
                    <div class="absolute top-3 right-3 z-10">
                        ${this.createMatchBadges(poem.matchInfo)}
                    </div>
                    
                    <!-- 标题区域 -->
                    <div class="absolute inset-0 flex items-center justify-center text-center text-white">
                        <div>
                            <h3 class="text-3xl md:text-4xl font-bold mb-4 tracking-tight poem-font drop-shadow-2xl" title="${poem.title}">
                                ${this.highlightSearchTerm(this.formatTitle(poem.title), query)}
                            </h3>
                            
                            <div class="flex justify-center mb-4">
                                <div class="w-16 h-px bg-white/80"></div>
                            </div>
                            
                            <p class="text-lg font-medium opacity-90 drop-shadow">${poem.section}</p>
                        </div>
                    </div>
                </div>
                
                <!-- 内容区域 - 使用flex-1使其填充剩余空间 -->
                <div class="px-5 pt-3 pb-5 flex-1 flex flex-col min-h-0">
                    <!-- 诗歌预览 - 设置固定高度区域 -->
                    <div class="poem-preview rounded-lg p-4 pt-2 mb-3 flex-1 flex items-start overflow-hidden" style="max-height: 180px;">
                        <div class="text-gray-700 leading-relaxed poem-font text-lg font-light whitespace-pre-line overflow-hidden line-clamp-4">
                            ${this.highlightSearchTerm(this.getFirstFourLines(poem.preview), query)}
                        </div>
                    </div>
                    
                    <!-- 底部信息 - 固定在底部 -->
                    <div class="flex justify-end items-center mt-auto pt-2 border-t border-gray-100">
                        <div class="inline-flex items-center text-gray-700 group-hover:text-gray-900 transition-colors font-medium">
                            <span class="mr-2">阅读全文</span>
                            <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
                            </svg>
                        </div>
                    </div>
                </div>
            </div>
        `;

        return article;
    }


    createMatchBadges(matchInfo) {
        if (!matchInfo) return '';
        
        let badges = '<div class="flex flex-wrap gap-1">';
        if (matchInfo.titleMatch) {
            badges += '<span class="inline-block bg-blue-500/80 text-white text-xs px-2 py-1 rounded-full backdrop-blur-sm border border-white/20 shadow-sm">标题</span>';
        }
        if (matchInfo.contentMatch) {
            badges += '<span class="inline-block bg-green-500/80 text-white text-xs px-2 py-1 rounded-full backdrop-blur-sm border border-white/20 shadow-sm">内容</span>';
        }
        if (matchInfo.sectionMatch) {
            badges += '<span class="inline-block bg-purple-500/80 text-white text-xs px-2 py-1 rounded-full backdrop-blur-sm border border-white/20 shadow-sm">章节</span>';
        }
        badges += '</div>';
        
        return badges;
    }

    highlightSearchTerm(text, query) {
        if (!text || !query) return text;
        
        // 转义正则表达式特殊字符
        const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(`(${escapedQuery})`, 'gi');
        return text.replace(regex, '<mark class="bg-yellow-300/80 text-yellow-900 rounded px-1 font-medium">$1</mark>');
    }

    formatTitle(title) {
        if (!title || title.length <= 6) return title;
        
        // 如果标题超过6个字，在第4个字后插入换行
        const firstPart = title.substring(0, 4);
        const secondPart = title.substring(4);
        return `${firstPart}<br>${secondPart}`;
    }

    getFirstFourLines(text) {
        if (!text) return '';
        
        // 按换行符分割，过滤空行
        const lines = text.split('\n').filter(line => line.trim());
        
        // 对于很长的第一行（可能是散文），进一步截断
        const processedLines = lines.map(line => {
            if (line.length > 50) {
                return line.substring(0, 50) + '...';
            }
            return line;
        });
        
        // 取前四行
        let result = processedLines.slice(0, 4).join('\n');
        
        // 最终长度限制
        if (result.length > 180) {
            result = result.substring(0, 180) + '...';
        }
        
        return result;
    }

    clearSearch() {
        const searchInput = document.getElementById('search-input');
        const clearBtn = document.getElementById('clear-search');
        const pagination = document.getElementById('pagination');
        const searchResults = document.getElementById('search-results');
        const heroSection = document.querySelector('header');

        // 清空搜索框
        if (searchInput) {
            searchInput.value = '';
        }

        // 隐藏清空按钮
        if (clearBtn) {
            clearBtn.style.display = 'none';
        }

        // 重置状态
        this.searchResults = [];
        this.isSearchMode = false;

        // 检查是否在诗歌详情页
        const isInPoemPage = window.location.pathname.includes('poem.html');
        
        if (isInPoemPage) {
            // 在诗歌详情页，隐藏搜索结果面板
            if (searchResults) {
                searchResults.classList.add('hidden');
            }
        } else {
            // 在首页，恢复正常显示
            if (heroSection) {
                heroSection.style.display = '';
            }
            
            // 恢复原始的诗歌容器结构
            const container = document.getElementById('poems-container');
            if (container) {
                container.innerHTML = `
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4 lg:gap-5 auto-rows-fr">
                        <!-- 诗歌卡片将通过 JavaScript 动态生成 -->
                    </div>
                `;
                container.classList.remove('hidden');
            }
            
            if (typeof window.poemPage !== 'undefined') {
                window.poemPage.renderCurrentPage();
            }

            // 显示分页
            if (pagination) {
                pagination.style.display = '';
                pagination.classList.remove('hidden');
            }
        }

        console.log('已清空搜索');
    }
}

// 全局搜索实例
window.poemSearcher = null;

// 初始化搜索功能
document.addEventListener('DOMContentLoaded', () => {
    window.poemSearcher = new PoemSearcher();
});