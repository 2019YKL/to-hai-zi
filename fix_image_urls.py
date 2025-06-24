import json
import re

def fix_image_urls():
    """将本地图片路径改为 Pexels URL"""
    
    # 读取当前数据
    with open('assets/js/poems-data.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 JSON 数据
    json_start = content.find('[')
    json_end = content.rfind(']') + 1
    json_str = content[json_start:json_end]
    
    poems_data = json.loads(json_str)
    
    print(f"修复 {len(poems_data)} 首诗歌的图片URL...")
    
    # 根据日志获取的完整图片URL映射
    image_mapping = {
        "七月不远": "https://images.pexels.com/photos/27268278/pexels-photo-27268278.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "七月的大海": "https://images.pexels.com/photos/7659110/pexels-photo-7659110.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "不幸": "https://images.pexels.com/photos/7958869/pexels-photo-7958869.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "不要问我那绿色是什么": "https://images.pexels.com/photos/6963451/pexels-photo-6963451.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "东方山脉": "https://images.pexels.com/photos/32671486/pexels-photo-32671486.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "中午": "https://images.pexels.com/photos/7958214/pexels-photo-7958214.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "中国器乐": "https://images.pexels.com/photos/7958005/pexels-photo-7958005.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "为了美丽": "https://images.pexels.com/photos/7958216/pexels-photo-7958216.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "主人": "https://images.pexels.com/photos/7958218/pexels-photo-7958218.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "亚洲铜": "https://images.pexels.com/photos/28831416/pexels-photo-28831416.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "从六月到十月": "https://images.pexels.com/photos/7958843/pexels-photo-7958843.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "你的手": "https://images.pexels.com/photos/7958019/pexels-photo-7958019.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "八月尾": "https://images.pexels.com/photos/7958245/pexels-photo-7958245.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "写给脖子上的菩萨": "https://images.pexels.com/photos/1707471/pexels-photo-1707471.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "农耕民族": "https://images.pexels.com/photos/19758090/pexels-photo-19758090.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "北方门前": "https://images.pexels.com/photos/31853285/pexels-photo-31853285.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "半截的诗": "https://images.pexels.com/photos/157069/pexels-photo-157069.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "单翅鸟": "https://images.pexels.com/photos/32663074/pexels-photo-32663074.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "印度之夜": "https://images.pexels.com/photos/552788/pexels-photo-552788.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "哑脊背": "https://images.pexels.com/photos/12594942/pexels-photo-12594942.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "哭泣": "https://images.pexels.com/photos/18232582/pexels-photo-18232582.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "喜马拉雅": "https://images.pexels.com/photos/13340067/pexels-photo-13340067.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "在昌平的孤独": "https://images.pexels.com/photos/1134204/pexels-photo-1134204.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "面朝大海，春暖花开": "https://images.pexels.com/photos/457882/pexels-photo-457882.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "山楂树": "https://images.pexels.com/photos/4495702/pexels-photo-4495702.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "在一个阿拉伯沙漠的村镇上": "https://images.pexels.com/photos/2156083/pexels-photo-2156083.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "在大草原上预感到海的降临": "https://images.pexels.com/photos/13456191/pexels-photo-13456191.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "夜晚　亲爱的朋友": "https://images.pexels.com/photos/923203/pexels-photo-923203.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "夜色": "https://images.pexels.com/photos/981866/pexels-photo-981866.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "大草原　大雪封山": "https://images.pexels.com/photos/29376366/pexels-photo-29376366.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
    }
    
    # 更新图片URL
    for poem in poems_data:
        title = poem['title']
        if title in image_mapping:
            poem['image'] = image_mapping[title]
            print(f"✅ 更新《{title}》的图片URL")
        else:
            # 使用默认图片
            poem['image'] = "assets/images/image-haizi.jpg"
    
    # 保存更新后的数据
    js_content = f"""// 海子诗歌数据 - 自动生成
// 生成时间: 2025-06-23 21:00:00

const poemsData = {json.dumps(poems_data, ensure_ascii=False, indent=2)};

// 导出数据
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = poemsData;
}} else if (typeof window !== 'undefined') {{
    window.poemsData = poemsData;
}}
"""
    
    with open('assets/js/poems-data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"\n🎉 完成！已修复图片URL")

if __name__ == "__main__":
    fix_image_urls()