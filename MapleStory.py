import pygame
import random
import os


pygame.init()

 
def refresh():
    gameDisplay.fill(skyblue) #畫面刷新
    # gameDisplay.blit(build1, (0, 250))
    gameDisplay.blit(land, (0, 520))
    gameDisplay.blit(tree, (100, 252))
    gameDisplay.blit(tree, (550, 252))

font_name = os.path.join("./ttf/font.ttf")
def draw_text(surf, text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

class attack(pygame.sprite.Sprite):
    def __init__(self, dir, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = attack_anim[dir][0]
        self.raduis = 25
        self.dir = dir
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 90
        self.hitbox_l = pygame.Rect(self.rect.x - 15, self.rect.y, 20, 70)
        self.hitbox_r = pygame.Rect(self.rect.x + 45, self.rect.y, 20, 70)
        
        
    def update(self):
        # pygame.draw.rect(gameDisplay, red, self.hitbox_l)  hitbox 檢查
        # pygame.draw.rect(gameDisplay, red, self.hitbox_r)  hitbox 檢查
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 4:
                self.kill()
                all_sprites.add(player)
               
            else:
                if self.frame == 3:
                    global score
                    # 偵測碰撞
                    if self.dir == 'left':  # 人物向左 只會攻擊左邊的香菇
                        for gu in gugus:
                            if self.hitbox_l.colliderect((gu.rect.x, gu.rect.y, 75, 75)):
                                gu.kill()
                                
                                score += 10
                                g = gugu(gugu_L)
                                all_sprites.add(g)
                                gugus.add(g)
                                
                    else:
                        for gu in gugus:    # 人物向右 只會攻擊右邊的香菇
                            if self.hitbox_r.colliderect((gu.rect.x, gu.rect.y, 75, 75)):
                                gu.kill()
                                g = gugu(gugu_L)
                                all_sprites.add(g)
                                gugus.add(g)
                                
                                score += 10
                                
                self.image = attack_anim[self.dir][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
                
                                      
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/beginner_L.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (500, 520)  #782
        self.vel_y = 0
        self.jump = False
        self.direction = 'left'
        self.radius = 50
        
    def update(self):
        X_MOVE = 0
        Y_MOVE = 0
        
        key = pygame.key.get_pressed()
        # 跳躍
        if key[pygame.K_x] and self.jump is False:
            self.vel_y = -18
            self.jump = True
        # 防止跳多次(高度確認)
        if self.rect.bottom == 520: 
            self.jump = False
        # 左右移動
        if key[pygame.K_LEFT]:
            self.direction = 'left'
            X_MOVE -= 5
        if key[pygame.K_RIGHT]:
            self.direction = 'right'
            X_MOVE += 5        
        # 人物攻擊
        if key[pygame.K_z] and self.jump is False:
            att = attack(self.direction, self.rect.center)
            all_sprites.remove(player)
            all_sprites.add(att)
        # 賦予重力
        self.vel_y += 1.2
        if self.vel_y > 10:
            self.vel_y = 10
        Y_MOVE += self.vel_y
        
        self.rect.x += X_MOVE
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.y += Y_MOVE
         
        
        # 確保在地板上
        if self.rect.bottom > 520:
            self.rect.bottom = 520
        # 人物跳躍面對的方向
        if self.jump:
            if self.direction == 'left':
                self.image = pygame.image.load('./img/beginner_jump_L.png')
            else:
                self.image = pygame.image.load('./img/beginner_jump_R.png')
        else:
            if self.direction == 'left':
                self.image = pygame.image.load('./img/beginner_L.png')
            else:
                self.image = pygame.image.load('./img/beginner_R.png')
        
                     
class gugu(pygame.sprite.Sprite):
    def __init__(self, img:pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.raduis = 25
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([0, 800])   # 隨機從左右出現
        self.rect.y = 452
        self.direction = 'left'
        self.speed = random.choice([3, 2, 1])   # 隨機速度
        self.speedx = 0
        
    def update(self):
        # pygame.draw.rect(gameDisplay, red, (self.rect.x, self.rect.y, 75, 75)) #檢查 hitbox 
        # 如果從右邊出現
        if self.rect.centerx - player.rect.centerx > 0:
            self.direction = 'left'
            self.image = gugu_L
            # 碰到人物則暫停
            if self.rect.left < player.rect.right:
                self.speedx = 0
            else:
                self.speedx = -self.speed
        # 如果從左邊出現
        else:
            self.direction = 'right'
            self.image = gugu_R
            # 碰到人物則暫停
            if self.rect.right > player.rect.left:
                self.speedx = 0
            else:
                self.speedx = self.speed
        
        self.rect.x += self.speedx
        

class winning(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 200
        self.start_frame = pygame.time.get_ticks()
        self.youwin = "YOU WIN!"
        self.keep = "' Esc '結束遊戲, 任意鍵重新開始遊戲"
    def update(self):
        
# 遊戲結束畫面 #閃爍
        now = pygame.time.get_ticks()
        if now - self.start_frame >= 500:
            gameDisplay.fill(black)
            if now - self.start_frame >= 1000:
                self.start_frame = pygame.time.get_ticks()
        else:
            draw_text(gameDisplay, self.keep, 20, white, WIDTH / 2, 400)
            draw_text(gameDisplay, self.youwin, 100, white, WIDTH / 2, 210)
            
# 遊戲結束畫面 #橫移
        # gameDisplay.fill(black)
        # draw_text(gameDisplay, self.text, 100, self.x, 210)
        # if self.x > 1100:
        #     self.x = 0
        # else:
        #     self.x += 8
    
# 遊戲初始介面
def draw_init():
    # 初始介面
    gameDisplay.fill(skyblue)
    draw_text(gameDisplay, "一起來打怪", 100, black, WIDTH / 2, 100)
    draw_text(gameDisplay, "遊戲開始", 50, black, WIDTH / 2, 300)
    draw_text(gameDisplay, "← →進行移動, 'X'跳躍, 'Z'攻擊", 20, black, WIDTH / 2, 450)
    gameDisplay.blit(beginner, (20, 330))
    gameDisplay.blit(big_gugu, (630, 320))
    pygame.display.update()
    # 等待按下開始
    waitting = True
    while waitting:
        x, y = pygame.mouse.get_pos()
        # 偵測滑鼠位置 顯示框線
        if(x >= 310 and x <= 500 and y >= 310 and y <= 360):
            pygame.draw.rect(gameDisplay, black, (290, 308, 220, 55), 4)
        else:
            pygame.draw.rect(gameDisplay, skyblue, (290, 308, 220, 55), 4)
        pygame.display.update()
        
        # 是否按下開始
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if(x >= 310 and x <= 500 and y >= 310 and y <= 360):
                    waitting = False
                
#初始設定
FPS = 60
fpsclock = pygame.time.Clock()


#介面設定
WIDTH= 800
HIGH = 600
gameDisplay = pygame.display.set_mode((WIDTH, HIGH))
pygame.display.set_caption("Maple Story")

# 載入圖片
tree_img = pygame.image.load('./img/tree.png').convert_alpha()
build1_img = pygame.image.load('./img/build1.png').convert_alpha()
land_img = pygame.image.load('./img/land.png').convert_alpha()
gugu_L_img = pygame.image.load('./img/gugu_L.png').convert_alpha()
gugu_R_img = pygame.image.load('./img/gugu_R.png').convert_alpha()
beginner_img = pygame.image.load('./img/beginner_jump_R.png').convert_alpha()

attack_anim = {}
attack_anim['left']= []
attack_anim['right']= []
for i in range(4):
    att_L_img = pygame.image.load(os.path.join("img", f"beginner_a{i}_L.png")).convert_alpha()
    att_R_img = pygame.image.load(os.path.join("img", f"beginner_a{i}_R.png")).convert_alpha()
    attack_anim['right'].append(att_R_img)
    attack_anim['left'].append(att_L_img)

# 修改圖片大小
tree = pygame.transform.rotozoom(tree_img, 0, 2)
build1 = pygame.transform.rotozoom(build1_img, 0, 2)
land = pygame.transform.scale(land_img, (WIDTH, 50))
gugu_L = pygame.transform.scale(gugu_L_img, (75, 75))
gugu_R = pygame.transform.scale(gugu_R_img, (75, 75))
beginner = pygame.transform.scale(beginner_img, (180, 400))
big_gugu = pygame.transform.scale(gugu_L, (150, 200))

# 顏色
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
skyblue = (45, 171, 255)

# 創建角色
all_sprites = pygame.sprite.Group()
gugus = pygame.sprite.Group()
win = winning()
player = Player()
for i in range(2):
    g = gugu(gugu_L)
    gugus.add(g)
    all_sprites.add(g)
all_sprites.add(player)

score = 0
gameover = False
# cloud = cloud(200, 200)



#主程式
playing = True
show_init = True

while playing:
    
    # 顯示初始介面
    if show_init:
        draw_init()
        show_init = False
    refresh()
    if score >= 50:     # 滿分->結束
        gameover = True
    # 進到結束畫面
    if gameover:
        gameDisplay.fill(black)
        win.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    pygame.quit()
                    print(1)
                    exit()
                    playing = False
                else:
                    gameover = False
                    score = 0
                    show_init = True
    # 沒結束就繼續
    else:
        all_sprites.update()
        all_sprites.draw(gameDisplay)
        draw_text(gameDisplay, str(score), 20, black, WIDTH / 2, 10)
     
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
    # 遊戲開始
       
    
    fpsclock.tick(FPS)
    
pygame.quit()
quit()