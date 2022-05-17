import json
import pymongo

# 本程序用以将除开大小超限的其他全部数据导入MongoDB

# 连接并访问MongoDB
myclient = pymongo.MongoClient('mongodb://localhost:27017/')

dblist = myclient.list_database_names()

dbanme = "test"
colname = "gadm404"

if dbanme in dblist:
    print("数据库已存在！")
    db = myclient[dbanme]
    collection = db[colname]
    # 将Json文件存储到MongoDB
    with open("gadm404/gadm404.geojson", "r", encoding="utf-8") as f:
        for line in f:
            try:
                line = line.strip().strip(",")
                # print(line) # 测试打印每一行
                data = json.loads(line)  # 将Json字符串转换为字典
                collection.insert_one(data)
            except Exception as e:
                print(e)
    print("数据库已存储！")


else:
    print('数据库出错！')
