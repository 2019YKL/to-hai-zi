import markdown
import re

def convert_md_to_html():
    """将markdown文件转换为HTML"""
    
    # 读取markdown文件
    with open('haizi_poems.md', 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 读取HTML模板
    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 预处理markdown内容，添加CSS类
    processed_md = preprocess_markdown(md_content)
    
    # 转换markdown为HTML
    md = markdown.Markdown(extensions=['toc', 'codehilite'])
    html_content = md.convert(processed_md)
    
    # 后处理HTML内容
    html_content = postprocess_html(html_content)
    
    # 替换模板中的占位符
    final_html = template.replace('{{CONTENT}}', html_content)
    
    # 保存最终HTML文件
    with open('haizi_poems.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print("HTML文件已生成: haizi_poems.html")

def preprocess_markdown(content):
    """预处理markdown内容"""
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        # 为章节标题添加id
        if line.startswith('## 第一编'):
            line = '<h2 id="section1">第一编　短诗（1983—1986）</h2>'
        elif line.startswith('## 第二编'):
            line = '<h2 id="section2">第二编　长诗（1984—1985）</h2>'
        elif line.startswith('## 第三编'):
            line = '<h2 id="section3">第三编　短诗（1987—1989）</h2>'
        
        processed_lines.append(line)
    
    return '\n'.join(processed_lines)

def postprocess_html(html_content):
    """后处理HTML内容"""
    
    # 为诗歌内容添加CSS类
    # 将诗歌标题后的内容包装在poem-content div中
    pattern = r'(<h3>.*?</h3>)(.*?)(<p><em>链接:.*?</em></p>)'
    
    def replace_poem(match):
        title = match.group(1)
        content = match.group(2).strip()
        link = match.group(3)
        
        # 清理内容，移除多余的p标签
        content = re.sub(r'<p>(.*?)</p>', r'\1', content)
        content = content.replace('\n', '<br>')
        
        return f'{title}\n<div class="poem-content">{content}\n<div class="poem-meta">{link}</div></div>'
    
    html_content = re.sub(pattern, replace_poem, html_content, flags=re.DOTALL)
    
    # 处理链接样式
    html_content = html_content.replace('<em>链接:', '<em class="poem-link">原文链接:')
    
    return html_content

if __name__ == "__main__":
    convert_md_to_html()