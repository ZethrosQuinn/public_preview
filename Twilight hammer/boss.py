import pygame
import random

class Boss(pygame.sprite.Sprite):
    def __init__(self, position, type, things):
    
        #load the mob sprite sheet based on type
        if type == "grunt":
            self.main_sheet = pygame.image.load("boss_grunt.png")

        #set the size of the individual frames, and the frame count to 0
        self.things = things
        self.rectWidth = 200
        self.rectHeight = 200
        self.frame = 0
        self.buffer = 10
        self.direction = "left"
        self.swing = False
        self.type = type
        self.speed = 15
        self.swing_delay_curr = 0
        self.swing_delay_max = 3
        self.touching = False
        self.health = 20
        self.damage_val = 10

        #define the area of a single sprite on the image
        self.main_sheet.set_clip(pygame.Rect(0, 0, self.rectWidth, self.rectHeight))

        #set the initial frame to the clip from the main sheet
        self.display_frame = self.main_sheet.subsurface(self.main_sheet.get_clip())
        self.rect = self.main_sheet.get_rect()

        #set the initial position of the character on the screen
        self.rect.topleft = position

        # Define animation frames for each direction
        self.state = {
            'left': [(0, self.buffer, self.rectWidth, self.rectHeight),
                    (self.rectWidth, self.buffer, self.rectWidth, self.rectHeight),
                    (self.rectWidth * 2, self.buffer, self.rectWidth + self.buffer, self.rectHeight)],
            'right':  [(self.buffer, self.rectHeight + self.buffer * 3, self.rectWidth, self.rectHeight),
                    (self.rectWidth + self.buffer, self.rectHeight + self.buffer * 3, self.rectWidth, self.rectHeight),
                    (self.rectWidth * 2 + self.buffer, self.rectHeight + self.buffer * 3, self.rectWidth, self.rectHeight)]
        }

    def iterate_frame(self):
        if self.frame == 0:
            self.frame = 1
        else:
            self.frame = 0

    def show(self, direction):
        if direction in self.state:
            self.display_frame = self.main_sheet.subsurface(pygame.Rect(self.state[direction][self.frame]))

    def scroller(self,distance):
        self.rect.x += distance

    def update(self, direction):
            
        if direction in self.state:
            self.iterate_frame()
            self.show(direction)

        self.image = self.main_sheet.subsurface(self.main_sheet.get_clip())

    def attack(self,direction,player):
        
        if self.swing_delay_curr >= self.swing_delay_max:
            self.swing_delay_curr = 0
            if self.swing == False:
                self.display_frame = self.main_sheet.subsurface(pygame.Rect(self.state[direction][2]))
                self.swing = True
                player.damage_Self(self.damage_val)
            else:
                self.swing = False
                self.update(direction)
        else:
            self.swing_delay_curr += 1

    def handle_event(self, player, event, mobs):

        if self.health == 0:
            mobs.remove(self)
            return

        self.touching = False
        
        if abs(self.rect.x - player.rect.x) < 125:
            self.touching = True
        else:
            self.touching = False

        if event.type == pygame.TEXTINPUT and event.text == 'z' and self.touching:
            if player.swinging:
                if player.rect.x < self.rect.x:
                    #change to bounce
                    self.scroller(random.randint(50, 150))
                else:
                    self.scroller(-random.randint(50, 150))
                self.health -=1
        else:
            if self.rect.x < (player.rect.x - self.rectWidth/2):
                self.scroller(self.speed)
                self.update("right")
            elif self.rect.x > (player.rect.x + self.rectWidth/2):
                self.scroller(-self.speed)
                self.update("left")
            else:
                if self.rect.x < player.rect.x:
                    self.attack("right",player)
                else:
                    self.attack("left",player)
