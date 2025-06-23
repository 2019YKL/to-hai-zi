import requests
from bs4 import BeautifulSoup
import time
import re
import os
from urllib.parse import urljoin
import json
from pathlib import Path

class HaiziFullScraper:
    def __init__(self, base_url="https://haizi.huhaitai.com/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # 创建输出目录结构
        self.output_dir = Path("../assets/content/poems")
        self.sections = {
            'preface': self.output_dir / '00-preface',
            'part1': self.output_dir / '01-short-poems-1983-1986', 
            'part2': self.output_dir / '02-long-poems-1984-1985',
            'part3': self.output_dir / '03-short-poems-1987-1989'
        }
        
        # 创建目录
        for section_dir in self.sections.values():
            section_dir.mkdir(parents=True, exist_ok=True)
        
        self.scraped_poems = []
        self.failed_poems = []
    
    def get_page(self, url):
        """获取页面内容"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"❌ 获取页面失败 {url}: {e}")
            return None
    
    def extract_all_poem_links(self):
        """从主页提取所有诗歌链接"""
        print("📖 正在获取所有诗歌链接...")
        soup = self.get_page(self.base_url)
        if not soup:
            return []
        
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            title = link.get_text().strip()
            
            if (href and href.startswith('/') and 
                title and len(title) > 0 and
                not any(skip in title for skip in ['目录', '扉页', '骆一禾', '西川'])):
                
                full_url = urljoin(self.base_url, href)
                links.append({
                    'title': title,
                    'url': full_url,
                    'path': href,
                    'section': self.determine_section(href)
                })
        
        print(f"✅ 找到 {len(links)} 首诗歌")
        return links
    
    def determine_section(self, path):
        """根据路径确定诗歌所属章节"""
        if path.startswith('/f'):
            return 'preface'
        elif path.startswith('/01/'):
            return 'part1'
        elif path.startswith('/02/'):
            return 'part2'
        elif path.startswith('/03/'):
            return 'part3'
        else:
            return 'part1'  # 默认归类
    
    def clean_filename(self, title):
        """清理文件名，移除特殊字符"""
        # 移除或替换特殊字符
        filename = re.sub(r'[<>:"/\\|?*]', '', title)
        filename = re.sub(r'[，。：；！？（）【】《》""''、]', '', filename)
        filename = filename.replace(' ', '-').replace('　', '-')
        filename = re.sub(r'-+', '-', filename)  # 合并多个连字符
        filename = filename.strip('-')
        return filename[:50]  # 限制文件名长度
    
    def extract_poem_content(self, url, title):
        """提取单首诗的详细内容"""
        soup = self.get_page(url)
        if not soup:
            return None
        
        # 移除导航和脚本元素
        for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
            tag.decompose()
        
        # 获取主要内容
        content_text = ""
        body = soup.find('body')
        if body:
            content_text = body.get_text(separator='\n')
        
        # 清理和格式化内容
        lines = [line.strip() for line in content_text.split('\n') if line.strip()]
        
        # 过滤掉导航和无关内容
        skip_patterns = [
            r'目录', r'第[一二三]编', r'上一页', r'下一页', r'返回',
            r'haizi\.huhaitai\.com', r'^\d+$', r'^[←→]$'
        ]
        
        filtered_lines = []
        for line in lines:
            if (len(line) > 1 and 
                not any(re.search(pattern, line) for pattern in skip_patterns)):
                filtered_lines.append(line)
        
        # 提取诗歌正文（通常标题后面就是正文）
        poem_content = []
        found_title = False
        
        for line in filtered_lines:
            if title in line and not found_title:
                found_title = True
                continue
            elif found_title:
                # 如果遇到年份标记，可能是诗歌结尾
                if re.match(r'^\d{4}\.\d{1,2}$', line):
                    poem_content.append(line)
                    break
                poem_content.append(line)
        
        return '\n'.join(poem_content[:30]) if poem_content else None  # 限制长度
    
    def create_poem_markdown(self, poem_data, content):
        """创建单首诗的markdown文件"""
        section_dir = self.sections[poem_data['section']]
        filename = f"{self.clean_filename(poem_data['title'])}.md"
        filepath = section_dir / filename
        
        # 避免文件名冲突
        counter = 1
        original_filepath = filepath
        while filepath.exists():
            name_without_ext = original_filepath.stem
            filepath = section_dir / f"{name_without_ext}-{counter}.md"
            counter += 1
        
        # 创建markdown内容
        markdown_content = f"""# {poem_data['title']}

{content}

---

**原文链接**: {poem_data['url']}  
**章节**: {self.get_section_name(poem_data['section'])}  
**路径**: {poem_data['path']}
"""
        
        # 写入文件
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            return str(filepath)
        except Exception as e:
            print(f"❌ 创建文件失败 {filepath}: {e}")
            return None
    
    def get_section_name(self, section_key):
        """获取章节中文名称"""
        section_names = {
            'preface': '扉页',
            'part1': '第一编　短诗（1983—1986）',
            'part2': '第二编　长诗（1984—1985）',
            'part3': '第三编　短诗（1987—1989）'
        }
        return section_names.get(section_key, '未知章节')
    
    def scrape_all_poems(self):
        """爬取所有诗歌并生成独立文件"""
        print("🚀 开始全量爬取海子诗集...")
        
        # 获取所有诗歌链接
        poem_links = self.extract_all_poem_links()
        if not poem_links:
            print("❌ 没有找到诗歌链接")
            return
        
        total_poems = len(poem_links)
        print(f"📝 准备爬取 {total_poems} 首诗歌...")
        
        for i, poem in enumerate(poem_links, 1):
            print(f"📄 [{i:3d}/{total_poems}] 处理: {poem['title']}")
            
            # 提取诗歌内容
            content = self.extract_poem_content(poem['url'], poem['title'])
            
            if content:
                # 创建markdown文件
                filepath = self.create_poem_markdown(poem, content)
                if filepath:
                    self.scraped_poems.append({
                        'title': poem['title'],
                        'section': poem['section'],
                        'filepath': filepath,
                        'url': poem['url']
                    })
                    print(f"  ✅ 已保存: {filepath}")
                else:
                    self.failed_poems.append(poem)
                    print(f"  ❌ 保存失败: {poem['title']}")
            else:
                self.failed_poems.append(poem)
                print(f"  ❌ 内容提取失败: {poem['title']}")
            
            # 添加延迟避免过于频繁的请求
            time.sleep(0.2)
        
        self.create_summary()
        print(f"\n🎉 爬取完成！")
        print(f"✅ 成功: {len(self.scraped_poems)} 首")
        print(f"❌ 失败: {len(self.failed_poems)} 首")
    
    def create_summary(self):
        """创建爬取总结文件"""
        summary_file = self.output_dir / "README.md"
        
        section_stats = {}
        for poem in self.scraped_poems:
            section = poem['section']
            if section not in section_stats:
                section_stats[section] = []
            section_stats[section].append(poem)
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# 海子诗集 - 爬取总结\n\n")
            f.write(f"**爬取时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**数据来源**: {self.base_url}\n")
            f.write(f"**成功爬取**: {len(self.scraped_poems)} 首诗歌\n")
            f.write(f"**失败数量**: {len(self.failed_poems)} 首\n\n")
            
            f.write("## 目录结构\n\n")
            f.write("```\n")
            f.write("poems/\n")
            for section_key, poems in section_stats.items():
                section_name = self.get_section_name(section_key)
                f.write(f"├── {section_key}/ ({section_name})\n")
                f.write(f"│   └── {len(poems)} 首诗歌\n")
            f.write("```\n\n")
            
            f.write("## 各章节详情\n\n")
            for section_key, poems in section_stats.items():
                section_name = self.get_section_name(section_key)
                f.write(f"### {section_name}\n\n")
                f.write(f"共 {len(poems)} 首诗歌：\n\n")
                
                for poem in poems[:10]:  # 只显示前10首
                    filename = Path(poem['filepath']).name
                    f.write(f"- [{poem['title']}]({section_key}/{filename})\n")
                
                if len(poems) > 10:
                    f.write(f"- ... 还有 {len(poems) - 10} 首诗歌\n")
                f.write("\n")
            
            if self.failed_poems:
                f.write("## 爬取失败的诗歌\n\n")
                for poem in self.failed_poems:
                    f.write(f"- {poem['title']} ({poem['url']})\n")
        
        print(f"📋 总结文件已创建: {summary_file}")

if __name__ == "__main__":
    scraper = HaiziFullScraper()
    scraper.scrape_all_poems()