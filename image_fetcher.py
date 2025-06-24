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
        # 精确的标题关键词映射
        title_keywords = {
            # 自然元素
            "七月不远": "july summer lake",
            "七月的大海": "july ocean sea waves",
            "面朝大海，春暖花开": "ocean view spring flowers beach",
            "春天，十个海子": "spring lake nature",
            "亚洲铜": "copper metal ancient asia",
            "阿尔的太阳": "sun bright golden light",
            "麦地": "wheat field golden harvest",
            "秋": "autumn fall leaves golden",
            "冬天": "winter snow cold landscape",
            "村庄": "village countryside rural",
            "山楂树": "hawthorn tree blossoms",
            "桃花": "peach blossoms pink flowers",
            "菊花": "chrysanthemum yellow flowers",
            "莲花": "lotus flower water",
            "梅花": "plum blossoms winter flowers",
            
            # 时间和季节
            "春": "spring flowers nature green",
            "夏": "summer sun bright golden",
            "秋": "autumn leaves golden orange",
            "冬": "winter snow white landscape",
            "黎明": "dawn sunrise morning light",
            "黄昏": "sunset dusk evening golden",
            "夜": "night stars darkness moon",
            "正午": "noon bright sun midday",
            
            # 地理和景观
            "大海": "ocean sea waves blue horizon",
            "湖泊": "lake water calm reflection",
            "河流": "river stream flowing water",
            "山脉": "mountains peaks landscape",
            "草原": "grassland prairie green vast",
            "森林": "forest trees green nature",
            "田野": "field countryside rural green",
            "沙漠": "desert sand dunes golden",
            
            # 情感和抽象
            "孤独": "solitude alone contemplation",
            "思念": "longing memory nostalgic",
            "爱情": "love romantic heart",
            "梦想": "dream aspiration hope",
            "自由": "freedom bird sky open",
            "诗歌": "poetry writing literature",
            "音乐": "music harmony sound",
            "舞蹈": "dance movement graceful",
            
            # 动物
            "马": "horse running field wild",
            "鸟": "bird flying sky freedom",
            "鱼": "fish water swimming ocean",
            "蝴蝶": "butterfly colorful flowers",
            "天鹅": "swan white elegant water",
            
            # 建筑和人文
            "村庄": "village countryside houses",
            "城市": "city urban buildings",
            "教堂": "church architecture spiritual",
            "桥梁": "bridge river architecture",
            "古迹": "ancient ruins historical"
        }
        
        # 直接匹配标题
        if title in title_keywords:
            return title_keywords[title]
        
        # 检查标题中包含的关键词
        for keyword, search_term in title_keywords.items():
            if keyword in title:
                return search_term
        
        # 默认搜索词 - 更加诗意和自然
        return "nature landscape poetry serene beautiful"
    
    def search_image(self, query):
        """搜索图片，确保不重复"""
        params = {
            "query": query,
            "per_page": 30,  # 获取更多选择
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
        """为诗歌获取合适的图片URL（不下载）"""
        keywords = self.get_poem_keywords(title)
        print(f"为《{title}》搜索图片，关键词: {keywords}")
        
        # 搜索图片
        search_result = self.search_image(keywords)
        if not search_result or not search_result.get('photos'):
            print(f"未找到合适的图片: {title}")
            return "assets/images/image-haizi.jpg"  # 返回默认图片
        
        # 寻找未使用的图片
        for photo in search_result['photos']:
            photo_id = photo['id']
            if photo_id not in self.used_images:
                self.used_images.add(photo_id)
                image_url = photo['src']['large']  # 使用大图
                print(f"✅ 为《{title}》找到图片: {image_url}")
                return image_url
        
        # 如果所有图片都已使用，使用第一张
        photo = search_result['photos'][0]
        image_url = photo['src']['large']
        print(f"⚠️ 为《{title}》使用重复图片: {image_url}")
        return image_url

def update_all_poems_with_images():
    """为所有诗歌获取图片URL（不下载文件）"""
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
            
            # 添加短暂延迟避免API限制
            time.sleep(0.3)
        except Exception as e:
            print(f"处理《{poem['title']}》时出错: {e}")
            poem['image'] = "assets/images/image-haizi.jpg"  # 使用默认图片
    
    # 保存更新后的数据
    save_poems_data(poems_data)
    print(f"\n🎉 完成！已为所有 {len(poems_data)} 首诗歌配置图片URL")

if __name__ == "__main__":
    # 检查是否需要安装依赖
    try:
        import dotenv
    except ImportError:
        print("请先安装依赖: pip install python-dotenv requests")
        exit(1)
    
    update_all_poems_with_images()