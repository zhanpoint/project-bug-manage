from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


# 图片验证码由一些验证码+干扰点+干扰线+干扰圆圈组成
def image_code(width=120, height=30, char_length=6, font_file='static/Monaco.ttf', font_size=25):
    code = []
    # 创建一个新图片
    img = Image.new(mode='RGB', color=(255, 255, 255), size=(width, height))
    # 创建一个画笔对象,并绑定到图片上img上
    draw = ImageDraw.Draw(img, mode='RGB')

    def random_char():
        return chr(random.randint(65, 90))  # 将65~90的ASCII码转换为字符

    def random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # ImageFont.truetype返回TrueType字体文件
    font = ImageFont.truetype(font=font_file, size=font_size)
    for i in range(char_length):
        char = random_char()
        code.append(char)
        # 计算每个字符在图片上的横向位置和纵向位置
        x, y = i * width / char_length, random.randint(0, 4)
        # font 为TrueType字体文件，fill为RGB模式字体颜色
        draw.text((x, y), char, font=font, fill=random_color())

    # 写干扰点
    for i in range(40):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), fill=random_color())

    # 写干扰圆圈
    for i in range(40):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), fill=random_color())
        # draw.arc绘制一个弧形，弧形的起点和终点由(x,y)和(x+4,y+4)确定，角度范围是从0度到90度
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=random_color())

    # 画干扰直线
    for i in range(5):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=random_color())

    # ImageFilter.EDGE_ENHANCE_MORE 滤镜增强图片的边缘效果
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)


if __name__ == '__main__':
    image_object, code_str = image_code()

    # 以二进制写入模式 (wb) 打开文件code.png，并以png格式保存图片对象到code.png，然后自动关闭文件
    # file = open('code.png', 'wb')
    # image_object.save(file, format='png')
    # file.close()
    # 效果同上
    # with open('code.png', 'wb') as file:
    #     image_object.save(file, format='png')
