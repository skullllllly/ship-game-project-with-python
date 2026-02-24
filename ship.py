import pygame

class ship():
    def __init__(self,screen):
        self.screen=screen

        #load the ship image
        self.image=pygame.image.load("pic game\Jellyfish.bmp")
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()

        #start each new ship at the bottom center of the screen
        #rect=rectangular مثلث
        self.rect.centerx=self.screen_rect.centerx
        self.rect.centery=self.screen_rect.centery
        # moving flag x
        self.moving_right=False
        self.moving_left=False

        #moving flag y
        self.moving_up=False
        self.moving_down=False

#------------------------------------------------------------------



    def update(self):
        #update the ship postion x
        if self.moving_right and self.rect.right <self.screen_rect.right:
            self.rect.centerx+=1

        if self.moving_left and self.rect.left > 0 :
            self.rect.centerx-=1
        # update the ship postion y
        if self.moving_up  and self.rect.top > 0:
            self.rect.centery-=1

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.centery+=1

    def center_ship(self):
        self.center=self.screen_rect.centerx
#-------------------------------------------------------------------

    def blitme(self):
        #draw the ship at its current location
         self.screen.blit(self.image,self.rect)

