"""
https://ai-bot.cn/daily-ai-news/
counter=1; for file in *.png; do base=$(basename "$file" .png); new_name=$(printf "%d" "$counter"); new_name="$new_name.png"; mv -v -- "$file" "$new_name"; ((counter++)); done
"""

import re
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
# import random
import shutil
import os

# 背景图片路径和输出图片路径
background_img_path = '/Users/chaihuasong/Documents/AI/resources/pic4/'
output_image_path = '../../learn/data/zeekr/img/'

def read_pairs_from_file(file_path):
    subtitle_content_pairs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        # 跳过空行
        while i < len(lines) and not lines[i].strip():
            i += 1

            # 检查是否已经到达文件末尾
        if i >= len(lines):
            break

            # 读取key行
        key = lines[i].strip()
        i += 1

        # 跳过key行后的空行
        while i < len(lines) and not lines[i].strip():
            i += 1

            # 检查是否已经到达文件末尾
        if i >= len(lines):
            break

            # 读取content行
        content = lines[i].strip()
        i += 1

        # 将key和content添加到pairs列表中
        subtitle_content_pairs.append((key, content))

    return subtitle_content_pairs

# 使用示例
file_path = 'data.txt'
subtitle_content_pairs = read_pairs_from_file(file_path)

def add_text_to_image(image_path, title, subtitle_content_pairs, output_image_path,
                      title_font_size=32, subtitle_font_size=24, text_font_size=20,
                      text_color=(255, 255, 255), bg_color=(0, 0, 0, 128),
                      padding=20, line_spacing=12, max_line_length=62, content_max_line_length=72):
    # 打开背景图片
    image = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))

    # 创建一个可以在透明图层上绘制的对象
    draw = ImageDraw.Draw(overlay)

    # 加载字体
    title_font = ImageFont.truetype("/Users/chaihuasong/Documents/AI/code/AIClub/learn/data/zeekr/ttf/lianxiangbold.ttf", title_font_size)
    subtitle_font = ImageFont.truetype("/Users/chaihuasong/Documents/AI/code/AIClub/learn/data/zeekr/ttf/lianxiangbold.ttf", subtitle_font_size)
    text_font = ImageFont.truetype("/Users/chaihuasong/Documents/AI/code/AIClub/learn/data/zeekr/ttf/lianxiang.ttf", text_font_size)

    # 获取图片尺寸
    image_width, image_height = image.size

    # 处理标题文本
    title_lines = re.findall(f'.{{1,{max_line_length}}}', title)
    title_height = sum(draw.textbbox((0, 0), line, font=title_font)[3] for line in title_lines) + (len(title_lines) - 1) * line_spacing


    # 定义字符宽度函数
    def char_width(c):
        # 常见的中文标点符号
        chinese_punctuations = {
            '，', '。', '！', '？', '；', '：', '“', '”', '‘', '’', '（', '）', '《', '》', '【', '】', '—', '…', '～', '、'
        }

        # 判断是否为中文字符或中文标点符号
        if '\u4e00' <= c <= '\u9fff' or c in chinese_punctuations:
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
    current_y = (image_height - total_text_height) / 2 - line_spacing * len(processed_pairs) - title_height / 2

    # 计算背景矩形的大小
    max_text_width = max(
        max(draw.textbbox((0, 0), line, font=title_font)[2] for line in title_lines),
        *[max(
            max(draw.textbbox((0, 0), line, font=subtitle_font)[2] for line in subtitle_lines),
            max(draw.textbbox((0, 0), line, font=text_font)[2] for line in content_lines)
        ) for subtitle_lines, content_lines in processed_pairs]
    )
    bg_width = max_text_width + 2 * padding
    bg_height = total_text_height * 3 / 2 - len(processed_pairs) * 50 + line_spacing

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

# 生成1到80之间的随机整数
# random_number = random.randint(1,  80)
# print(random_number)

dst_dir = '/Users/chaihuasong/Documents/AI/resources/out/' + today_date + '/'

# 创建新文件夹
os.makedirs(dst_dir, exist_ok=True)

# 遍历文件夹
for filename in os.listdir(background_img_path):
    if filename.endswith('.png'):
        full_path = os.path.join(background_img_path, filename)
        output_full_path = os.path.join(output_image_path, filename)
        print(full_path)
        # 在背景图片上添加文本并保存
        add_text_to_image(full_path, title, subtitle_content_pairs, output_full_path)
        # 移动文件
        shutil.move(output_full_path, dst_dir)