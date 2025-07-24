import os
import random
import math 
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platform game")
WIDTH, HEIGHT = 800, 600
FPS = 60 
PLAYER_VELOCITY = 5

window = pygame.display.set_mode( (WIDTH, HEIGHT) )

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}
    for image in images: 
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []

        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface( (width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = flip(sprites)
    
    return all_sprites


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    ANIMATION_DELAY = 3
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)

    def __init__(self, x, y, width, height):
        self.rect =pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0 

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, velocity):
        self.x_vel = -velocity
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
  
    def move_right(self, velocity):
        self.x_vel = velocity
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    # scraped

    # def move_top(self, velocity):
    #     self.y_vel = -velocity
    #     if self.direction != "top":
    #         self.direction = "top"
    #         self.animation_count = 0
    
    # def move_bottom(self, velocity):
    #     self.y_vel = velocity
    #     if self.direction != "bottom":
    #         self.direction = "bottom"
    #         self.animation_count = 0

    def loop(self, fps):
        # self.y_vel +=  4*(self.GRAVITY * (self.fall_count/FPS))
        self.move(self.x_vel, self.y_vel)
        self.update_sprite()
        self.fall_count += 1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.x_vel != 0:
            sprite_sheet = "run"
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update():
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        # self.sprite = self.SPRITES["idle_" + self.direction][0]
        win.blit(self.sprite, (self.rect.x, self.rect.y))

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))

    _, _, width, height = image.get_rect()

    tiles = []

    for i in range(WIDTH// width + 1):
        for j in range(HEIGHT// height + 1):
            pos = (i * width, j*height)
            tiles.append(pos)
    
    return tiles, image

def draw(window, background, bg_image, player):
    for tile in background:
        window.blit(bg_image, tile)
    player.draw(window)
    pygame.display.update()

def handle_move(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    player.y_vel = 0
    if keys[pygame.K_a]:
        player.move_left(PLAYER_VELOCITY)
    if keys[pygame.K_d]:
        player.move_right(PLAYER_VELOCITY)
    # if keys[pygame.K_w]:
    #     player.move_top(PLAYER_VELOCITY)
    # if keys[pygame.K_s]:
    #     player.move_bottom(PLAYER_VELOCITY)
    

def main(window):
    clock = pygame.time.Clock()
    bg, bg_image = get_background("Pink.png")
    
    player =  Player(100, 100, 50, 50)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
                break

        player.loop(FPS) 
        handle_move(player)
        draw(window, bg, bg_image, player)  

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)