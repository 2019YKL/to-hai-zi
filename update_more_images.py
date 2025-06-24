from image_fetcher import update_poems_with_images

# 分批处理更多图片
if __name__ == "__main__":
    print("继续为更多诗歌获取图片...")
    # 可以调整数量，比如每次处理30首
    update_poems_with_images(max_poems=50)