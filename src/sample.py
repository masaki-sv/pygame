import random
te = ("","グー","チョキ","パー")

#勝ち負け判定
def hantei(a,b) : 
    if a == b :
        return 2
    elif a==1 and b==2 :
        return 1
    elif a==1 and b==3 :
        return 0
    elif a==2 and b==1 :
        return 0
    elif a==2 and b==3 :
        return 1
    elif a==3 and b==1 :
        return 1
    elif a==3 and b==2 :
        return 0

#メイン
while True:
    #人間の手
    print("1:グー、2:チョキ、3:パー")
    a = int(input())
    #コンピュータの手
    b = random.randint(1,3)
    print("コンピュータ："+te[b])
    #判定
    c = hantei(a,b)
    if c == 2 :
        print("あいこ")
        continue
    elif c == 0 :
        print("コンピュータの勝ち")
    elif c == 1 :
        print("あなたの勝ち")
    break
        

