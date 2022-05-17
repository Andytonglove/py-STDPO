import pymongo

# 本程序用以在MongoDB中检索西经60度的经线穿过的所有国家

# 连接并访问MongoDB
myclient = pymongo.MongoClient('mongodb://localhost:27017/')

dblist = myclient.list_database_names()

dbanme = "test"
colname = "gadm404"

if dbanme in dblist:
    print("数据库存在！")
    db = myclient[dbanme]

    # 检索西经60度的经线穿过的所有国家
    result = db.get_collection(colname).find({
        "geometry": {"$geoIntersects":
                     {"$geometry": {"type": "LineString", "coordinates": [[-60, 90], [-60, -90]]}
                      }
                     }
    }, {"properties": 1, "geometry": 1, "_id": 0})

    # 打印查询结果的县级所属国家名字
    lis = list(result)
    country = []
    for i in range(0, len(lis)):
        # print(lis[i]['properties']['NAME_0'])
        country.append(lis[i]['properties']['NAME_0'])
    print(list(set(country)))  # 这里由于重复原因需要对结果数组进行综合过滤去重

    # 统计查询时间，explain()方法返回查询结果的详细信息
    time = result.explain()['executionStats']['executionTimeMillis']
    print("检索花费时间：" + str(time) + "ms")

else:
    print('数据库出错！')
