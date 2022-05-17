import psycopg2
import time

# 本程序用以在PostGIS中检索西经60度的经线穿过的所有国家

conn = psycopg2.connect(database='test', user='postgres',
                        password='******', host='localhost')
curs = conn.cursor()

# 通过sql语句查找西经60度的经线穿过端点，这里进行Intersects空间查询
sql = "SELECT name_0 FROM gadm404 WHERE ST_Intersects(ST_GeomFromText('LINESTRING(-60 90, -60 -90)', 0), gadm404.geom)"

# 进行sql语句查询，并统计时间
start = time.time()
curs.execute(sql)
end = time.time()
print("查询花费时间：" + str((end - start)*1000) + "ms")

# 将返回的结果中的国家进行去重并打印
country = []
for row in curs.fetchall():
    # print(row[0])
    country.append(row[0])
print(list(set(country)))
