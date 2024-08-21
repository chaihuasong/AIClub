"""
https://ai-bot.cn/daily-ai-news/
counter=1; for file in *.png; do base=$(basename "$file" .png) new_name=$(printf "%d" "$counter") new_name="$new_name.png" mv -v -- "$file" "$new_name" ((counter++)) done
"""

import re
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random
import shutil

def add_text_to_image(image_path, title, subtitle_content_pairs, output_image_path,
                      title_font_size=32, subtitle_font_size=24, text_font_size=20,
                      text_color=(255, 255, 255), bg_color=(0, 0, 0, 128),
                      padding=22, line_spacing=15, max_line_length=56, content_max_line_length=63):
    # 打开背景图片
    image = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))

    # 创建一个可以在透明图层上绘制的对象
    draw = ImageDraw.Draw(overlay)

    # 加载字体
    title_font = ImageFont.truetype("STHeiti Medium.ttc", title_font_size)
    subtitle_font = ImageFont.truetype("STHeiti Medium.ttc", subtitle_font_size)
    text_font = ImageFont.truetype("Hiragino Sans GB.ttc", text_font_size)

    # 获取图片尺寸
    image_width, image_height = image.size

    # 处理标题文本
    title_lines = re.findall(f'.{{1,{max_line_length}}}', title)
    title_height = sum(draw.textbbox((0, 0), line, font=title_font)[3] for line in title_lines) + (len(title_lines) - 1) * line_spacing


    # 定义字符宽度函数
    def char_width(c):
        if '\u4e00' <= c <= '\u9fff':  # 判断是否为中文字符
            return 2
        return 1

        # 定义分割字符串函数

    def split_text(text, max_line_length):
        result = []
        current_line = ""
        current_length = 0
        for char in text:
            char_len = char_width(char)
            if current_length + char_len <= max_line_length:
                current_line += char
                current_length += char_len
            else:
                result.append(current_line)
                current_line = char
                current_length = char_len
        result.append(current_line)  # 添加最后一行
        return result

        # 处理小标题和正文内容

    processed_pairs = []
    for subtitle, content in subtitle_content_pairs:
        subtitle_lines = split_text(subtitle, max_line_length)
        content_lines = split_text(content, content_max_line_length)
        processed_pairs.append((subtitle_lines, content_lines))


        # 计算所有文本的总高度
    total_text_height = title_height + padding + sum(
        sum(draw.textbbox((0, 0), line, font=subtitle_font)[3] for line in subtitle_lines) +
        sum(draw.textbbox((0, 0), line, font=text_font)[3] for line in content_lines) +
        2 * line_spacing + line_spacing  # 为每个内容结束后增加行间距
        for subtitle_lines, content_lines in processed_pairs
    ) + padding

    # 设置文本位置（垂直居中）
    current_y = (image_height - total_text_height) / 2 - line_spacing * 4

    # 计算背景矩形的大小
    max_text_width = max(
        max(draw.textbbox((0, 0), line, font=title_font)[2] for line in title_lines),
        *[max(
            max(draw.textbbox((0, 0), line, font=subtitle_font)[2] for line in subtitle_lines),
            max(draw.textbbox((0, 0), line, font=text_font)[2] for line in content_lines)
        ) for subtitle_lines, content_lines in processed_pairs]
    )
    bg_width = max_text_width + 2 * padding
    bg_height = total_text_height * 3 / 2 - len(processed_pairs) * padding * 2 + line_spacing

    # 绘制半透明背景矩形
    bg_x = (image_width - bg_width) / 2
    draw.rectangle([bg_x, current_y - padding, bg_x + bg_width, current_y + bg_height],
                   fill=bg_color)

    # 绘制标题
    for line in title_lines:
        draw.text((bg_x + padding, current_y), line, fill=text_color, font=title_font)
        current_y += draw.textbbox((0, 0), line, font=title_font)[3] + line_spacing

    current_y += padding

    # 绘制小标题和正文内容
    for subtitle_lines, content_lines in processed_pairs:
        for line in subtitle_lines:
            draw.text((bg_x + padding, current_y), line, fill=text_color, font=subtitle_font)
            current_y += draw.textbbox((0, 0), line, font=subtitle_font)[3] + line_spacing
        for line in content_lines:
            draw.text((bg_x + padding, current_y), line, fill=text_color, font=text_font)
            current_y += draw.textbbox((0, 0), line, font=text_font)[3] + line_spacing
        current_y += line_spacing  # 每个内容结束后添加额外的行间距

    # 将透明图层与背景图像合并
    combined = Image.alpha_composite(image, overlay).convert("RGB")

    # 保存带有文本和半透明背景的图片
    combined.save(output_image_path)

# 获取当天日期并格式化为 YYYY-MM-DD
today_date = datetime.now().strftime("%Y-%m-%d")

# 构建标题
title = f"{today_date} 前沿播报"

# 小标题和正文内容的动态输入
subtitle_content_pairs = [
    ("全球最强数学大模型 Qwen2-Math 发布人人可玩Demo",
     "阿里千问大模型团队发布了 Qwen2-Math 的体验Demo，HuggingFace在线可玩。惊喜的是，如果嫌输入数学公式比较麻烦，可以把想问的题截图or扫描，上传即可解题。试玩界面的OCR功能，由阿里千问大模型团队Qwen2-VL提供支持；数学推理能力，由Qwen2-Math支持。"),

    ("Luma Dream Machine v1.5版本发布，更快、更真、更清晰",
     "据 Luma AI 官方消息， Luma Dream Machine v1.5版本已经在近日发布，在视频生成方面获得巨大改善。据Luma官方表示，Luma Dream Machine V1.5版本在视频生成方面取得了显著进步，不仅提升了视频的质量，更缩短了生成时间。现在，用户可以在更短的时间内，得到更高质量的视频作品。"),

    ("AMD 宣布49亿美元收购服务器制造商 ZT Systems 以挑战英伟达",
     "AMD 宣布同意以75%现金和 25%股票交易方式收购服务器制造商 ZT Systems，交易价值为49亿美元，以增加数据中心技术。ZT Systems 将成为 AMD 数据中心解决方案业务集团的一部分。ZT Systems 在过去12个月的收入超过100亿美元。"),

    ("通义千问宣布启用新域名\"tongyi.ai\"，网页版聊天新增深度搜索功能",
     "阿里大语言模型“通义千问”今日宣布启用新域名“tongyi.ai”，并带来多项新功能。网页版聊天新增深度搜索功能；App 图片微动效支持多尺寸图片；App 自定义唱演支持 3:4 画幅（原先 1:1）。")
]

# 生成1到80之间的随机整数
random_number = random.randint(1,  80)
print(random_number)
# 背景图片路径和输出图片路径
background_img_path = '/Users/chaihuasong/Documents/AI/resources/pictures/' + str(random_number) + ".png"
output_image_path = '../../learn/data/zeekr/img/' + str(random_number) + ".png"

print(output_image_path)
# 在背景图片上添加文本并保存
add_text_to_image(background_img_path, title, subtitle_content_pairs, output_image_path)


# 拷贝文件
shutil.move(output_image_path,  '/Users/chaihuasong/Documents/AI/resources/out/' + str(random_number) + ".png")