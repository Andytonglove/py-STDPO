import numpy as np
from linecache import getline


def floodFill(c, r, mask):
    # cells already filled
    filled = set()
    # cells to fill
    fill = set()
    fill.add((c, r))
    width = mask.shape[1]-1
    height = mask.shape[0]-1
    # Our output inundation array
    flood = np.zeros_like(mask, dtype=np.int8)
    # Loop through and modify the cells which
    # need to be checked.
    while fill:
        # Grab a cell
        x, y = fill.pop()
        if y == height or x == width or x < 0 or y < 0:
            # Don't fill
            continue
        if mask[y][x] == 1:
            # Do fill
            flood[y][x] = 1
            filled.add((x, y))
            # Check neighbors for 1 values
            west = (x-1, y)
            east = (x+1, y)
            north = (x, y-1)
            south = (x, y+1)
            if west not in filled:
                fill.add(west)
            if east not in filled:
                fill.add(east)
            if north not in filled:
                fill.add(north)
            if south not in filled:
                fill.add(south)
    return flood


def coord2pixel(coordx, coordy, ncols, nrows, xllcorner, yllcorner, cellsize):
    # 从地理坐标计算得到像素坐标 函数
    sx = (int)((coordx-xllcorner)/cellsize)
    sy = (int)((coordy-yllcorner)/cellsize)
    return (int)(sx-1) if sx <= ncols else (int)(ncols-1), (int)(sy-1) if sy <= nrows else (int)(nrows-1)


source = "srtm.asc"
target = "srtm-flood.asc"

print("Opening image...")
img = np.loadtxt(source, skiprows=6)
print("Image opened")

# Parse the headr using a loop and
# the built-in linecache module
hdr = [getline(source, i) for i in range(1, 7)]
values = [float(h.split(" ")[-1].strip()) for h in hdr]
cols, rows, lx, ly, cell, nd = values
xres = cell
yres = cell * -1

# Starting point for the
# flood inundation
# 淹没中心点，这里通过地理坐标计算得到像素坐标
cx = 72.25
cy = 37.25
sx, sy = coord2pixel(cx, cy, cols, rows, lx, ly, cell)  # 原像素坐标：2582 2057

# 这里确定淹没高程，从种子点参数增加一定高度读出
filledval = img[sx][sy]+10
a = np.where(img < filledval, 1, 0)
print("Image masked")

# 开始计算淹没
print("Beginning flood fill")
fld = floodFill(sx, sy, a)
print("Finished Flood fill")

header = ""
for i in range(6):
    header += hdr[i]

print("Saving grid")
# Open the output file, add the hdr, save the array
with open(target, "wb") as f:
    f.write(bytes(header, 'UTF-8'))
    np.savetxt(f, fld, fmt="%1i")
print("Done!")
