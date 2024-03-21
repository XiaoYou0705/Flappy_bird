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
            self.speedy = -12
            self.rotate(-10)
        self.speedy += 1.2
        if self.speedy >= 6.5:
            self.speedy = 6.5
            
        self.rect.y += self.speedy
        
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

# 調整圖片
bird = pygame.transform.scale(bird_img, (100, 80))
bird_fly = pygame.transform.rotate(bird, 45)
# 顏色
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
skyblue = (45, 171, 255)

# 載入背景

# 加入角色
all_sprite = pygame.sprite.Group()
player = Bird()
all_sprite.add(player)

# 主程式
playing = True
while playing:
    gameDisplay.fill(skyblue)
    
    all_sprite.update()
    all_sprite.draw(gameDisplay)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
    pygame.display.update()
    fpsclock.tick(FPS)

pygame.quit()
quit()