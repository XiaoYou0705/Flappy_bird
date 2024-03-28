import pygame
import os
import random

# 鳥 Sprite
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = bird
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HIGH / 2 - 80
        self.speedy = 6.5
        self.total_degree = 0
        self.angle = 0
        
    def rotate(self, rotate_degree):
        self.total_degree += rotate_degree
        if self.total_degree >= 75:
            self.total_degree = 75
        if self.total_degree <= -74:
            self.total_degree = -74
            
        if rotate_degree == -10:
            self.total_degree = -74
            self.image = bird_fly
            
        if rotate_degree == 3 and self.total_degree >= -45:
            self.image = pygame.transform.rotate(self.image_ori, -self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
            
        
    def update(self):
        self.rotate(3)
        # 防止角色超出地圖
        if self.rect.bottom >= 700:
            self.rect.bottom = 700
        if self.rect.y <= 0:
            self.rect.y = 0
        # 跳躍
        key = pygame.key.get_pressed()
        
        if key[pygame.K_SPACE]:
            self.speedy = -8
            self.rotate(-10)
        self.speedy += 1.2
        if self.speedy >= 6.5:
            self.speedy = 6.5
            
        self.rect.y += self.speedy

# 下_水管
class Pipe_down(pygame.sprite.Sprite):
    def __init__(self, exit_high):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe_down
        self.rect = self.image.get_rect()
        self.rect.left = 630
        self.rect.top = exit_high + 100
        self.speedx = 5
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right == 0:
            self.kill()
# 上_水管       
class Pipe_top(pygame.sprite.Sprite):
    def __init__(self, exit_high):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe_top
        self.rect = self.image.get_rect()
        self.rect.left = 630
        self.rect.bottom = exit_high - 100
        self.speedx = 5
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right == 0:
            self.kill()
        
# 介面設定
WIDTH = 630
HIGH = 700

gameDisplay = pygame.display.set_mode((WIDTH, HIGH))
pygame.display.set_caption("Flappy bird")

# 幀數設定
FPS = 60
fpsclock = pygame.time.Clock()

# 載入圖片
bird_img = pygame.image.load(os.path.join("./img/bird.png")).convert_alpha()
pipe_down_img = pygame.image.load(os.path.join("./img/pipe.png")).convert_alpha()
pipe_img = pygame.transform.rotate(pipe_down_img, 180)


# 調整圖片
bird = pygame.transform.scale(bird_img, (100, 80))
bird_fly = pygame.transform.rotate(bird, 45)

pipe_top = pygame.transform.scale(pipe_img, (150, 500))
pipe_down = pygame.transform.scale(pipe_down_img, (150, 500))

# 顏色
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
skyblue = (45, 171, 255)

# 載入背景


# 水管數值
pipe_x = 775
exit_y = random.randrange(200, 600)

# 加入角色

all_sprite = pygame.sprite.Group()
pipes = pygame.sprite.Group()
top_pipe = Pipe_top(exit_y)
down_pipe = Pipe_down(exit_y)
pipes.add(top_pipe)
pipes.add(down_pipe)
player = Bird()
all_sprite.add(player)
all_sprite.add(top_pipe)
all_sprite.add(down_pipe)


# 主程式
playing = True
while playing:
    
    gameDisplay.fill(skyblue)
    pipe_x -= 5
    if(pipe_x <= 200):
        print(exit_y)
        exit_y = random.randrange(200, 600)
        next_top_pipe = Pipe_top(exit_y)
        next_down_pipe = Pipe_down(exit_y)
        pipes.add(next_down_pipe)
        pipes.add(next_top_pipe)   
        all_sprite.add(next_top_pipe)
        all_sprite.add(next_down_pipe)
        pipe_x = 775

    all_sprite.update()
    all_sprite.draw(gameDisplay)
    hits = pygame.sprite.spritecollide(player, pipes, False)
    for hit in hits:
        playing = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
    pygame.display.update()
    fpsclock.tick(FPS)

pygame.quit()
quit()