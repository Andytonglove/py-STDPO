import json
from math import floor
import random
import psycopg2
from PIL import Image, ImageDraw

# 本程序用以实现PostGIS功能函数并进行测试

# 函数1：输入任意一个国家，统计出这个国家的县级行政区的数量，
# 并统计这个国家中县级行政区面积最大的三个，打印出名字和面积值


def get_county_count(country):
    # 连接数据库创建游标
    conn = psycopg2.connect(database="test", user="postgres",
                            password="******", host="localhost", port="5432")

    cur = conn.cursor()
    # 查询县级行政区数量，获取结果
    sql_count = "SELECT COUNT(*) FROM gadm404 WHERE name_0 = %s"
    cur.execute(sql_count, (country,))
    result = cur.fetchone()

    # 查询这个国家中县级行政区面积最大的三个，并保存结果
    sql_area = "SELECT name_3, ST_Area(geom) FROM gadm404 WHERE name_0 = %s ORDER BY ST_Area(geom) DESC LIMIT 3"
    cur.execute(sql_area, (country,))
    # 保存结果
    area_result = cur.fetchall()

    # 关闭游标连接
    cur.close()
    conn.close()

    # 打印这个国家的县级行政区数量与三个最大面积行政区
    print("国家'"+str(country)+"'的县级行政区数量为：" + str(result[0]))
    print("国家'"+str(country)+"'的县级行政区面积最大的三个分别为：\n" +
          str(area_result[0][0])+"，面积为："+str(area_result[0][1])+"平方千米\n" +
          str(area_result[1][0])+"，面积为："+str(area_result[1][1])+"平方千米\n" +
          str(area_result[2][0])+"，面积为："+str(area_result[2][1])+"平方千米\n")

    # 返回数量结果
    return result[0]


# 函数2：输入任意一个国家，统计出这个国家在地域上邻接的其它国家


def get_neighbor_countries(country):
    # 连接数据库
    conn = psycopg2.connect(database="test", user="postgres",
                            password="******", host="localhost", port="5432")
    # 创建游标
    cur = conn.cursor()

    # 查询任意一个国家的县级行政区的所有邻接国家
    sql_neighbor = "SELECT DISTINCT gadm404.name_0 \
                    FROM gadm404,(SELECT geom,name_0 FROM gadm404 WHERE name_0 = %s) AS t\
                    WHERE ST_Touches ( gadm404.geom, t.geom ) AND gadm404.name_0 != %s\
                    "
    cur.execute(sql_neighbor, (country, country))
    result = cur.fetchall()

    cur.close()
    conn.close()
    # 返回并打印结果
    print("国家'"+str(country)+"'的邻接国家为：")
    for i in range(len(result)):
        print(result[i][0])
    print("\n")
    return result


# 函数3：实现一个数据处理函数，函数接受三个参数：国家名，像素分辨率，输出目录。
# 输入任意一个国家，将这个国家的数据按指定像素分辨率进行渲染，然后按256x256像素大小的索引格网，切片输出

def render_country_slice(country, resolution, output_dir):
    # 连接数据库
    conn = psycopg2.connect(database="test", user="postgres",
                            password="******", host="localhost", port="5432")
    # 创建游标
    cur = conn.cursor()

    # 确定区域范围
    sql_range = "SELECT max(st_xmax(geom)) AS maxx,min(st_xmin(geom)) AS minx,\
                max(st_ymax(geom)) AS maxy,min(st_ymin(geom)) AS miny\
                FROM gadm404 WHERE name_0=%s"
    cur.execute(sql_range, (country,))
    ranging = cur.fetchall()  # 注意命名，不能重写range！
    print(ranging)

    # 获取x轴和y轴的最值和坐标范围
    x_max = ranging[0][0]
    x_min = ranging[0][1]
    y_max = ranging[0][2]
    y_min = ranging[0][3]
    x_dist = x_max - x_min
    y_dist = y_max - y_min
    # 计算输出的图片大小
    x_size = int(x_dist / resolution)
    y_size = int(y_dist / resolution)

    # 绘制图像空白图层等待填充
    img = Image.new('RGB', (x_size, y_size), "white")
    # 创建一个画笔
    draw = ImageDraw.Draw(img)

    # 以GeoJson形式获取县级行政区的数据
    sql_geojson = "SELECT ST_AsGeoJSON(geom),uid FROM gadm404 WHERE name_0 = %s"
    cur.execute(sql_geojson, (country,))
    geojson_list = cur.fetchall()  # 获取结果为字符串形式

    # 开始绘制
    for i in range(len(geojson_list)):
        # 将数据转为字典形式
        geojson_dict = json.loads(geojson_list[i][0])
        # 获取几何图形上的多边形
        polygon = geojson_dict['coordinates'][0][0]
        # 创建绘制的坐标像素集合
        pixel_list = []
        # 根据像素分辨率计算px、py
        for j in range(len(polygon)):
            px = int(x_size-((x_max - polygon[j][0]) / resolution))
            py = int((y_max-polygon[j][1]) / resolution)
            # 将像素坐标添加到像素集合中
            pixel_list.append((px, py))
        # 直接在循环内，绘制多边形，边缘为黑色，填充随机颜色
        draw.polygon(pixel_list, outline="rgb(0, 0, 0)",
                     fill="rgb(%d, %d, %d)" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        # 保存图片
        img.save(output_dir + country + '.jpg')

    # 定义切分尺寸和切分的图片
    slice_size = 256
    slice_img = Image.open(output_dir + country + '.jpg')

    # 切分图片并生成参考文件
    for i in range(0, x_size, slice_size):
        for j in range(0, y_size, slice_size):
            # 计算切片图片的四角坐标，分别为左上角、右上角、右下角、左下角
            x1 = i+slice_size if i+slice_size < x_size else x_size-1
            y1 = j+slice_size if j+slice_size < y_size else y_size-1
            # 输出切片影像的数据命名用索引方式
            output_i = str(floor((i+slice_size)/slice_size))
            output_j = str(floor((j+slice_size)/slice_size))
            # 切片，并保存
            slice_img.crop((i, j, x1, y1)).save(
                output_dir + country + '_' + output_i + '-' + output_j + '.jpg')
            # 写入参考文件：对应的坐标配准文件jgw
            with open(output_dir + country + '_' + output_i + '-' + output_j + '.jgw', 'w') as f:
                # 六个参数：x方向像素分辨率、x方向旋转角度、y方向旋转角度、y方向像素分辨率、左上角像素坐标x、左上角像素坐标y
                x2 = x_min+resolution*i
                y2 = y_max-resolution*j
                f.write('%f\n%f\n%f\n%f\n%f\n%f\n' %
                        (resolution, 0.00, 0.00, -resolution, x2, y2))

    # 关闭游标和连接
    cur.close()
    conn.close()
    print('Done!')


# 测试上述函数，这里用不同国家测试至少2次
get_county_count("China")
get_county_count("France")

get_neighbor_countries("China")
get_neighbor_countries("France")

# 函数三测试，这里以中国、日本为例
render_country_slice("China", 0.1, "")
render_country_slice("China", 0.2, "")
render_country_slice("Japan", 0.1, "")
render_country_slice("Japan", 0.2, "")
