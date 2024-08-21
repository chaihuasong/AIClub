"""
https://ai-bot.cn/daily-ai-news/
counter=1; for file in *.png; do base=$(basename "$file" .png); new_name=$(printf "%d" "$counter"); new_name="$new_name.png"; mv -v -- "$file" "$new_name"; ((counter++)); done
"""

import re
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random
import shutil

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
    current_y = (image_height - total_text_height) / 2 - line_spacing * 9 - 10

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
    ("谷歌开放 HeAR AI 模型 API:1亿条咳嗽声训练，辅助筛查、诊断和监测肺结核",
     "谷歌公司于8月19 日发布博文，宣布通过 Google Cloud API，目前已经向研究人员开放健康声学表征（HealthAcoustic Representations，简称 HeAR）AI 模型。谷歌 HeAR AI 模型可以帮助人类诊断疾病，可以通过分析人的咳嗽和呼吸，诊断出疾病。"),

    ("Salesforce推出 xGen-MM 开源多模态AI模型",
     "xGen-MM 是Salesforce推出的一款开源多模态AI模型，具有处理交错数据的能力，能同时理解和生成文本、图像等多种数据类型。xGen-MIM 通过学习大量的图片和文字信息，不仅在视觉语言任务上展现出强大的性能，还通过开源模型、数据集和微调代码库，促进模型能力的不断提升。"),

    ("OpenAI 开放GPT-40微调功能，企业可更轻松打造专属AI助手",
     "OpenAI 推出了一项新功能，允许企业客户使用自己的数据来定制其最强大的 AI 模型 GPT-40。此举旨在应对日益激烈的AI企业应用竞争，并满足企业对 AI投资回报的更高要求。通过微调，现有 AI 模型可以针对特定任务或领域进行优化。"),

    ("PICO发布“中国版Vision Pro”，搭载的AI芯片性能暴增800%",
     "8月20日下午，字节跳动旗下XR平台PICO推出首款MR混合现实一体机PICO 4 Ultra，硬件上搭载全新高通骁龙XR2 Gen2计算平台，拥有12GB超大内存，GPU性能相比前代XR1提升2.5倍，Al性能比XR1提升8倍。价格方面，PICO 4 Ultra消费者版本售价4299元，PICO 4 Ultra Enterprise（企业版）7499元，PICO体感追踪器售价399元一对，现已全面开启预售"),

    ("iPad上最强的绘画应用 Procreate，永远不会在其产品中引入生成式AI",
     "Procreate CEO James Cuda 宣布该应用将永不使用生成式AI技术，以保护艺术家免受其影响；Procreate 是一款受欢迎的iPad绘图应用，自2011年上线以来获得多个奖项，并广泛用于艺术和设计教育；尽管Procreate拒绝采用生成式Al，公司仍将继续使用传统的机器学习技术来优化应用功能。"),

    ("EliseAI 跻身纽约独角兽行列：D轮融资7500万美元、估值超10亿美元",
     "据VentureBeat官网报道，近日，房产科技公司 EliseAI宣布成功完成7500万美元D轮融资，此轮融资由知名风投公司 Sapphire Ventures 领投，新筹集的资金将主要用于扩充团队规模，推进产品研发。至此，EliseAI的估值超过10亿美元，成为了纽约最新的独角兽公司。")

]

# 生成1到80之间的随机整数
random_number = random.randint(1,  80)
print(random_number)
# 背景图片路径和输出图片路径
background_img_path = '/Users/chaihuasong/Documents/AI/resources/pic2/' + str(random_number) + ".png"
output_image_path = '../../learn/data/zeekr/img/' + str(random_number) + ".png"

print(output_image_path)
# 在背景图片上添加文本并保存
add_text_to_image(background_img_path, title, subtitle_content_pairs, output_image_path)


# 拷贝文件
shutil.move(output_image_path,  '/Users/chaihuasong/Documents/AI/resources/out/' + str(random_number) + ".png")