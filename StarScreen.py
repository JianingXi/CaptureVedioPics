import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# 参数设置
width, height = 1920, 1080
num_stars = 300
T = 60  # 帧数和周期一致

# 星星位置和大小
np.random.seed(42)
x = np.random.rand(num_stars) * width
y = np.random.rand(num_stars) * height
radii_base = np.random.rand(num_stars) * 1.8 + 1

# 关键：使用整周期频率和相位，确保闭环
n_values = np.random.randint(1, 6, size=num_stars)  # n_i ∈ [1, 5]
ω = 2 * np.pi * n_values / T
k_values = np.random.randint(0, T, size=num_stars)
φ = 2 * np.pi * k_values / T

# 虚空背景生成函数
def generate_background():
    base = Image.new("RGB", (width, height), (13, 0, 25))
    overlay = Image.new("RGB", (width, height))
    for y_ in range(height):
        for x_ in range(width):
            dx = (x_ - width/2)
            dy = (y_ - height/2)
            d = (dx*dx + dy*dy)**0.5
            fade = int(20 + 30 * np.sin(d / 150))  # 紫色晕染
            overlay.putpixel((x_, y_), (fade, 0, fade*2))
    return Image.blend(base, overlay, alpha=0.2).filter(ImageFilter.GaussianBlur(radius=2))

# 构造帧图像
frames = []
for frame in range(T):
    t = frame
    brightness = (np.cos(ω * t + φ) + 1) / 2 * 200 + 55
    sizes = (np.cos(ω * t + φ) + 1.5) * radii_base
    brightness = np.clip(brightness, 60, 255).astype(int)

    img = generate_background()
    draw = ImageDraw.Draw(img)
    for i in range(num_stars):
        cx, cy = x[i], y[i]
        r = sizes[i]
        b = brightness[i]
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(b, b, b))

    frames.append(img)

# 保存为闭环 GIF
frames[0].save("star.gif", save_all=True, append_images=frames[1:], duration=50, loop=0)
