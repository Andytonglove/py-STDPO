from osgeo import gdal_array
import random

# 分类类别输入
print("请输入分类的类别数(5、10、15、20):")
cnt = input()

# Input file name (thermal image)
src = "GF1.jpg"

# Output file name
tgt = "GF1-classified-"+cnt+".jpg"

# Load the image into numpy using gdal
srcArr = gdal_array.LoadFile(src)

# Split the histogram into cnt bins as our classes
classes = gdal_array.numpy.histogram(srcArr, bins=int(cnt))[1]

# Color look-up table (LUT) - must be len(classes)+1.
# Specified as R, G, B tuples
lut = []
# 随机生成颜色列表参数
for i in range(len(classes)+1):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    lut.append([r, g, b])

# Starting value for classification
start = 1

# Set up the RGB color JPEG output image
rgb = gdal_array.numpy.zeros((3, srcArr.shape[0],
                              srcArr.shape[1], ), gdal_array.numpy.float32)

# Process all classes and assign colors
for i in range(len(classes)):
    mask = gdal_array.numpy.logical_and(start <= srcArr, srcArr <= classes[i])
    for j in range(len(lut[i])):
        rgb[j] = gdal_array.numpy.choose(mask, (rgb[j], lut[i][j]))
    start = classes[i]+1

# Save the image
output = gdal_array.SaveArray(rgb.astype(
    gdal_array.numpy.uint8), tgt, format="JPEG")
output = None
