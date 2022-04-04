#先输出helloworld
print("hello world")

#循环输出hellopy：99次
""" for i in range(1,100):
    print("hello,python ",i) """

#判断语句
""" if 2>1:
    print("2>1")
elif 2==1:
    print("2=1")
else:
    print("2<1") """

#阶乘跑个
factorial=1
print("please input your num:\n")
num=int(input())
if num<1:
    print("error")
elif num==1:
    print(1)
elif num>1:
    for i in range(1,num+1):
        num=num*i
    print(num)