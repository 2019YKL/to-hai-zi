import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import time

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
        """从诗歌标题中提取精确关键词"""
        title_keywords = {
            # 海子经典作品
            "面朝大海，春暖花开": "ocean spring flowers beach horizon",
            "七月不远": "july summer lake water",
            "七月的大海": "july ocean sea waves blue",
            "春天，十个海子": "spring lake water nature",
            "亚洲铜": "copper metal ancient asia bronze",
            "阿尔的太阳": "sun bright golden light vincent",
            "麦地": "wheat field golden harvest farm",
            "村庄": "village countryside rural houses",
            
            # 季节和时间
            "春": "spring flowers green nature",
            "夏": "summer sun bright golden",
            "秋": "autumn leaves golden orange",
            "冬": "winter snow white cold",
            "黎明": "dawn sunrise morning light",
            "黄昏": "sunset dusk evening golden",
            "夜": "night stars darkness moon",
            "中午": "noon bright sun midday",
            "正午": "noon bright sun midday",
            "拂晓": "dawn sunrise morning light",
            "日出": "sunrise dawn morning",
            
            # 自然景观
            "大海": "ocean sea waves blue",
            "湖泊": "lake water calm reflection",
            "河流": "river stream flowing water",
            "山脉": "mountains peaks landscape",
            "东方山脉": "mountains peaks eastern landscape",
            "草原": "grassland prairie green vast",
            "大草原": "grassland prairie green vast",
            "森林": "forest trees green nature",
            "田野": "field countryside green rural",
            "沙漠": "desert sand dunes golden",
            "太平洋": "pacific ocean blue vast",
            
            # 植物
            "花": "flowers colorful beautiful",
            "梅花": "plum blossoms winter white",
            "桃花": "peach blossoms pink spring",
            "菊花": "chrysanthemum yellow autumn",
            "莲花": "lotus flower water pink",
            "山楂树": "hawthorn tree blossoms white",
            "麦": "wheat golden field",
            "草": "grass green meadow",
            "树": "trees forest green",
            
            # 动物
            "马": "horse running field wild",
            "鸟": "bird flying sky freedom",
            "天鹅": "swan white elegant water",
            "鱼": "fish water swimming ocean",
            "蝴蝶": "butterfly colorful flowers",
            "单翅鸟": "bird flying sky freedom",
            
            # 天象
            "太阳": "sun bright golden light",
            "月": "moon night sky silver",
            "星": "stars night sky cosmic",
            "云": "clouds sky white fluffy",
            "雨": "rain drops weather water",
            "雪": "snow white winter cold",
            "风": "wind movement nature",
            "光": "light bright sunshine",
            
            # 地理和地名
            "青海": "lake blue water plateau",
            "西藏": "tibet mountains plateau snow",
            "喜马拉雅": "himalaya mountains snow peaks",
            "昌平": "countryside rural peaceful",
            "北方": "north landscape vast",
            "印度": "india culture ancient",
            "阿拉伯": "arab desert sand middle east",
            
            # 情感和抽象
            "孤独": "solitude alone contemplation",
            "思念": "longing memory nostalgic",
            "爱情": "love romantic heart",
            "幸福": "happiness joy bright",
            "美丽": "beauty elegant serene",
            "梦想": "dream aspiration hope",
            "自由": "freedom sky open space",
            "死亡": "death dark contemplation",
            "生命": "life vibrant nature",
            
            # 人文
            "诗歌": "poetry writing literature",
            "音乐": "music harmony instruments",
            "器乐": "instruments music traditional",
            "舞蹈": "dance movement graceful",
            "民族": "culture traditional ethnic",
            "村镇": "village town rural",
            "城里": "city urban buildings",
            "家乡": "hometown countryside nostalgic"
        }
        
        # 直接匹配标题
        if title in title_keywords:
            return title_keywords[title]
        
        # 检查标题中包含的关键词
        for keyword, search_term in title_keywords.items():
            if keyword in title:
                return search_term
        
        # 根据标题长度和内容推测
        if "海" in title:
            return "ocean sea water blue"
        elif "山" in title:
            return "mountains landscape nature"
        elif "花" in title:
            return "flowers beautiful colorful"
        elif "夜" in title:
            return "night stars moon darkness"
        elif "春" in title:
            return "spring green nature flowers"
        elif "雨" in title:
            return "rain water drops weather"
        elif "雪" in title:
            return "snow white winter cold"
        elif "风" in title:
            return "wind movement nature"
        elif "太阳" in title:
            return "sun bright golden light"
        
        # 默认搜索词
        return "nature landscape beautiful serene poetry"
    
    def search_image(self, query):
        """搜索图片"""
        params = {
            "query": query,
            "per_page": 50,  # 获取更多选择
            "orientation": "landscape"
        }
        
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"搜索图片失败: {e}")
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

def update_all_poems_with_images():
    """为所有诗歌获取图片URL"""
    from generate_poems_data import generate_poems_data, save_poems_data
    
    # 初始化图片获取器
    fetcher = PexelsImageFetcher()
    
    # 生成诗歌数据
    poems_data = generate_poems_data()
    
    print(f"开始为所有 {len(poems_data)} 首诗歌获取图片URL...")
    
    # 为每首诗获取图片URL
    for i, poem in enumerate(poems_data, 1):
        print(f"\n[{i}/{len(poems_data)}] 处理: {poem['title']}")
        
        try:
            # 获取图片URL
            image_url = fetcher.get_image_url_for_poem(poem['title'])
            poem['image'] = image_url
            
            # 添加延迟避免API限制
            time.sleep(0.2)  # 减少延迟
        except Exception as e:
            print(f"处理《{poem['title']}》时出错: {e}")
            poem['image'] = "assets/images/image-haizi.jpg"
    
    # 保存更新后的数据
    save_poems_data(poems_data)
    print(f"\n🎉 完成！已为所有 {len(poems_data)} 首诗歌配置图片URL")

if __name__ == "__main__":
    update_all_poems_with_images()