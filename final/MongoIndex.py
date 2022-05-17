import json
import pymongo

# 此函数用于在MongoDB中导入符合的数据并创建空间索引

# 连接并访问MongoDB
myclient = pymongo.MongoClient('mongodb://localhost:27017/')

dblist = myclient.list_database_names()

dbanme = "test"
colname = "gadm404"

if dbanme in dblist:
    print("数据库存在！")
    db = myclient[dbanme]

    # 先在仅剩一条数据的数据库集合中先建立空间索引
    db.get_collection(colname).create_index([("geometry", pymongo.GEOSPHERE)])
    print("空间索引已建立！")

    # 再导入数据，将Json文件存储到MongoDB
    with open("gadm404/gadm404.geojson", "r", encoding="utf-8") as f:
        for line in f:
            try:
                line = line.strip().strip(",")
                data = json.loads(line)
                db[colname].insert_one(data)
            except Exception as e:
                print(e)  # 如果不能插入该条数据就输出错误信息
    print("数据库已存储！")

else:
    print('数据库出错！')
