import turtle
# スクリーンの設定
screen = turtle.Screen()
screen.setup(width=600, height=400)
screen.title("日本の国旗")
# タートルの設定
kame = turtle.Turtle()
# 赤い円を描く
kame.penup()
kame.goto(0, -120) # 円の中心に移動
kame.pendown()
kame.color("red")
kame.begin_fill()
kame.circle(120) # 円の半径
kame.end_fill()
# 終了
kame.hideturtle()
turtle.done()
