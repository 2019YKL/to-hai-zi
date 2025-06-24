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
        // 尝试从桌面端或移动端搜索框获取查询内容
        const searchInput = document.getElementById('search-input');
        const mobileSearchInput = document.getElementById('mobile-search-input');
        
        let query = '';
        if (searchInput && searchInput.value.trim()) {
            query = searchInput.value.trim();
        } else if (mobileSearchInput && mobileSearchInput.value.trim()) {
            query = mobileSearchInput.value.trim();
            // 同步到桌面端搜索框
            if (searchInput) {
                searchInput.value = query;
            }
        }

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
        const footer = document.querySelector('footer');

        // 检测是否为移动端
        const isMobile = window.innerWidth < 768;
        
        if (isMobile) {
            // 移动端直接跳转到搜索结果页面
            this.redirectToSearchPage(query);
            return;
        }

        // 桌面端显示搜索结果（保持原有逻辑）
        // 隐藏hero区域、分页、加载状态和页脚
        if (heroSection) heroSection.style.display = 'none';
        if (pagination) {
            pagination.style.display = 'none';
            pagination.classList.add('hidden');
        }
        if (loading) {
            loading.style.display = 'none';
            loading.classList.add('hidden');
        }
        if (footer) {
            footer.style.display = 'none';
        }

        // 添加返回首页按钮
        this.addHomeButton();

        if (!container) return;

        this.displayDesktopSearchResults(container, query);

        // 确保容器可见并滚动到顶部
        container.style.display = 'block';
        container.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    redirectToSearchPage(query) {
        // 检查当前URL是否已经有搜索参数，避免无限跳转
        const currentUrl = new URL(window.location.href);
        const currentSearch = currentUrl.searchParams.get('search') ? decodeURIComponent(currentUrl.searchParams.get('search')) : null;
        
        if (currentSearch === query) {
            // 如果当前页面已经是这个搜索结果页面，直接显示移动端搜索结果
            this.displayMobileSearchResults(document.getElementById('poems-container'), query);
            return;
        }
        
        // 创建搜索结果页面的URL参数
        const searchUrl = new URL(window.location.href);
        searchUrl.searchParams.set('search', encodeURIComponent(query));
        
        // 跳转到搜索结果页面
        window.location.href = searchUrl.toString();
    }
    
    displayMobileSearchResults(container, query) {
        // 隐藏hero区域、分页、加载状态和页脚
        const heroSection = document.querySelector('header');
        const pagination = document.getElementById('pagination');
        const loading = document.getElementById('loading');
        const footer = document.querySelector('footer');
        
        if (heroSection) heroSection.style.display = 'none';
        if (pagination) {
            pagination.style.display = 'none';
            pagination.classList.add('hidden');
        }
        if (loading) {
            loading.style.display = 'none';
            loading.classList.add('hidden');
        }
        if (footer) {
            footer.style.display = 'none';
        }

        // 添加返回首页按钮
        this.addHomeButton();
        
        // 移动端搜索结果页面
        container.innerHTML = `
            <div class="min-h-screen bg-gray-50">
                <!-- 移动端搜索头部 -->
                <div class="bg-white border-b border-gray-200 px-4 py-4 sticky top-0 z-10">
                    <div class="flex items-center justify-between mb-3">
                        <h1 class="text-lg font-bold text-gray-900 poem-font">搜索结果</h1>
                        <button onclick="window.poemSearcher.clearSearch()" class="text-blue-600 text-sm font-medium">
                            返回首页
                        </button>
                    </div>
                    <div class="text-sm text-gray-600">
                        关键词: <span class="font-medium">"${query}"</span> · 
                        找到 <span class="font-medium text-blue-600">${this.searchResults.length}</span> 首诗歌
                    </div>
                </div>
                
                <!-- 搜索结果表格区域 -->
                <div class="px-4 py-2">
                    ${this.searchResults.length === 0 ? this.createMobileNoResults() : this.createMobileSearchTable(query)}
                </div>
            </div>
        `;
        
        // 确保容器可见并滚动到顶部
        container.style.display = 'block';
        container.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    createMobileSearchTable(query) {
        let tableHTML = '';
        
        this.searchResults.forEach((poem, index) => {
            const highlightedTitle = this.highlightSearchTerm(poem.title, query);
            
            // 匹配类型标识
            let matchBadges = '';
            if (poem.matchInfo) {
                if (poem.matchInfo.titleMatch) {
                    matchBadges += '<span class="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs mr-1">标题</span>';
                }
                if (poem.matchInfo.contentMatch) {
                    matchBadges += '<span class="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs mr-1">内容</span>';
                }
                if (poem.matchInfo.sectionMatch) {
                    matchBadges += '<span class="px-2 py-1 bg-purple-100 text-purple-700 rounded-full text-xs mr-1">章节</span>';
                }
            }
            
            tableHTML += `
                <div class="rounded-lg mb-3 shadow-sm border border-gray-100 overflow-hidden" style="background-color: #F7FBFC;">
                    <div class="p-4 cursor-pointer hover:bg-gray-50 transition-colors" 
                         onclick="window.location.href='${this.getPoemUrl(poem)}'">
                        <div class="flex items-center space-x-3">
                            <img src="${poem.image}" alt="${poem.title}" class="w-12 h-12 object-cover rounded flex-shrink-0">
                            <div class="flex-1 min-w-0">
                                <h3 class="font-bold text-gray-900 poem-font text-base leading-tight mb-2">
                                    ${highlightedTitle}
                                </h3>
                                <div class="flex items-center text-sm text-gray-500 mb-2">
                                    <span>${poem.section}</span>
                                </div>
                                ${matchBadges ? `<div class="flex flex-wrap gap-1">${matchBadges}</div>` : ''}
                            </div>
                            <svg class="w-6 h-6 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                            </svg>
                        </div>
                    </div>
                </div>
            `;
        });
        
        return tableHTML;
    }
    
    createMobileNoResults() {
        return `
            <div class="text-center py-20">
                <div class="poem-font text-xl text-gray-500 mb-4 leading-relaxed">
                    "远方除了遥远<br>一无所有"
                </div>
                <div class="w-16 h-px bg-gray-300 mx-auto mb-4"></div>
                <p class="text-gray-500 text-sm mb-2">没有找到相关的诗歌内容</p>
                <button onclick="window.poemSearcher.clearSearch()" 
                        class="text-blue-600 text-sm font-medium underline">
                    浏览所有诗歌
                </button>
            </div>
        `;
    }
    
    getPoemUrl(poem) {
        if (typeof contentManager !== 'undefined') {
            return contentManager.getPoemUrl(poem);
        }
        return `poem.html?poem=${encodeURIComponent(poem.path)}`;
    }
    
    displayDesktopSearchResults(container, query) {
        // 桌面端搜索结果布局（保持原有逻辑）
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
                <div id="search-results-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4 lg:gap-5" style="grid-auto-rows: 320px;">
                    <!-- 搜索结果卡片将在这里生成 -->
                </div>
            </div>
        `;

        const searchGrid = container.querySelector('#search-results-grid');
        
        if (this.searchResults.length === 0) {
            // 没有结果时，重写整个容器，不显示搜索结果标题
            container.innerHTML = `
                <div class="max-w-6xl mx-auto px-8 py-8">
                    <!-- 搜索结果网格 -->
                    <div id="search-results-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4 lg:gap-5" style="grid-auto-rows: 320px;">
                        <!-- 搜索结果卡片将在这里生成 -->
                    </div>
                </div>
            `;
            
            const searchGrid = container.querySelector('#search-results-grid');
            this.displayNoResults(searchGrid);
        } else {
            // 显示搜索结果
            this.searchResults.forEach((poem, index) => {
                const poemCard = this.createPoemCard(poem, index, query);
                searchGrid.appendChild(poemCard);
            });
        }
    }

    displaySearchResultsInPanel(query) {
        const searchResults = document.getElementById('search-results');
        if (!searchResults) return;

        searchResults.classList.remove('hidden');
        const resultsContainer = searchResults.querySelector('div');
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
        noResults.className = 'col-span-full';
        noResults.style.position = 'fixed';
        noResults.style.top = '0';
        noResults.style.left = '0';
        noResults.style.width = '100vw';
        noResults.style.height = '100vh';
        noResults.style.display = 'flex';
        noResults.style.alignItems = 'center';
        noResults.style.justifyContent = 'center';
        noResults.style.transform = 'translateY(-5vh)';
        noResults.style.zIndex = '10';
        noResults.innerHTML = `
            <div class="text-center max-w-4xl px-8">
                <div class="poem-font text-3xl md:text-4xl lg:text-5xl xl:text-6xl text-gray-600 leading-relaxed tracking-wide opacity-80 font-light">
                    "远方除了遥远<br>一无所有"
                </div>
                <div class="w-32 h-px bg-gradient-to-r from-transparent via-gray-300 to-transparent mx-auto mt-8"></div>
                <p class="text-lg text-gray-500 poem-font font-light mt-6">
                    没有找到相关的诗歌内容
                </p>
                <p class="text-sm text-gray-400 font-light mt-2">
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

        // 添加匹配标识
        let matchBadges = '';
        if (poem.matchInfo.titleMatch) {
            matchBadges += '<span class="inline-block bg-blue-100 text-blue-800 text-xs px-1 py-0.5 rounded mr-1">标题</span>';
        }
        if (poem.matchInfo.contentMatch) {
            matchBadges += '<span class="inline-block bg-green-100 text-green-800 text-xs px-1 py-0.5 rounded mr-1">内容</span>';
        }
        if (poem.matchInfo.sectionMatch) {
            matchBadges += '<span class="inline-block bg-purple-100 text-purple-800 text-xs px-1 py-0.5 rounded mr-1">章节</span>';
        }

        item.innerHTML = `
            <div class="flex items-center space-x-3">
                <img src="${poem.image}" alt="${poem.title}" class="w-12 h-12 object-cover rounded flex-shrink-0">
                <div class="flex-1 min-w-0">
                    <h4 class="font-medium text-gray-900 poem-font mb-1 text-base">
                        ${highlightedTitle}
                    </h4>
                    <div class="flex items-center space-x-2">
                        <span class="text-sm text-gray-500">${poem.section}</span>
                        ${matchBadges ? matchBadges : ''}
                    </div>
                </div>
                <svg class="w-5 h-5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
            </div>
        `;

        return item;
    }


    createPoemCard(poem, index, query) {
        const article = document.createElement('article');
        article.className = `poem-card rounded-xl overflow-hidden shadow-lg hover:shadow-2xl cursor-pointer group h-full`;
        article.onclick = () => {
            if (typeof contentManager !== 'undefined') {
                window.location.href = contentManager.getPoemUrl(poem);
            } else {
                window.location.href = `poem.html?poem=${encodeURIComponent(poem.path)}`;
            }
        };

        // 简化的卡片结构，图片占满整个卡片
        article.innerHTML = `
            <div class="relative overflow-hidden h-full">
                <!-- 图片占满整个卡片 -->
                <div class="h-full relative group-hover:scale-102 transition-transform duration-700 overflow-hidden">
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
            </div>
        `;

        return article;
    }


    createMatchBadges(matchInfo) {
        if (!matchInfo) return '';
        
        let badges = '<div class="flex flex-wrap gap-1">';
        if (matchInfo.titleMatch) {
            badges += '<span class="inline-block bg-white/80 text-gray-700 text-xs px-2 py-1 rounded-full backdrop-blur-md border border-white/40 shadow-sm font-medium">标题匹配</span>';
        }
        if (matchInfo.contentMatch) {
            badges += '<span class="inline-block bg-white/80 text-gray-700 text-xs px-2 py-1 rounded-full backdrop-blur-md border border-white/40 shadow-sm font-medium">内容匹配</span>';
        }
        if (matchInfo.sectionMatch) {
            badges += '<span class="inline-block bg-white/80 text-gray-700 text-xs px-2 py-1 rounded-full backdrop-blur-md border border-white/40 shadow-sm font-medium">章节匹配</span>';
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
        if (!title) return title;
        
        // 如果标题超长（超过12个字符），进行智能缩短
        if (title.length > 12) {
            // 寻找合适的分割点（如破折号、空格等）
            const breakPoints = ['——', '—', '·', ' ', '：', ':'];
            for (const bp of breakPoints) {
                const index = title.indexOf(bp);
                if (index > 2 && index < 8) {
                    const firstPart = title.substring(0, index);
                    const secondPart = title.substring(index + bp.length);
                    // 如果第二部分仍然太长，截断并加省略号
                    if (secondPart.length > 8) {
                        return `${firstPart}<br>${secondPart.substring(0, 6)}…`;
                    }
                    return `${firstPart}<br>${secondPart}`;
                }
            }
            // 没找到合适分割点，直接截断
            return title.substring(0, 10) + '…';
        }
        
        // 标题适中长度（7-12字符），简单换行
        if (title.length > 6) {
            const firstPart = title.substring(0, 4);
            const secondPart = title.substring(4);
            return `${firstPart}<br>${secondPart}`;
        }
        
        // 短标题直接显示
        return title;
    }


    addHomeButton() {
        // 检查是否已经存在返回按钮
        if (document.getElementById('search-home-btn')) return;
        
        // 创建返回首页按钮
        const homeButton = document.createElement('div');
        homeButton.id = 'search-home-btn';
        homeButton.className = 'fixed top-6 left-6 z-20';
        homeButton.innerHTML = `
            <button onclick="window.poemSearcher.clearSearch()" class="bg-white/80 px-4 py-3 rounded-full text-gray-700 hover:text-gray-900 transition-all duration-300 hover:shadow-lg flex items-center">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
                </svg>
            </button>
        `;
        document.body.appendChild(homeButton);
    }

    removeHomeButton() {
        const homeButton = document.getElementById('search-home-btn');
        if (homeButton) {
            homeButton.remove();
        }
    }

    clearSearch() {
        const searchInput = document.getElementById('search-input');
        const mobileSearchInput = document.getElementById('mobile-search-input');
        const clearBtn = document.getElementById('clear-search');
        const mobileClearBtn = document.getElementById('mobile-clear-search');
        const pagination = document.getElementById('pagination');
        const searchResults = document.getElementById('search-results');
        const heroSection = document.querySelector('header');

        // 清空搜索框
        if (searchInput) {
            searchInput.value = '';
        }
        if (mobileSearchInput) {
            mobileSearchInput.value = '';
        }

        // 隐藏清空按钮
        if (clearBtn) {
            clearBtn.style.display = 'none';
        }
        if (mobileClearBtn) {
            mobileClearBtn.classList.add('hidden');
        }

        // 重置状态
        this.searchResults = [];
        this.isSearchMode = false;

        // 移除返回首页按钮
        this.removeHomeButton();

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
            
            // 恢复页脚显示
            const footer = document.querySelector('footer');
            if (footer) {
                footer.style.display = '';
            }
            
            // 恢复原始的诗歌容器结构
            const container = document.getElementById('poems-container');
            if (container) {
                container.innerHTML = `
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-4 lg:gap-5" style="grid-auto-rows: 480px;">
                        <!-- 诗歌卡片将通过 JavaScript 动态生成 -->
                    </div>
                `;
                container.classList.remove('hidden');
                // 恢复原始容器样式
                container.className = 'max-w-6xl mx-auto px-4 md:px-8 py-2 md:py-4 hidden';
            }
            
            if (typeof window.poemPage !== 'undefined') {
                window.poemPage.renderCurrentPage();
                window.poemPage.hideLoading();
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

// 初始化搜索功能
if (typeof window !== 'undefined') {
    // 立即创建全局搜索实例
    window.poemSearcher = new PoemSearcher();
}