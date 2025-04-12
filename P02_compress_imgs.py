import os
from PIL import Image

# 原图文件夹路径
input_folder = r"C:\MyPython\CaptureVedioPics\output\2傅里叶"
# 压缩后图片保存的文件夹
output_folder = os.path.join(input_folder, "compressed")
# 设置压缩后宽或高的最大值（单位：像素）
max_size = 300  # 例如将最大边长压缩到不超过400像素

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 遍历文件夹中的所有图片
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with Image.open(input_path) as img:
            # 保持等比例缩放，最大宽/高为 max_size
            img.thumbnail((max_size, max_size))
            img.save(output_path)

print("图片压缩完成，保存于：", output_folder)
