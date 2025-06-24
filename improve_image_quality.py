import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import time
import random

# 加载环境变量
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
        
        # 直接意象类（有明确物象的）
        direct_imagery = {
            # 自然景观
            "面朝大海，春暖花开": "ocean waves horizon spring flowers peaceful",
            "七月不远": "summer lake water peaceful reflection",
            "七月的大海": "ocean waves blue summer peaceful",
            "大海": "ocean waves vast blue peaceful",
            "海": "ocean sea waves blue serene",
            "海上": "ocean seascape waves blue vast",
            "海水没顶": "ocean waves underwater blue",
            "海滩上为女士算命": "beach ocean waves sand peaceful",
            "湖泊": "lake water reflection peaceful calm",
            "河流": "river stream flowing water nature",
            "山脉": "mountains peaks landscape majestic",
            "东方山脉": "mountains sunrise peaks golden",
            "喜马拉雅": "snow mountains peaks majestic",
            "草原": "grassland vast green peaceful",
            "大草原": "grassland prairie wide peaceful",
            "黄金草原": "golden grassland sunset peaceful",
            "沙漠": "desert dunes golden peaceful",
            "阿拉伯": "desert dunes golden sand",
            "敦煌": "desert ancient dunes golden",
            
            # 植物花卉
            "花": "flowers colorful beautiful delicate",
            "梅花": "white blossoms winter delicate",
            "桃花": "pink blossoms spring beautiful",
            "菊花": "chrysanthemum golden autumn",
            "莲花": "lotus pink water peaceful",
            "玫瑰花": "roses red beautiful romantic",
            "山楂树": "white blossoms tree peaceful",
            "麦地": "wheat field golden harvest",
            "五月的麦地": "wheat field golden may",
            "熟了麦子": "golden wheat field harvest",
            "果园": "orchard trees blossoms peaceful",
            "葡萄园": "vineyard green peaceful",
            
            # 动物
            "天鹅": "white swan elegant water",
            "鸟": "bird flying sky freedom",
            "单翅鸟": "bird flying sky freedom",
            "马": "horse running field freedom",
            "鱼": "fish swimming water peaceful",
            "妻子和鱼": "water fish peaceful swimming",
            "木鱼儿": "fish water peaceful swimming",
            "公鸡": "rooster morning sunrise farm",
            "龙": "clouds sky mystical powerful",
            "抱着白虎走过海洋": "ocean waves powerful mystical",
            
            # 天象
            "太阳": "sun bright golden rays",
            "阿尔的太阳": "sun bright golden provence",
            "夏天的太阳": "sun bright summer golden",
            "月": "moon night silver peaceful",
            "月亮": "moon night silver calm",
            "星": "stars night sky cosmic",
            "云": "clouds sky white peaceful",
            "雨": "rain drops peaceful nature",
            "我请求：雨": "rain drops gentle peaceful",
            "雪": "snow white winter peaceful",
            "风": "wind movement nature peaceful",
            "光": "sunlight rays golden peaceful",
            "日光": "sunlight bright golden peaceful",
            "日出": "sunrise golden peaceful morning",
            
            # 季节时间
            "春天": "spring flowers green peaceful",
            "春": "spring blossoms green peaceful",
            "夏": "summer golden warm peaceful",
            "秋": "autumn golden leaves peaceful",
            "秋天": "autumn golden orange peaceful",
            "冬": "winter snow white peaceful",
            "黎明": "dawn sunrise golden peaceful",
            "拂晓": "dawn morning light peaceful",
            "黄昏": "sunset golden peaceful evening",
            "夜": "night stars peaceful dark",
            "夜晚": "night stars peaceful calm",
            "印度之夜": "night stars peaceful mystical",
            "中午": "noon bright sun peaceful",
            "正午": "noon bright golden peaceful",
            
            # 建筑空间
            "村庄": "village countryside peaceful rural",
            "村": "village peaceful countryside",
            "两座村庄": "village peaceful countryside",
            "九首诗的村庄": "village peaceful countryside",
            "城里": "city peaceful urban soft",
            "房屋": "house peaceful architecture soft",
            "门关户闭": "door peaceful quiet solitude",
            "家乡": "countryside peaceful nostalgic",
            
            # 水相关
            "但是水、水": "water peaceful flowing calm",
            "一滴水中的黑夜": "water drop night peaceful",
        }
        
        # 抽象概念类（用诗意的抽象意象）
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
            "幸福的一日": "person peaceful happy nature",
            "活在珍贵的人间": "person peaceful nature grateful",
            "美丽": "flowers peaceful beautiful nature",
            "为了美丽": "flowers peaceful beautiful delicate",
            
            # 文学人物（用相关意象）
            "给托尔斯泰": "birch trees peaceful russian landscape",
            "给卡夫卡": "mysterious door peaceful urban",
            "给安徒生": "fairy tale forest peaceful magical",
            "给萨福": "sea cliff peaceful romantic",
            "荷尔德林": "german landscape peaceful romantic",
            "但丁来到此时此地": "path mysterious peaceful journey",
            "莫扎特在《安魂曲》中说": "piano keys peaceful classical",
            "梭罗这人有脑子": "forest pond peaceful contemplation",
            "尼采，你使我想起悲伤的热带": "mountain peak philosophical",
            
            # 诗歌创作
            "诗歌": "feather writing peaceful artistic",
            "诗": "paper writing peaceful artistic",
            "诗集": "books peaceful artistic knowledge",
            "诗学：一份提纲": "writing paper peaceful artistic",
            "半截的诗": "paper torn peaceful artistic melancholy",
            "叙事诗": "storytelling peaceful artistic",
            "四行诗": "writing peaceful minimalist artistic",
            "十四行": "roses romantic peaceful classical",
            "歌或哭": "person emotional peaceful expression",
            "民间艺人": "hands crafting peaceful traditional",
            
            # 死亡主题（用安详的意象）
            "死亡": "dove flying peaceful heaven",
            "自杀者之歌": "dove peaceful white heaven",
            "土地·忧郁·死亡": "dove peaceful field heaven",
            
            # 神秘哲学
            "写给脖子上的菩萨": "lotus peaceful meditation spiritual",
            "莲界慈航": "lotus peaceful spiritual water",
            "早祷与枭": "dawn peaceful spiritual meditation",
            "打钟": "temple bell peaceful spiritual",
            
            # 人物关系
            "主人": "person peaceful contemplative solitary",
            "女孩子": "young woman peaceful flowers innocent",
            "你的手": "hands gentle peaceful caring",
            "你和桃花": "person peaceful pink blossoms",
            "得不到你": "solitary person peaceful melancholy",
            "妻子": "woman peaceful domestic gentle",
            "四姐妹": "women peaceful sisterhood harmony",
            
            # 物品器具
            "坛子": "ceramic jar peaceful traditional simple",
            "杯子": "ceramic cup peaceful simple traditional",
            "我的窗户里埋着一只为你祝福的杯子": "window light peaceful blessing",
            "煤堆": "mountain peaceful dark simple",
            "粮食": "grain peaceful abundance harvest",
            "船": "boat peaceful water journey",
            "木船": "wooden boat peaceful water traditional",
            "船尾之梦": "boat peaceful water dreamy",
            
            # 颜色意象
            "黑风": "dark clouds peaceful stormy dramatic",
            "八月　黑色的火把": "torch fire peaceful dramatic",
            "蓝姬的巢": "blue bird peaceful nest delicate",
            
            # 身体部位（用温柔意象）
            "哑脊背": "person peaceful contemplative back",
            "脖子": "woman peaceful gentle graceful",
            "脚": "bare feet peaceful walking nature",
            
            # 时间数字
            "七百年前": "ancient peaceful historical misty",
            "给1986": "peaceful nostalgic vintage soft",
            "明天醒来我会在哪一只鞋子里": "morning peaceful awakening soft",
            
            # 工作生活
            "农耕民族": "farming peaceful traditional rural",
            "北方门前": "door peaceful northern landscape",
            "让我把脚丫搁在黄昏中一位木匠的工具箱上": "sunset peaceful craftsmanship",
            "坐在纸箱上想起疯了的朋友们": "person peaceful contemplative nostalgic",
            
            # 抽象动作
            "跳跃者": "person jumping peaceful athletic graceful",
            "我们坐在一棵木头中": "tree peaceful meditation natural",
            "抱着": "embrace peaceful gentle caring",
            "哭泣": "person peaceful emotional release",
            "我感到魅惑": "person peaceful mystical attractive",
            "我，以及其他的证人": "group peaceful contemplative witness",
            
            # 地名（用相关意象）
            "九寨": "colorful lakes peaceful mystical",
            "昌平": "peaceful countryside rural chinese",
            "北方": "snow peaceful northern landscape",
            "南方": "warm peaceful southern landscape",
            "印度": "temple peaceful spiritual mystical",
            "青海": "lake blue peaceful plateau",
            "西藏": "mountains peaceful spiritual plateau",
            
            # 未分类
            "不幸": "dove peaceful white melancholy",
            "不要问我那绿色是什么": "green forest peaceful mysterious",
            "中国器乐": "traditional instruments peaceful cultural",
            "亚洲铜": "bronze peaceful ancient traditional",
            "从六月到十月": "seasons changing peaceful natural",
            "八月尾": "late summer peaceful golden",
            "八月之杯": "cup peaceful summer golden",
            "光棍": "solitary person peaceful simple",
            "公爵的私生女": "woman peaceful aristocratic melancholy",
            "冬天的雨": "rain winter peaceful gentle",
            "大自然": "forest peaceful natural beautiful",
            "太阳·土地篇": "sun earth peaceful powerful",
            "太阳·弑": "sun dramatic peaceful powerful",
            "太阳·弥赛亚": "sun divine peaceful powerful",
            "太阳·断头篇": "sun dramatic peaceful powerful",
            "太阳·诗剧": "sun theatrical peaceful powerful",
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
            return "water ocean lake peaceful blue calm"
        elif any(word in title for word in ["山", "峰", "岭", "岩", "坡"]):
            return "mountains landscape peaceful majestic"
        elif any(word in title for word in ["花", "草", "树", "林", "园", "叶"]):
            return "flowers nature peaceful beautiful delicate"
        elif any(word in title for word in ["夜", "晚", "暗", "黑", "星", "月"]):
            return "night stars peaceful calm mystical"
        elif any(word in title for word in ["春", "夏", "秋", "冬", "季"]):
            return "seasons nature peaceful beautiful"
        elif any(word in title for word in ["雨", "雪", "风", "云", "雾"]):
            return "weather peaceful atmospheric beautiful"
        elif any(word in title for word in ["太阳", "阳", "光", "日", "晨", "晓"]):
            return "sunlight peaceful golden bright"
        elif any(word in title for word in ["村", "乡", "家", "故", "门", "房"]):
            return "countryside peaceful rural nostalgic"
        elif any(word in title for word in ["鸟", "马", "鱼", "虫", "蝶"]):
            return "animal peaceful nature beautiful"
        elif any(word in title for word in ["爱", "情", "心", "恋", "思", "念"]):
            return "romantic peaceful beautiful sunset flowers"
        elif any(word in title for word in ["孤", "独", "寂", "静", "默"]):
            return "solitary person peaceful contemplation nature"
        elif any(word in title for word in ["死", "亡", "终", "末"]):
            return "dove white peaceful heaven serene"
        elif any(word in title for word in ["诗", "歌", "文", "书", "艺", "乐"]):
            return "artistic peaceful beautiful creative inspiration"
        elif any(word in title for word in ["给", "致", "献"]):
            return "gift peaceful beautiful meaningful"
        
        # 默认：诗意的抽象美景
        return "peaceful landscape beautiful serene poetic"
    
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
                    wait_time = (2 ** attempt) * 8
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
                    time.sleep(3)
        
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

def improve_all_images():
    """改进所有诗歌的图片质量"""
    
    # 读取当前数据
    with open('assets/js/poems-data.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    json_start = content.find('[')
    json_end = content.rfind(']') + 1
    json_str = content[json_start:json_end]
    poems_data = json.loads(json_str)
    
    print(f"开始改进所有 {len(poems_data)} 首诗歌的图片...")
    
    fetcher = PoeticImageFetcher()
    
    for i, poem in enumerate(poems_data, 1):
        print(f"\n[{i}/{len(poems_data)}] 处理: {poem['title']}")
        
        try:
            image_url = fetcher.get_image_url_for_poem(poem['title'])
            poem['image'] = image_url
            
            # 随机延迟避免API限制
            delay = random.uniform(2.0, 4.0)
            time.sleep(delay)
            
            # 每10首保存一次
            if i % 10 == 0:
                save_poems_data(poems_data)
                print(f"✅ 已保存前 {i} 首诗歌数据")
                time.sleep(5)  # 额外休息
                
        except Exception as e:
            print(f"处理《{poem['title']}》时出错: {e}")
            continue
    
    # 最终保存
    save_poems_data(poems_data)
    print(f"\n🎉 完成！已改进所有诗歌的图片质量")

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
    improve_all_images()