import pygame
import random

class Bubbles(pygame.sprite.Sprite):
    def __init__(self,screen):
        self.screen=screen

        self.image=pygame.image.load("pic game\Bubbles.bmp")
        self.rect=self.image.get_rect()

        screen_rect=screen.get_rect()

        self.rect.x=random.randint(0,screen_rect.width-self.rect.width)
        self.rect.y=random.randint(0,screen_rect.height-self.rect.height)

    def draw_bubble(self):
        self.screen.blit(self.image,self.rect)

