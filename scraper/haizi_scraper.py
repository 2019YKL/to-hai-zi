import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin
import json

class HaiziScraper:
    def __init__(self, base_url="https://haizi.huhaitai.com/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.data = {
            'sections': [],
            'poems': []
        }
    
    def get_page(self, url):
        """获取页面内容"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_poem_links(self, soup):
        """从主页提取所有诗歌链接"""
        links = []
        # 查找所有诗歌链接
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and ('/' in href and not href.startswith('http')):
                full_url = urljoin(self.base_url, href)
                title = link.get_text().strip()
                if title and title not in ['扉　页：海子简历与照片', '骆一禾：海子生涯', '西　川：怀念']:
                    links.append({
                        'title': title,
                        'url': full_url,
                        'path': href
                    })
        return links
    
    def extract_poem_content(self, url, title):
        """提取单首诗的内容"""
        soup = self.get_page(url)
        if not soup:
            return None
        
        # 尝试多种方式提取诗歌内容
        content = ""
        
        # 方法1: 查找包含诗歌内容的主要区域
        main_content = soup.find('div', class_='content') or soup.find('div', id='content')
        if main_content:
            content = main_content.get_text(separator='\n').strip()
        else:
            # 方法2: 查找body中的文本内容，排除导航等
            body = soup.find('body')
            if body:
                # 移除script和style标签
                for tag in body(['script', 'style', 'nav', 'header', 'footer']):
                    tag.decompose()
                content = body.get_text(separator='\n').strip()
        
        # 清理内容
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        # 过滤掉导航和目录相关的行
        filtered_lines = []
        skip_keywords = ['目录', '第一编', '第二编', '第三编', '上一页', '下一页', '返回']
        
        for line in lines:
            if not any(keyword in line for keyword in skip_keywords) and len(line) > 1:
                filtered_lines.append(line)
        
        return '\n'.join(filtered_lines) if filtered_lines else None
    
    def scrape_all_poems(self):
        """爬取所有诗歌"""
        print("开始爬取海子诗集...")
        
        # 获取主页
        main_soup = self.get_page(self.base_url)
        if not main_soup:
            print("无法获取主页")
            return
        
        # 提取所有诗歌链接
        poem_links = self.extract_poem_links(main_soup)
        print(f"找到 {len(poem_links)} 首诗歌")
        
        # 按类别组织
        sections = {
            '扉页': [],
            '第一编　短诗（1983—1986）': [],
            '第二编长诗（1984—1985）': [],  
            '第三编短诗（1987—1989）': []
        }
        
        current_section = '扉页'
        
        for i, poem in enumerate(poem_links):
            print(f"正在处理: {poem['title']} ({i+1}/{len(poem_links)})")
            
            # 判断章节
            if '第一编' in poem['title'] or poem['path'].startswith('/01/'):
                current_section = '第一编　短诗（1983—1986）'
            elif '第二编' in poem['title'] or poem['path'].startswith('/02/'):
                current_section = '第二编长诗（1984—1985）'
            elif '第三编' in poem['title'] or poem['path'].startswith('/03/'):
                current_section = '第三编短诗（1987—1989）'
            elif poem['path'].startswith('/f'):
                current_section = '扉页'
            
            # 提取诗歌内容
            content = self.extract_poem_content(poem['url'], poem['title'])
            
            poem_data = {
                'title': poem['title'],
                'url': poem['url'],
                'path': poem['path'],
                'content': content,
                'section': current_section
            }
            
            sections[current_section].append(poem_data)
            self.data['poems'].append(poem_data)
            
            # 添加延迟避免过于频繁请求
            time.sleep(0.5)
        
        self.data['sections'] = sections
        print("爬取完成!")
        return self.data
    
    def save_to_markdown(self, filename="haizi_poems.md"):
        """保存为Markdown格式"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# 海子诗集\n\n")
            f.write("本诗集内容来源于 https://haizi.huhaitai.com/\n\n")
            
            # 按章节组织
            for section_name, poems in self.data['sections'].items():
                if poems:  # 只有当章节有内容时才写入
                    f.write(f"## {section_name}\n\n")
                    
                    for poem in poems:
                        f.write(f"### {poem['title']}\n\n")
                        if poem['content']:
                            # 格式化诗歌内容
                            content = poem['content']
                            # 简单格式化，将短行识别为诗句
                            lines = content.split('\n')
                            formatted_lines = []
                            for line in lines:
                                if line.strip():
                                    # 如果行很短，可能是诗句，添加适当格式
                                    if len(line) < 50 and not line.endswith('。') and not line.endswith('：'):
                                        formatted_lines.append(f"    {line}")
                                    else:
                                        formatted_lines.append(line)
                            
                            f.write('\n'.join(formatted_lines))
                        else:
                            f.write("*内容获取失败*")
                        
                        f.write(f"\n\n*原文链接: {poem['url']}*\n\n")
                        f.write("---\n\n")
        
        print(f"已保存到 {filename}")
    
    def save_raw_data(self, filename="haizi_raw_data.json"):
        """保存原始数据为JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"原始数据已保存到 {filename}")

if __name__ == "__main__":
    scraper = HaiziScraper()
    data = scraper.scrape_all_poems()
    scraper.save_to_markdown()
    scraper.save_raw_data()