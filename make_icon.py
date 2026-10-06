"""
生成 Minecraft 安装器的 exe 图标 icon.ico
样式: 深蓝圆角外框 + 像素化草地绿方块 + 白色下箭头
运行: python3 make_icon.py
作者: weijianyu
"""

import random

from PIL import Image, ImageDraw

SIZE = 256
image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# 1. 深蓝灰圆角外框
draw.rounded_rectangle([4, 4, 252, 252], radius=44, fill=(45, 58, 76, 255))

# 2. 内部亮绿色方块
draw.rounded_rectangle([18, 18, 238, 238], radius=26, fill=(76, 175, 80, 255))

# 3. 像素化草地纹理(小方格随机深浅绿,模拟 MC 草地)
greens = [
    (56, 142, 60, 255),   # 深绿
    (67, 160, 71, 255),
    (76, 175, 80, 255),   # 基色
    (88, 193, 92, 255),
    (102, 208, 104, 255), # 亮绿
    (129, 212, 118, 255),
]
random.seed(42)
cell = 16
for y in range(22, 238, cell):
    for x in range(22, 238, cell):
        draw.rectangle([x, y, x + cell - 1, y + cell - 1],
                       fill=random.choice(greens))

# 4. 白色下箭头(带轻微阴影)
shadow = [(134, 63), (184, 113), (164, 113), (164, 179),
          (104, 179), (104, 113), (84, 113)]
arrow = [(128, 56), (178, 106), (158, 106), (158, 172),
         (98, 172), (98, 106), (78, 106)]
draw.polygon(shadow, fill=(0, 0, 0, 90))
draw.polygon(arrow, fill=(255, 255, 255, 255))

# 5. 保存图标(多尺寸 ico + 预览用 png)
image.save("icon.ico", sizes=[(16, 16), (24, 24), (32, 32),
                              (48, 48), (64, 64), (128, 128), (256, 256)])
image.save("icon.png")
print("图标生成完成: icon.ico / icon.png")
