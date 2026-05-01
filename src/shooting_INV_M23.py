import pyxel
import random

# ゲームの定数
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 160

class Player:
    """プレイヤーのキャラクタークラス"""
    def __init__(self,app, x, y):
        self.app = app
        self.app.player = self
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
        self.speed = 2
    
    def update(self):
        """プレイヤーの更新（移動と弾の発射）"""
        if pyxel.btn(pyxel.KEY_LEFT) :
            self.x = max(0, self.x - self.speed)
        if pyxel.btn(pyxel.KEY_RIGHT) :
            self.x = min(SCREEN_WIDTH - self.width, self.x + self.speed)
        if pyxel.btn(pyxel.KEY_UP) :
            self.y = max(0, self.y - self.speed)
        else :
            if SCREEN_HEIGHT - self.height*5 > self.y :
                self.y = self.y + 1
        if pyxel.btn(pyxel.KEY_DOWN) :
            self.y = min(SCREEN_HEIGHT - self.height, self.y + self.speed)
        else :
            if SCREEN_HEIGHT - self.height*5 < self.y :
                self.y = self.y + - 1

        # 弾の発射
        if pyxel.btnp(pyxel.KEY_SPACE) :
            Bullet(self.app, self.x + self.width / 2 - 1, self.y)
    
    def draw(self):
        """プレイヤーの描画"""
        # pyxel.rect(self.x, self.y, self.width, self.height, pyxel.COLOR_LIGHT_BLUE)
        pyxel.blt(self.x, self.y,0,0,0,8,8,0)

class Enemy:
    """敵キャラクタークラス"""
    def __init__(self, app,x, y, vec):
        self.app = app
        self.app.enemy = self
        self.x = x
        self.y = y
        self.vec = vec
        self.width = 8
        self.height = 8
        self.speed = 1
        self.app.enemies.append(self)

    def update(self):
        """敵の更新（下方向、横方向への移動）"""
        if self.vec == 0 :
            self.y += self.speed
        else :
            self.x -= self.speed
        # 画面外に出た敵を削除
        if self.y > SCREEN_HEIGHT:
            if self.app.enemies :
                self.app.enemies.remove(self)
    
    def draw(self):
        """敵の描画"""
        # pyxel.rect(self.x, self.y, self.width, self.height, pyxel.COLOR_RED)
        pyxel.blt(self.x, self.y,0,8,0,8,8,0)

class Bullet:
    """弾クラス"""
    def __init__(self, app, x, y):
        self.app = app
        self.app.bullet = self
        self.x = x
        self.y = y
        self.width = 2
        self.height = 8
        self.speed = 3
        self.app.bullets.append(self)

    def update(self):
        """弾の更新（上方向への移動）"""
        self.y -= self.speed
        # 画面外に出た弾を削除
        if self.y < 0:
            if self.app.bullets :
                self.app.bullets.remove(self)
    
    def draw(self):
        """弾の描画"""
        pyxel.blt(self.x, self.y,0,0,8,2,8,0)

class App:
    """ゲーム全体のロジックを管理するクラス"""
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Shooting Game")
        pyxel.load("shooting_resource.pyxres")
        self.bullets = []
        Player(self,SCREEN_WIDTH / 2 - 4, SCREEN_HEIGHT - 16 )
        self.enemies = []
        self.score = 0
        self.spawn_timer = 0
        self.is_game_over = False

        # サウンドの初期設定
        # 0番のサウンドバンクに音データを設定 (音符, 音量, 音色, エフェクト, スピード)
        # C3: ド, D3: レ, E3: ミ, F3: ファ, G3: ソ, A3: ラ, B3: シ
        pyxel.sound(0).set("c3e3g3c4", "2", "6", "vffn", 5) # 敵を倒した時の音
        onpu = "" 
        c = 0
        while c < 30 :
            onpu += "f2g2"
            c += 1
        pyxel.sound(1).set(onpu, "2", "4", "v", 10) # ゲームオーバー時の音

        pyxel.run(self.update, self.draw)

    def update(self):
        """ゲームロジックの更新"""
        # if self.is_game_over:
        #     if pyxel.btnp(pyxel.KEY_R):
        #         self.reset_game()
        #     return
        if self.is_game_over:
            return
            
        # プレイヤーの更新
        self.player.update()
        
        # 敵の生成
        self.spawn_timer += 1
        if self.spawn_timer >= 10: # 30フレームごとに敵を生成
            vec = random.choice([0,0,1])
            print(vec)
            if vec == 0 :
                Enemy(self, random.randint(0, SCREEN_WIDTH - 8), 0,vec)
            else :
                Enemy(self, SCREEN_WIDTH - 8, random.randint(SCREEN_HEIGHT/2,
                                                              SCREEN_HEIGHT-40),vec)
            self.spawn_timer = 0
        
        # 弾の更新
        for bullet in self.bullets.copy():
            bullet.update()
        # 敵の更新
        for enemy in self.enemies.copy():
            enemy.update()

        # 弾と敵の衝突判定と削除
        for bullet in self.bullets.copy():
            for enemy in self.enemies.copy():
                if (bullet.x < enemy.x + enemy.width and
                    bullet.x + bullet.width > enemy.x and
                    bullet.y < enemy.y + enemy.height and
                    bullet.y + bullet.height > enemy.y):
                    
                    if self.bullets :
                        self.bullets.remove(bullet)
                    if self.enemies :
                        self.enemies.remove(enemy)
                    # self.score += 100
                    pyxel.play(0, 0) # 効果音 (サウンドバンク0の0番の音)



        # 敵とプレイヤーの衝突判定
        for enemy in self.enemies:
            if (self.player.x < enemy.x + enemy.width and
                self.player.x + self.player.width > enemy.x and
                self.player.y < enemy.y + enemy.height and
                self.player.y + self.player.height > enemy.y):
                
                self.is_game_over = True
                pyxel.play(0, 1) # 効果音 (サウンドバンク0の1番の音)

    def draw(self):
        """画面の描画"""
        pyxel.cls(0) # 画面をクリア (黒)
        
        # if not self.is_game_over:
        self.player.draw()
        for bullet in self.bullets.copy():
            bullet.draw()
        for enemy in self.enemies.copy():
            enemy.draw()
            
        #     pyxel.text(5, 5, f"SCORE: {self.score}", pyxel.COLOR_WHITE)
        # else:
        #     pyxel.text(SCREEN_WIDTH/2 - 20, SCREEN_HEIGHT/2 - 4, "GAME OVER", pyxel.COLOR_RED)
        #     pyxel.text(SCREEN_WIDTH/2 - 24, SCREEN_HEIGHT/2 + 4, f"SCORE: {self.score}", pyxel.COLOR_WHITE)
        #     pyxel.text(SCREEN_WIDTH/2 - 40, SCREEN_HEIGHT/2 + 12, "PRESS R TO RESTART", pyxel.COLOR_LIGHT_BLUE)

    # def reset_game(self):
    #     self.player.x = SCREEN_WIDTH / 2 - 4
    #     self.player.y = SCREEN_HEIGHT - 16
    #     self.bullets = []
    #     self.enemies = []
    #     self.score = 0
    #     self.spawn_timer = 0
    #     self.is_game_over = False
    #     self.player.bullets = self.bullets

App()

