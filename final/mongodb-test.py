import pymongo

# 本程序用以实现MongoDB功能函数并进行测试


# 函数1：实现一个函数，给定一个经纬度坐标及编码长度，则生成一个geohash编码

def geohash_encode(latitude, longitude, precision):
    # 通过经纬度和给定的编码长度，计算出经纬度的编码
    __base32 = '0123456789bcdefghjkmnpqrstuvwxyz'  # 定义编码字符集
    lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)  # 定义纬度和经度的范围
    geohash = []  # 定义一个空列表，用来存放编码结果
    bits = [16, 8, 4, 2, 1]  # 定义编码长度
    bit = 0  # 定义一个变量，用来记录当前编码的位数
    ch = 0  # 定义一个变量，用来记录当前编码的字符
    even = True  # 定义一个变量，用来记录当前是否是偶数位
    while len(geohash) < precision:  # 当编码长度小于给定的编码长度时，循环编码
        if even:  # 当是偶数位时
            mid = (lon_interval[0] + lon_interval[1]) / 2
            if longitude > mid:  # 当经度大于经度范围的中间值时
                ch |= bits[bit]  # 将当前位置1
                lon_interval = (mid, lon_interval[1])  # 更新经度范围
            else:
                lon_interval = (lon_interval[0], mid)
        else:  # 当是奇数位时，同上
            mid = (lat_interval[0] + lat_interval[1]) / 2
            if latitude > mid:
                ch |= bits[bit]
                lat_interval = (mid, lat_interval[1])
            else:
                lat_interval = (lat_interval[0], mid)
        even = not even
        if bit < 4:  # 当位数小于4时，更新位数
            bit += 1
        else:  # 当位数大于等于4时，将当前字符添加到编码列表中，并更新位数
            geohash += __base32[ch]  # 添加字符到编码列表
            bit = 0
            ch = 0
    return ''.join(geohash)  # 返回编码结果


# 函数2：给定一个县级行政区名字，即可查询出某个县级行政区域，并将这几何边界用8位geohash编码数据组织


def get_geohash_by_name(name):
    # 连接数据库和集合
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    dblist = myclient.list_database_names()
    dbanme = "test"
    colname = "gadm404"

    if dbanme in dblist:
        print("数据库存在！")
        db = myclient[dbanme]
        collection = db[colname]
        # 通过县级行政区名字查找数据库数据，注意这里的查询语句格式
        result = collection.find_one({
            "properties.NAME_1": name.split('-')[0],  # 处理输入数据格式
            "properties.NAME_2": name.split('-')[1],
            "properties.NAME_3": name.split('-')[2]
        }, {
            "properties": 1,
            "geometry": 1,
            "_id": 0
        })
        # 将查询到的行政区域的边界数据转换为geohash编码
        if result:
            # 将边界数据转换为geohash编码
            geohash_list = []
            # 分层遍历边界数据，注意数据组织结构
            for i in result['geometry']['coordinates'][0]:
                for j in i:
                    # print(j[1], j[0]) # 测试打印经度和纬度
                    geohash_list.append(geohash_encode(j[1], j[0], 8))

            # 连续存放geohash编码
            geohash_str = ''
            # 将geohash编码列表中的数据连续存放
            for i in geohash_list:
                geohash_str += i

            # 打印出geohash编码
            print(str(name)+"对应的geohash编码为: "+geohash_str)
            return geohash_list
        else:
            return None

    else:
        print('数据库出错！')


# 测试geohash编码
print(geohash_encode(116.39, 39.9, 8))

# 这里用“湖北省鄂州市鄂城市”的数据进行测试，这里即是Hubei-Ezhou-Echeng Shì
get_geohash_by_name("Hubei-Ezhou-Echeng Shì")
