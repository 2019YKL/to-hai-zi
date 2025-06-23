import os
import json
from pathlib import Path
import re

def generate_poems_data():
    """生成诗歌数据文件"""
    poems_dir = Path("assets/content/poems")
    poems_data = []
    
    # 章节配置
    sections = {
        '00-preface': {'name': '扉页', 'order': 0},
        '01-short-poems-1983-1986': {'name': '第一编　短诗（1983—1986）', 'order': 1},
        '02-long-poems-1984-1985': {'name': '第二编　长诗（1984—1985）', 'order': 2},
        '03-short-poems-1987-1989': {'name': '第三编　短诗（1987—1989）', 'order': 3}
    }
    
    for section_dir_name, section_info in sections.items():
        section_path = poems_dir / section_dir_name
        
        if not section_path.exists():
            continue
            
        # 获取该章节的所有MD文件
        md_files = list(section_path.glob("*.md"))
        md_files.sort()  # 按文件名排序
        
        for md_file in md_files:
            try:
                # 读取MD文件内容
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 解析诗歌信息
                poem_info = parse_poem_content(content)
                
                # 生成slug（用于URL）
                slug = md_file.stem
                
                # 相对路径
                relative_path = f"{section_dir_name}/{md_file.name}"
                
                poem_data = {
                    'title': poem_info['title'],
                    'slug': slug,
                    'path': relative_path,
                    'section': section_info['name'],
                    'section_order': section_info['order'],
                    'preview': poem_info['preview'],
                    'full_content': poem_info['full_content'],
                    'date': poem_info.get('date', ''),
                    'image': 'assets/images/image-haizi.jpg',  # 统一使用海子照片
                    'url': poem_info.get('original_url', ''),
                    'content_preview': poem_info['preview']
                }
                
                poems_data.append(poem_data)
                
            except Exception as e:
                print(f"处理文件 {md_file} 时出错: {e}")
                continue
    
    # 按章节和文件名排序
    poems_data.sort(key=lambda x: (x['section_order'], x['title']))
    
    return poems_data

def parse_poem_content(content):
    """解析诗歌内容，提取标题、完整内容等信息"""
    lines = content.split('\n')
    
    title = '未知诗歌'
    poem_lines = []
    preview_lines = []
    date = ''
    original_url = ''
    
    content_started = False
    in_meta_section = False
    
    for line in lines:
        line = line.strip()
        
        # 提取标题
        if line.startswith('# '):
            title = line[2:].strip()
            content_started = True
            continue
        
        # 检查是否进入元数据部分
        if line == '---' and content_started:
            in_meta_section = True
            continue
        
        # 在元数据部分提取信息
        if in_meta_section:
            if '**原文链接**:' in line:
                original_url = line.split(':', 1)[1].strip()
            continue
        
        # 收集正文内容
        if content_started and not in_meta_section and line:
            # 检查是否是日期格式（YYYY.MM.DD）
            if re.match(r'^\d{4}\.\d{1,2}(\.\d{1,2})?$', line):
                date = line
                continue
                
            poem_lines.append(line)
            
            # 前4行作为预览
            if len(preview_lines) < 4:
                preview_lines.append(line)
    
    # 生成预览文本
    preview = '\n'.join(preview_lines)
    if len(poem_lines) > 4:
        preview += '...'
    
    # 完整内容
    full_content = '\n'.join(poem_lines)
    
    return {
        'title': title,
        'preview': preview,
        'full_content': full_content,
        'date': date,
        'original_url': original_url
    }

def save_poems_data(poems_data):
    """保存诗歌数据到JS文件"""
    js_content = f"""// 海子诗歌数据 - 自动生成
// 生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

const poemsData = {json.dumps(poems_data, ensure_ascii=False, indent=2)};

// 导出数据
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = poemsData;
}} else if (typeof window !== 'undefined') {{
    window.poemsData = poemsData;
}}
"""
    
    output_path = Path("assets/js/poems-data.js")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ 诗歌数据已保存到: {output_path}")
    print(f"📊 共生成 {len(poems_data)} 首诗歌的数据")
    
    # 按章节统计
    section_stats = {}
    for poem in poems_data:
        section = poem['section']
        if section not in section_stats:
            section_stats[section] = 0
        section_stats[section] += 1
    
    print("\n📋 各章节统计:")
    for section, count in section_stats.items():
        print(f"  {section}: {count} 首")

if __name__ == "__main__":
    poems_data = generate_poems_data()
    save_poems_data(poems_data)