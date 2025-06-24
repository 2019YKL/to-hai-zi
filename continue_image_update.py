import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import time
import random

# 加载环境变量
load_dotenv()

class PexelsImageFetcher:
    def __init__(self):
        self.api_key = os.getenv('PEXELS_API_KEY')
        if not self.api_key:
            raise ValueError("请在 .env 文件中设置 PEXELS_API_KEY")
        
        self.base_url = "https://api.pexels.com/v1/search"
        self.headers = {
            "Authorization": self.api_key
        }
        self.used_images = set()  # 记录已使用的图片ID
    
    def get_poem_keywords(self, title):
        """从诗歌标题中提取精确关键词，扩大关键词库"""
        title_keywords = {
            # 海子经典作品
            "面朝大海，春暖花开": "ocean spring flowers beach horizon",
            "春天，十个海子": "spring lake water nature",
            "阿尔的太阳": "sun bright golden light provence",
            "麦地": "wheat field golden harvest farm",
            "村庄": "village countryside rural peaceful",
            
            # 季节和时间
            "春天": "spring flowers green nature",
            "春": "spring blossoms green",
            "夏天": "summer sun bright golden",
            "夏": "summer warm sunshine",
            "秋天": "autumn leaves golden orange",
            "秋": "autumn fall colors",
            "冬天": "winter snow white cold",
            "冬": "winter frost landscape",
            "黎明": "dawn sunrise morning light",
            "黄昏": "sunset dusk evening golden",
            "夜": "night stars darkness moon",
            "夜晚": "night evening stars",
            "中午": "noon bright sun midday",
            "正午": "noon bright sunshine",
            "拂晓": "dawn sunrise morning",
            "日出": "sunrise dawn morning golden",
            "日光": "sunlight bright rays",
            
            # 自然景观
            "大海": "ocean sea waves blue vast",
            "海": "ocean sea water blue",
            "海上": "ocean seascape waves",
            "海水": "ocean water blue waves",
            "太平洋": "pacific ocean blue vast",
            "湖泊": "lake water calm reflection",
            "河流": "river stream flowing water",
            "山脉": "mountains peaks landscape",
            "东方山脉": "mountains eastern peaks",
            "喜马拉雅": "himalaya mountains snow peaks",
            "草原": "grassland prairie green vast",
            "大草原": "grassland prairie wide open",
            "黄金草原": "golden grassland prairie",
            "森林": "forest trees green nature",
            "田野": "field countryside green rural",
            "沙漠": "desert sand dunes golden",
            
            # 植物花卉
            "花": "flowers colorful beautiful petals",
            "梅花": "plum blossoms winter white",
            "桃花": "peach blossoms pink spring",
            "菊花": "chrysanthemum yellow autumn",
            "莲花": "lotus flower water pink",
            "玫瑰花": "rose flowers red beautiful",
            "山楂树": "hawthorn tree blossoms white",
            "麦": "wheat golden field grain",
            "草": "grass green meadow field",
            "树": "trees forest green nature",
            "果园": "orchard trees fruit garden",
            "葡萄园": "vineyard grapes vines",
            
            # 动物
            "马": "horse running field wild",
            "鸟": "bird flying sky freedom",
            "天鹅": "swan white elegant water",
            "鱼": "fish water swimming ocean",
            "蝴蝶": "butterfly colorful flowers",
            "单翅鸟": "bird flying sky wings",
            "公鸡": "rooster farm morning",
            "龙": "dragon mythical powerful",
            "虎": "tiger powerful wild",
            "龟": "turtle peaceful water",
            
            # 天象气候
            "太阳": "sun bright golden light",
            "月": "moon night sky silver",
            "月亮": "moon night sky bright",
            "星": "stars night sky cosmic",
            "云": "clouds sky white fluffy",
            "雨": "rain drops weather water",
            "雪": "snow white winter cold",
            "风": "wind movement nature trees",
            "光": "light bright sunshine rays",
            "火": "fire flame warm orange",
            
            # 地理地名
            "青海": "lake blue water plateau",
            "西藏": "tibet mountains plateau",
            "昌平": "countryside rural peaceful",
            "北方": "north landscape vast",
            "南方": "south warm landscape",
            "印度": "india culture temple",
            "阿拉伯": "arab desert middle east",
            "敦煌": "desert ancient silk road",
            "九寨": "nature colorful lakes",
            
            # 情感抽象
            "孤独": "solitude alone peaceful",
            "思念": "longing memory nostalgic",
            "爱情": "love romantic heart",
            "幸福": "happiness joy bright",
            "美丽": "beauty elegant serene",
            "梦想": "dream aspiration hope",
            "自由": "freedom sky open space",
            "死亡": "dark contemplation somber",
            "生命": "life vibrant nature",
            "活": "life vibrant energy",
            
            # 人文艺术
            "诗歌": "poetry writing literature",
            "诗": "poetry artistic writing",
            "音乐": "music harmony instruments",
            "器乐": "instruments music traditional",
            "舞蹈": "dance movement graceful",
            "民族": "culture traditional ethnic",
            "农耕": "farming agriculture rural",
            "村镇": "village town rural",
            "城里": "city urban buildings",
            "家乡": "hometown countryside",
            "房屋": "house building architecture",
            "门": "door entrance architecture",
            
            # 物品器具
            "坛子": "pottery ceramic traditional",
            "杯子": "cup ceramic peaceful",
            "钟": "bell temple traditional",
            "船": "boat water sailing",
            "木船": "wooden boat water",
            "工具": "tools craftsmanship",
            
            # 身体感官
            "手": "hands gentle caring",
            "眼睛": "eyes vision sight",
            "脖子": "neck graceful",
            "脚": "feet walking journey",
            
            # 颜色
            "黑": "dark shadow mysterious",
            "白": "white pure clean",
            "金": "golden bright precious",
            "蓝": "blue sky ocean",
            "绿": "green nature forest",
            "红": "red warm passionate",
            
            # 数字时间
            "七月": "july summer warm",
            "八月": "august summer late",
            "九月": "september autumn",
            "五月": "may spring fresh",
            "六月": "june summer early",
            "十月": "october autumn golden",
            "七百年": "ancient historical time",
            
            # 文学人物
            "荷尔德林": "poetry literature romantic",
            "卡夫卡": "literature existential",
            "托尔斯泰": "literature russian classic",
            "但丁": "literature divine classic",
            "莫扎特": "music classical harmony",
            "梭罗": "nature philosophy thoreau",
            "尼采": "philosophy mountains",
        }
        
        # 直接匹配标题
        if title in title_keywords:
            return title_keywords[title]
        
        # 检查标题中包含的关键词
        for keyword, search_term in title_keywords.items():
            if keyword in title:
                return search_term
        
        # 根据标题特征推测
        if any(word in title for word in ["海", "水", "湖", "河", "波", "浪"]):
            return "water ocean lake blue peaceful"
        elif any(word in title for word in ["山", "峰", "岭", "岩"]):
            return "mountains landscape nature majestic"
        elif any(word in title for word in ["花", "草", "树", "林", "园"]):
            return "flowers nature garden beautiful"
        elif any(word in title for word in ["夜", "晚", "暗", "黑"]):
            return "night evening stars peaceful"
        elif any(word in title for word in ["春", "夏", "秋", "冬"]):
            return "seasons nature landscape beautiful"
        elif any(word in title for word in ["雨", "雪", "风", "云"]):
            return "weather nature sky atmospheric"
        elif any(word in title for word in ["太阳", "阳", "光", "日"]):
            return "sun sunshine bright golden"
        elif any(word in title for word in ["村", "乡", "家", "故"]):
            return "countryside rural village peaceful"
        elif any(word in title for word in ["城", "市", "街", "路"]):
            return "city urban architecture"
        elif any(word in title for word in ["爱", "情", "心", "恋"]):
            return "love romantic beautiful serene"
        elif any(word in title for word in ["诗", "歌", "文", "书"]):
            return "poetry literature artistic beautiful"
        
        # 默认搜索词 - 诗意自然风景
        return "poetry nature landscape serene beautiful peaceful"
    
    def search_image(self, query, retry_count=3):
        """搜索图片，添加重试机制"""
        params = {
            "query": query,
            "per_page": 40,  # 获取更多选择
            "orientation": "landscape"
        }
        
        for attempt in range(retry_count):
            try:
                response = requests.get(self.base_url, headers=self.headers, params=params, timeout=10)
                if response.status_code == 429:  # Too Many Requests
                    wait_time = (2 ** attempt) * 5  # 指数退避: 5, 10, 20 秒
                    print(f"API 限制，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == retry_count - 1:
                    print(f"搜索图片失败 (尝试 {retry_count} 次): {e}")
                    return None
                else:
                    print(f"搜索失败，{2} 秒后重试...")
                    time.sleep(2)
        
        return None
    
    def get_image_url_for_poem(self, title):
        """为诗歌获取合适的图片URL"""
        keywords = self.get_poem_keywords(title)
        print(f"为《{title}》搜索图片，关键词: {keywords}")
        
        # 搜索图片
        search_result = self.search_image(keywords)
        if not search_result or not search_result.get('photos'):
            print(f"未找到合适的图片: {title}")
            return "assets/images/image-haizi.jpg"
        
        # 寻找未使用的图片
        for photo in search_result['photos']:
            photo_id = photo['id']
            if photo_id not in self.used_images:
                self.used_images.add(photo_id)
                image_url = photo['src']['large']
                print(f"✅ 为《{title}》找到图片: {image_url}")
                return image_url
        
        # 如果所有图片都已使用，使用第一张
        photo = search_result['photos'][0]
        image_url = photo['src']['large']
        print(f"⚠️ 为《{title}》使用重复图片: {image_url}")
        return image_url

def continue_image_update(batch_size=20):
    """继续为剩余诗歌获取图片URL"""
    
    # 读取当前数据
    with open('assets/js/poems-data.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 JSON 数据
    json_start = content.find('[')
    json_end = content.rfind(']') + 1
    json_str = content[json_start:json_end]
    poems_data = json.loads(json_str)
    
    # 找出还没有 Pexels 图片的诗歌
    poems_to_process = []
    for poem in poems_data:
        if poem['image'] == "assets/images/image-haizi.jpg":
            poems_to_process.append(poem)
    
    print(f"需要处理 {len(poems_to_process)} 首诗歌")
    
    if not poems_to_process:
        print("所有诗歌都已有图片！")
        return
    
    # 初始化图片获取器
    fetcher = PexelsImageFetcher()
    
    # 分批处理
    for batch_start in range(0, len(poems_to_process), batch_size):
        batch_end = min(batch_start + batch_size, len(poems_to_process))
        batch = poems_to_process[batch_start:batch_end]
        
        print(f"\n处理批次 {batch_start//batch_size + 1}: {batch_start + 1}-{batch_end} 首诗歌")
        
        for i, poem in enumerate(batch, batch_start + 1):
            print(f"\n[{i}/{len(poems_to_process)}] 处理: {poem['title']}")
            
            try:
                # 获取图片URL
                image_url = fetcher.get_image_url_for_poem(poem['title'])
                poem['image'] = image_url
                
                # 随机延迟 1-3 秒
                delay = random.uniform(1.0, 3.0)
                time.sleep(delay)
                
            except Exception as e:
                print(f"处理《{poem['title']}》时出错: {e}")
                # 发生错误时使用默认图片
                continue
        
        # 每批次后保存数据
        save_poems_data(poems_data)
        print(f"✅ 批次 {batch_start//batch_size + 1} 完成，已保存数据")
        
        # 批次间休息
        if batch_end < len(poems_to_process):
            print("批次间休息 10 秒...")
            time.sleep(10)
    
    print(f"\n🎉 完成！已为所有诗歌配置图片URL")

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
    
    with open('assets/js/poems-data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)

if __name__ == "__main__":
    continue_image_update(batch_size=15)  # 每批15首诗歌