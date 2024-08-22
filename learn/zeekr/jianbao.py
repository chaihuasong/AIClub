"""
https://ai-bot.cn/daily-ai-news/
counter=1; for file in *.png; do base=$(basename "$file" .png); new_name=$(printf "%d" "$counter"); new_name="$new_name.png"; mv -v -- "$file" "$new_name"; ((counter++)); done
"""

import re
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random
import shutil
import os

def add_text_to_image(image_path, title, subtitle_content_pairs, output_image_path,
                      title_font_size=32, subtitle_font_size=24, text_font_size=20,
                      text_color=(255, 255, 255), bg_color=(0, 0, 0, 128),
                      padding=18, line_spacing=15, max_line_length=56, content_max_line_length=64):
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
    current_y = (image_height - total_text_height) / 2 - line_spacing * (len(processed_pairs) + 2) - title_height / 2 - 8

    # 计算背景矩形的大小
    max_text_width = max(
        max(draw.textbbox((0, 0), line, font=title_font)[2] for line in title_lines),
        *[max(
            max(draw.textbbox((0, 0), line, font=subtitle_font)[2] for line in subtitle_lines),
            max(draw.textbbox((0, 0), line, font=text_font)[2] for line in content_lines)
        ) for subtitle_lines, content_lines in processed_pairs]
    )
    bg_width = max_text_width + 2 * padding
    bg_height = total_text_height * 3 / 2 - len(processed_pairs) * 42 + line_spacing

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
    ("Midjourney网页版全面开放，每人每天25次免费试用机会",
     "Midiourney 网页版现在对所有人开放了，每位新用户每天提供 Midjourney 最先进模型V 6.125次试用机会。用戶可使用Discord或Google账号登录，并在账户设置中合并两个平台的登录信息，确保历史记录同步。"),

    ("百度、商汤、智谱前三，IDC首次发布大模型平台及应用市场份额报告",
     "国际数据公司 （IDC）于今日首次发布了《中国大模型平台市场份额，2023：大模型元年—初局》。数据显示，2023年中国大模型平台及相关应用市场规模达 17.65亿元人民币。受益于多年来在 AI领域的大力投入以及大模型的早期投入，百度智能云在2023年大模型市场规模达 3.5亿元人民币，位居市场第一，市场份额达19.9%；商汤科技位居市场第二，市场份额达 16.0%；智谱 AI 则是2023年初创企业中的胜出者，位居市场第三"),

    ("泡茶、弹琴、练咏春，星尘智能发布 AI 机器人助理 Astribot S1",
     "Astribot 星尘智能8 月19日发布了 AI机器人助理 Astribot S1，支持泡茶、做饭、弹琴、练咏春拳等，还能 VR遥控。据星尘智能介绍，Astribot S1采用了刚柔耦合传动机构，自主研发关键零部件，搭载软硬件一体化系统架构。"),

    ("微软发布Phi-3.5系列模型，性能超越Gemini 1.5 Flash与GPT-40",
     "Phi-3.5 是微软推出的新一代AI模型系列，包含 Phi-3.5-mini-instruct、Phi-3.5-MoE-instruct 和 Phi-3.5-vision-instruct 三个版本，分别针对轻量级推理、混合专家系统和多模态任务设计。Phi-3.5采用MIT开源许可证，具有不同参数规模，支持128k上下文长度，优化了多语言处理和多轮对话能力，在基准测试中性能表现超越了GPT4O、Llama 3.1、Gemini Flash等同类模型。"),
]

# 生成1到80之间的随机整数
# random_number = random.randint(1,  80)
# print(random_number)
# 背景图片路径和输出图片路径
background_img_path = '/Users/chaihuasong/Documents/AI/resources/pic3/'
output_image_path = '../../learn/data/zeekr/img/'

# 遍历文件夹
for filename in os.listdir(background_img_path):
    if filename.endswith('.png'):
        full_path = os.path.join(background_img_path, filename)
        output_full_path = os.path.join(output_image_path, filename)
        print(full_path)
        # 在背景图片上添加文本并保存
        add_text_to_image(full_path, title, subtitle_content_pairs, output_full_path)
        # 移动文件
        shutil.move(output_full_path, '/Users/chaihuasong/Documents/AI/resources/out/1/')