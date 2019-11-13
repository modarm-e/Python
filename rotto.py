import random as rd


list=[]
ran_num=rd.randint(1,45)

for i in range(6):
    while ran_num in list:
        ran_num = rd.randint(1,45)
    list.append(ran_num)
list.sort()
print(list)
print("내가 맞추는 수")
rs=[]
i=0
for i in range(6):
    put=int(input("정수 입력하세요"))
    while put in rs:
        put=int(input("동일 숫자 발견 다시입력하세요!"))
    rs.append(put)
    rs.sort()
    i+=1
    if i==6:
        break
print(list)
print(rs)
if list == rs:
    print('동일합니다')
else:
    print('틀립니다')
