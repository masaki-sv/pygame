import pyxel

# ゲーム設定
WIDTH = 128
HEIGHT = 192
# プレイヤー設定
PLAYER_WIDTH  = 16
PLAYER_HEIGHT = 16
PLAYER_SPEED = 4
# ボール設定
BALL_RADIUS = 8
BALL_SPEED_X = 4
BALL_SPEED_Y = 4

class app:

# ゲームの状態
    game_over = False
    player_x = 0
    player_y = HEIGHT - PLAYER_HEIGHT
    ball_x = 0
    ball_y = 0

    def __init__(self):
        self.game_start = False

        pyxel.init(WIDTH, HEIGHT,"スカッシュゲーム")
        pyxel.load("my_resource.pyxres")
        pyxel.run(self.update, self.draw)
 
    def update(self):
        global BALL_SPEED_X
        global BALL_SPEED_Y

        if pyxel.btnp(pyxel.KEY_S):
            self.game_start = True
            self.retry()

            

    # プレイヤーの操作
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += PLAYER_SPEED

    # プレイヤーの位置を制限
        self.player_x = min(max(self.player_x, 0), WIDTH - PLAYER_WIDTH)

    # ボールを動かす
        self.ball_x += BALL_SPEED_X
        self.ball_y += BALL_SPEED_Y

    # 壁との当たり判定
        if self.ball_x <= 0 or self.ball_x >= WIDTH:
            BALL_SPEED_X *= -1
        if self.ball_y <= 0:
            BALL_SPEED_Y *= -1

    # プレイヤーとの当たり判定
        if (
            self.ball_x + BALL_RADIUS >= self.player_x
            and self.ball_x <= self.player_x + PLAYER_WIDTH
            and self.ball_y + BALL_RADIUS >= self.player_y
            and self.ball_y <= self.player_y + PLAYER_HEIGHT
            ):
            BALL_SPEED_Y *= -1

    # ゲームオーバー判定
        if self.ball_y >= HEIGHT:
            self.game_over = True

    def draw(self):
        pyxel.cls(0)
        pyxel.line(0, 0, 0, HEIGHT-1, 7)
        pyxel.line(0, 0, WIDTH-1, 0, 7)
        pyxel.line(WIDTH-1, 0, WIDTH-1, HEIGHT-1, 7)

    # プレイヤーを描画
        pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16, 0)

    # ボールを描画
        pyxel.blt(self.ball_x - BALL_RADIUS, self.ball_y - BALL_RADIUS,
                   0, 16, 0, 16, 16, 0)

    # ゲームオーバー画面
        if self.game_over:
            pyxel.text(WIDTH // 2 - 40, HEIGHT // 2 - 16, "GAME OVER", 7)
        if self.game_start == False:
            pyxel.cls(1)

    def retry(self): #リトライ時のリセット関数
        self.game_over = False
        self.ball_x = 16
        self.ball_y = 8
        BALL_SPEED_X = 4
        BALL_SPEED_Y = 4
app()