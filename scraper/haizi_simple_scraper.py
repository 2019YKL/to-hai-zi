import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin

def get_page_content(url):
    """获取页面内容"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_poem_links_from_main():
    """从主页提取诗歌链接"""
    base_url = "https://haizi.huhaitai.com/"
    soup = get_page_content(base_url)
    if not soup:
        return []
    
    links = []
    # 查找所有包含诗歌链接的a标签
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        title = link.get_text().strip()
        
        # 过滤掉非诗歌链接
        if (href and href.startswith('/') and 
            title and len(title) > 0 and
            not title in ['扉　页：海子简历与照片', '骆一禾：海子生涯', '西　川：怀念']):
            
            full_url = urljoin(base_url, href)
            links.append({
                'title': title,
                'url': full_url, 
                'path': href
            })
    
    return links

def get_poem_content(url):
    """获取单首诗内容"""
    soup = get_page_content(url)
    if not soup:
        return None
    
    # 移除导航和脚本
    for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
        tag.decompose()
    
    # 获取body文本
    body = soup.find('body')
    if not body:
        return None
    
    text = body.get_text(separator='\n')
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # 过滤导航和目录行
    skip_words = ['目录', '第一编', '第二编', '第三编', '上一页', '下一页', '返回', 'haizi.huhaitai.com']
    filtered_lines = []
    
    for line in lines:
        if (len(line) > 1 and 
            not any(word in line for word in skip_words) and
            not line.isdigit() and
            not re.match(r'^\d+$', line)):
            filtered_lines.append(line)
    
    return '\n'.join(filtered_lines[:50])  # 限制行数避免过长

def main():
    print("开始爬取海子诗集...")
    
    # 获取所有诗歌链接
    poem_links = extract_poem_links_from_main()
    print(f"找到 {len(poem_links)} 个链接")
    
    # 创建markdown文件
    with open('../assets/content/haizi_poems.md', 'w', encoding='utf-8') as f:
        f.write("# 海子诗集\n\n")
        f.write("数据来源: https://haizi.huhaitai.com/\n\n")
        
        current_section = ""
        poem_count = 0
        
        # 处理前50首诗避免超时
        for i, poem in enumerate(poem_links[:50]):
            print(f"处理第 {i+1} 首: {poem['title']}")
            
            # 判断章节
            if poem['path'].startswith('/f'):
                section = "## 扉页\n\n"
            elif poem['path'].startswith('/01/'):
                section = "## 第一编　短诗（1983—1986）\n\n"
            elif poem['path'].startswith('/02/'):
                section = "## 第二编　长诗（1984—1985）\n\n"
            elif poem['path'].startswith('/03/'):
                section = "## 第三编　短诗（1987—1989）\n\n"
            else:
                section = ""
            
            # 写入新章节标题
            if section and section != current_section:
                f.write(section)
                current_section = section
            
            # 写入诗歌标题
            f.write(f"### {poem['title']}\n\n")
            
            # 获取内容
            content = get_poem_content(poem['url'])
            if content:
                f.write(f"{content}\n\n")
            else:
                f.write("*内容获取失败*\n\n")
            
            f.write(f"*链接: {poem['url']}*\n\n")
            f.write("---\n\n")
            
            poem_count += 1
            time.sleep(0.3)  # 短暂延迟
        
        f.write(f"\n\n*共收录 {poem_count} 首诗歌*\n")
    
    print(f"完成！已保存 {poem_count} 首诗歌到 ../assets/content/haizi_poems.md")

if __name__ == "__main__":
    main()