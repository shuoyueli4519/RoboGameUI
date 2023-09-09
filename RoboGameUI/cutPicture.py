from PIL import Image

# 打开图片
image = Image.open('./Source//Pic/Title.png')

# 获取图片的宽度和高度
width, height = image.size

# 定义要截取的区域
left = int(width * 0)  # 左边界，取宽度的25%
top = int(height * 0)  # 上边界，取高度的25%
right = int(width * 0.75)  # 右边界，取宽度的75%
bottom = int(height * 1)  # 下边界，取高度的75%

# 截取图片的一部分
cropped_image = image.crop((left, top, right, bottom))

# 缩小截取后的图片
new_width = int((right - left) * 0.5)  # 新的宽度为截取宽度的一半
new_height = int((bottom - top) * 0.5)  # 新的高度为截取高度的一半
resized_image = cropped_image.resize((new_width, new_height))

# 保存截取并缩小后的图片
resized_image.save('output_image.png')