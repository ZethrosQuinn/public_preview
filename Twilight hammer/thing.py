import pygame
import random

class Thing(pygame.sprite.Sprite):
    def __init__(self, position, type, direction=None):

        self.type = type
        self.rectWidth = 10
        self.rectHeight = 1
        self.direction = direction
        self.touching = False
        self.speed = 10
        self.damage = 10
    
        #load the mob sprite sheet based on type
        if type == "arrow":
            self.main_sheet = pygame.image.load("arrow.png")

        #define the area of a single sprite on the image
        if self.direction == "left":
            self.main_sheet.set_clip(pygame.Rect(0, 0, self.rectWidth, self.rectHeight))
        else:
            self.main_sheet.set_clip(pygame.Rect(0, 1, self.rectWidth, self.rectHeight))

        #set the initial frame to the clip from the main sheet
        self.display_frame = self.main_sheet.subsurface(self.main_sheet.get_clip())
        self.rect = self.main_sheet.get_rect()

        #set the initial position of the character on the screen
        self.rect.topleft = position
    
    def scroller(self,distance):
        self.rect.x += distance

    def handle_event(self, player, event, things):

        if abs(self.rect.x - player.rect.x - player.rectWidth/2) < 30:
            self.touching = True
            player.damage_Self(self.damage)
            things.remove(self)
        else:
            if self.direction == "left":
                self.scroller(-self.speed)
            elif self.direction == "right":
                self.scroller(self.speed)

        
        
        
