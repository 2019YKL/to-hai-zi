import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import time
import random

# 复用前面的类，只处理剩余的诗歌
load_dotenv()

class PoeticImageFetcher:
    def __init__(self):
        self.api_key = os.getenv('PEXELS_API_KEY')
        if not self.api_key:
            raise ValueError("请在 .env 文件中设置 PEXELS_API_KEY")
        
        self.base_url = "https://api.pexels.com/v1/search"
        self.headers = {
            "Authorization": self.api_key
        }
        self.used_images = set()
    
    def get_poetic_keywords(self, title):
        """为诗歌标题获取诗意的关键词"""
        
        # 直接意象类
        direct_imagery = {
            "面朝大海，春暖花开": "ocean waves horizon spring flowers peaceful",
            "大海": "ocean waves vast blue peaceful",
            "海": "ocean sea waves blue serene",
            "海上": "ocean seascape waves blue vast",
            "海水没顶": "ocean waves underwater blue",
            "海滩上为女士算命": "beach ocean waves sand peaceful",
            "太平洋": "pacific ocean blue vast",
            "湖泊": "lake water reflection peaceful calm",
            "河流": "river stream flowing water nature",
            "山脉": "mountains peaks landscape majestic",
            "东方山脉": "mountains sunrise peaks golden",
            "喜马拉雅": "snow mountains peaks majestic",
            "草原": "grassland vast green peaceful",
            "大草原": "grassland prairie wide peaceful",
            "黄金草原": "golden grassland sunset peaceful",
            "沙漠": "desert dunes golden peaceful",
            "麦地": "wheat field golden harvest",
            "五月的麦地": "wheat field golden may",
            "熟了麦子": "golden wheat field harvest",
            "天鹅": "white swan elegant water",
            "鸟": "bird flying sky freedom",
            "单翅鸟": "bird flying sky freedom",
            "马": "horse running field freedom",
            "鱼": "fish swimming water peaceful",
            "太阳": "sun bright golden rays",
            "月": "moon night silver peaceful",
            "月亮": "moon night silver calm",
            "星": "stars night sky cosmic",
            "云": "clouds sky white peaceful",
            "雨": "rain drops peaceful nature",
            "雪": "snow white winter peaceful",
            "风": "wind movement nature peaceful",
            "光": "sunlight rays golden peaceful",
            "花": "flowers colorful beautiful delicate",
            "梅花": "white blossoms winter delicate",
            "桃花": "pink blossoms spring beautiful",
            "菊花": "chrysanthemum golden autumn",
            "莲花": "lotus pink water peaceful",
            "玫瑰花": "roses red beautiful romantic",
            "山楂树": "white blossoms tree peaceful",
            "春天": "spring flowers green peaceful",
            "春": "spring blossoms green peaceful",
            "夏": "summer golden warm peaceful",
            "秋": "autumn golden leaves peaceful",
            "秋天": "autumn golden orange peaceful",
            "冬": "winter snow white peaceful",
            "村庄": "village countryside peaceful rural",
            "村": "village peaceful countryside",
        }
        
        # 抽象概念类
        abstract_concepts = {
            # 情感抽象
            "孤独": "solitary person peaceful contemplation",
            "在昌平的孤独": "solitary person peaceful landscape",
            "孤独的东方人": "solitary person peaceful contemplation",
            "思念": "solitary person nostalgic peaceful",
            "思念前生": "solitary person mystical peaceful",
            "爱情": "couple romantic peaceful sunset",
            "爱情故事": "couple romantic peaceful sunset",
            "爱情诗集": "couple romantic peaceful flowers",
            "幸福": "person peaceful happy meadow",
            "美丽": "flowers peaceful beautiful nature",
            "为了美丽": "flowers peaceful beautiful delicate",
            
            # 文学人物
            "给托尔斯泰": "birch trees peaceful russian landscape",
            "给卡夫卡": "mysterious forest peaceful contemplative",
            "给安徒生": "fairy tale cottage peaceful magical",
            "给萨福": "sea cliff peaceful romantic ancient",
            "荷尔德林": "german landscape peaceful romantic hills",
            "但丁来到此时此地": "path mysterious peaceful journey",
            "莫扎特在《安魂曲》中说": "music notes peaceful classical harmony",
            "梭罗这人有脑子": "forest pond peaceful contemplation nature",
            "尼采，你使我想起悲伤的热带": "mountain philosophy peaceful dramatic",
            
            # 诗歌创作
            "诗歌": "feather writing peaceful artistic inspiration",
            "诗": "paper writing peaceful artistic beautiful",
            "诗集": "books peaceful artistic knowledge wisdom",
            "诗学：一份提纲": "writing paper peaceful artistic study",
            "半截的诗": "paper torn peaceful artistic melancholy",
            "叙事诗": "storytelling peaceful artistic narrative",
            "四行诗": "writing peaceful minimalist artistic",
            "十四行": "roses romantic peaceful classical poetry",
            "歌或哭": "person emotional peaceful expression music",
            "民间艺人": "hands crafting peaceful traditional art",
            
            # 死亡主题
            "死亡": "dove white peaceful heaven serene",
            "自杀者之歌": "dove peaceful white heaven light",
            "土地·忧郁·死亡": "dove peaceful field heaven calm",
            
            # 神秘哲学
            "写给脖子上的菩萨": "lotus peaceful meditation spiritual golden",
            "莲界慈航": "lotus peaceful spiritual water divine",
            "早祷与枭": "dawn peaceful spiritual meditation temple",
            "打钟": "temple bell peaceful spiritual meditation",
            
            # 人物关系
            "主人": "person peaceful contemplative solitary nature",
            "女孩子": "young woman peaceful flowers innocent beautiful",
            "你的手": "hands gentle peaceful caring tender",
            "你和桃花": "person peaceful pink blossoms romantic",
            "得不到你": "solitary person peaceful melancholy longing",
            "妻子": "woman peaceful domestic gentle loving",
            "妻子和鱼": "water fish peaceful swimming gentle",
            "四姐妹": "women peaceful sisterhood harmony together",
            
            # 其他抽象概念
            "不幸": "dove peaceful white melancholy gentle",
            "不要问我那绿色是什么": "green forest peaceful mysterious nature",
            "中国器乐": "traditional instruments peaceful cultural harmony",
            "亚洲铜": "bronze peaceful ancient traditional art",
            "从六月到十月": "seasons changing peaceful natural cycle",
            "八月尾": "late summer peaceful golden harvest",
            "八月之杯": "cup peaceful summer golden reflection",
            "活在珍贵的人间": "person grateful peaceful nature blessed",
            "大自然": "forest peaceful natural beautiful wilderness",
            "房屋": "cottage peaceful architecture cozy home",
            "坛子": "ceramic jar peaceful traditional simple art",
            "杯子": "ceramic cup peaceful simple traditional beauty",
            "煤堆": "charcoal peaceful simple traditional craft",
            "粮食": "grain peaceful abundance harvest golden",
            "船": "boat peaceful water journey adventure",
            "木船": "wooden boat peaceful water traditional",
            "我们坐在一棵木头中": "tree peaceful meditation natural wisdom",
            "哭泣": "person peaceful emotional release healing",
            "我感到魅惑": "person peaceful mystical attractive dreamy",
            "我，以及其他的证人": "group peaceful contemplative witness truth",
            "门关户闭": "door peaceful quiet solitude contemplation",
        }
        
        # 首先检查直接意象
        if title in direct_imagery:
            return direct_imagery[title]
        
        # 然后检查抽象概念
        if title in abstract_concepts:
            return abstract_concepts[title]
        
        # 检查标题中包含的关键词
        for keyword, search_term in {**direct_imagery, **abstract_concepts}.items():
            if keyword in title and len(keyword) > 1:
                return search_term
        
        # 根据标题特征进行分类
        if any(word in title for word in ["海", "水", "湖", "河", "波", "浪", "泉"]):
            return "water ocean lake peaceful blue serene"
        elif any(word in title for word in ["山", "峰", "岭", "岩", "坡"]):
            return "mountains landscape peaceful majestic nature"
        elif any(word in title for word in ["花", "草", "树", "林", "园", "叶"]):
            return "flowers nature peaceful beautiful delicate"
        elif any(word in title for word in ["夜", "晚", "暗", "黑", "星", "月"]):
            return "night stars peaceful mystical calm"
        elif any(word in title for word in ["春", "夏", "秋", "冬", "季"]):
            return "seasons nature peaceful beautiful changing"
        elif any(word in title for word in ["雨", "雪", "风", "云", "雾"]):
            return "weather peaceful atmospheric beautiful nature"
        elif any(word in title for word in ["太阳", "阳", "光", "日", "晨", "晓"]):
            return "sunlight peaceful golden bright divine"
        elif any(word in title for word in ["村", "乡", "家", "故", "门", "房"]):
            return "countryside peaceful rural nostalgic home"
        elif any(word in title for word in ["鸟", "马", "鱼", "虫", "蝶"]):
            return "animal peaceful nature beautiful free"
        elif any(word in title for word in ["爱", "情", "心", "恋", "思", "念"]):
            return "romantic peaceful beautiful sunset flowers"
        elif any(word in title for word in ["孤", "独", "寂", "静", "默"]):
            return "solitary person peaceful contemplation nature"
        elif any(word in title for word in ["死", "亡", "终", "末"]):
            return "dove white peaceful heaven serene light"
        elif any(word in title for word in ["诗", "歌", "文", "书", "艺", "乐"]):
            return "artistic peaceful beautiful creative inspiration"
        elif any(word in title for word in ["给", "致", "献"]):
            return "gift peaceful beautiful meaningful tribute"
        
        # 默认：诗意的抽象美景
        return "peaceful landscape beautiful serene poetic nature"
    
    def search_image(self, query, retry_count=3):
        """搜索图片，添加重试机制"""
        params = {
            "query": query,
            "per_page": 50,
            "orientation": "landscape"
        }
        
        for attempt in range(retry_count):
            try:
                response = requests.get(self.base_url, headers=self.headers, params=params, timeout=15)
                if response.status_code == 429:
                    wait_time = (2 ** attempt) * 10
                    print(f"API 限制，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == retry_count - 1:
                    print(f"搜索图片失败: {e}")
                    return None
                else:
                    time.sleep(5)
        
        return None
    
    def get_image_url_for_poem(self, title):
        """为诗歌获取合适的图片URL"""
        keywords = self.get_poetic_keywords(title)
        print(f"为《{title}》搜索图片，关键词: {keywords}")
        
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

def finish_remaining_images():
    """完成剩余诗歌的图片"""
    
    # 读取当前数据
    with open('assets/js/poems-data.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    json_start = content.find('[')
    json_end = content.rfind(']') + 1
    json_str = content[json_start:json_end]
    poems_data = json.loads(json_str)
    
    # 找出还没有 Pexels 图片的诗歌
    remaining_poems = []
    for poem in poems_data:
        if poem['image'] == "assets/images/image-haizi.jpg":
            remaining_poems.append(poem)
    
    print(f"剩余需要处理 {len(remaining_poems)} 首诗歌")
    
    if not remaining_poems:
        print("🎉 所有诗歌都已有精美图片！")
        return
    
    fetcher = PoeticImageFetcher()
    
    # 处理剩余诗歌
    for i, poem in enumerate(remaining_poems, 1):
        print(f"\n[{i}/{len(remaining_poems)}] 处理: {poem['title']}")
        
        try:
            image_url = fetcher.get_image_url_for_poem(poem['title'])
            poem['image'] = image_url
            
            # 增加延迟避免API限制
            delay = random.uniform(3.0, 6.0)
            time.sleep(delay)
            
            # 每5首保存一次
            if i % 5 == 0:
                save_poems_data(poems_data)
                print(f"✅ 已保存前 {i} 首诗歌数据")
                time.sleep(10)  # 额外休息
                
        except Exception as e:
            print(f"处理《{poem['title']}》时出错: {e}")
            continue
    
    # 最终保存
    save_poems_data(poems_data)
    print(f"\n🎉 完成！所有 207 首诗歌都有精美图片了！")

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
    finish_remaining_images()