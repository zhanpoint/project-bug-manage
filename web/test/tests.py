from PIL import Image, ImageDraw

# 创建一个新图像
img = Image.new(mode='RGB', color=(255, 255, 255), size=(120, 30))

# 将图像保存到文件
img.save('code.png')

# 在指定图片上创建画笔
draw = ImageDraw.Draw(img)

#
