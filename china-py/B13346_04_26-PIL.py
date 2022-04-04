from PIL import Image
from PIL import ImageDraw
import shapefile
import random

# 读入china.shp文件
r = shapefile.Reader("china.shp")
iwidth = 981
iheight = 752
shapes = r.shapes()
# 初始化
maxx = shapes[0].bbox[2]
minx = shapes[0].bbox[0]
maxy = shapes[0].bbox[3]
miny = shapes[0].bbox[1]
# 确定宽高比范围
for i in range(1, len(shapes)):
    maxx = shapes[i].bbox[2] if shapes[i].bbox[2] > maxx else maxx
    minx = shapes[i].bbox[0] if shapes[i].bbox[0] < minx else minx
    maxy = shapes[i].bbox[3] if shapes[i].bbox[3] > maxy else maxy
    miny = shapes[i].bbox[1] if shapes[i].bbox[1] < miny else miny
# 确定图片缩放比例
xdist = maxx - minx
ydist = maxy - miny
xratio = iwidth / xdist
yratio = iheight / ydist

# 输出图像初始化
img = Image.new("RGB", (iwidth, iheight), "white")
draw = ImageDraw.Draw(img)

# 循环处理多边形数据，修改为可以处理全部多边形
for i in range(0, len(shapes)):
    pixels = []
    for x, y in shapes[i].points:
        px = int(iwidth - ((maxx - x) * xratio))
        py = int((maxy - y) * yratio)
        pixels.append((px, py))
    # 渲染到图片中，为不同多边形赋不同颜色
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    draw.polygon(pixels, outline="rgb(203, 196, 190)",
                 fill="rgb(%d, %d, %d)" % (r, g, b))

img.save("china.png")
