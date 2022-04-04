import pymongo

# 连接并访问MongoDB
myclient = pymongo.MongoClient('mongodb://localhost:27017/')

dblist = myclient.list_database_names()

dbanme = "yourdbname"

if dbanme in dblist:
    print("数据库已存在！")
    db = myclient[dbanme]

    # 用直线（84.26，27.34）--（108.95，45.22）进行intersect查询
    result = db.get_collection('china').find({
        "geometry": {"$geoIntersects":
                     {"$geometry": {"type": "LineString", "coordinates": [[84.26, 27.34], [108.95, 45.22]]}
                      }
                     }
    }, {"properties": 1})
    # print(list(result))  # 这是测试打印，输出list都是找到的所有

    # 打印查询结果的属性信息
    lis = list(result)
    for i in range(0, len(lis)):
        print(lis[i]['properties'])

else:
    print('数据库出错！')
