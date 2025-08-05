import pygame
import random
from thing import Thing

class Mob(pygame.sprite.Sprite):
    def __init__(self, position, type, things):
    
        #load the mob sprite sheet based on type
        if type == "grunt":
            self.main_sheet = pygame.image.load("grunt.png")
        if type == "archer":
            self.main_sheet = pygame.image.load("archer.png")

        #set the size of the individual frames, and the frame count to 0
        self.things = things
        self.type = type
        self.rectWidth = 100
        self.rectHeight = 100
        self.frame = 0
        self.buffer = 10
        self.direction = "left"
        self.swing = False
        self.type = type
        self.speed = 10
        self.swing_delay_curr = 0
        self.touching = False
        self.damage_val = 5

        if self.type == "grunt":
            self.swing_delay_max = 5
            self.health = 5
        elif self.type == "archer":
            self.swing_delay_max = 10
            self.health = 2

        #define the area of a single sprite on the image
        self.main_sheet.set_clip(pygame.Rect(0, self.buffer, self.rectWidth, self.rectHeight))

        #set the initial frame to the clip from the main sheet
        self.display_frame = self.main_sheet.subsurface(self.main_sheet.get_clip())
        self.rect = self.main_sheet.get_rect()

        #set the initial position of the character on the screen
        self.rect.topleft = position

        # Define animation frames for each direction
        if self.type == "grunt":
            self.state = {
                "left": [(0, self.buffer, self.rectWidth, self.rectHeight),
                        (self.rectWidth, self.buffer, self.rectWidth, self.rectHeight),
                        (self.rectWidth * 2, self.buffer, self.rectWidth + self.buffer, self.rectHeight)],
                "right":  [(self.buffer, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight),
                        (self.rectWidth + self.buffer, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight),
                        (self.rectWidth * 2 + self.buffer, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight)]
            }
        elif self.type == "archer":
            self.state = {
                "left": [(0, self.buffer, self.rectWidth, self.rectHeight),
                        (self.rectWidth, self.buffer, self.rectWidth, self.rectHeight),
                        (self.rectWidth * 2, self.buffer, self.rectWidth + self.buffer, self.rectHeight),
                        (self.rectWidth * 3, self.buffer, self.rectWidth + self.buffer, self.rectHeight)],
                "right":  [(self.buffer, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight),
                        (self.rectWidth + self.buffer, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight),
                        (self.rectWidth * 2 + self.buffer, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight),
                        (self.rectWidth * 3 + self.buffer, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight)]
            }

    def iterate_frame(self):
        if self.frame == 1:
            self.frame = 0
        else:
            self.frame = 1

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

    def attack(self,direction,player,things):

        if self.type == "grunt":
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
        elif self.type == "archer":
            if self.swing_delay_curr >= self.swing_delay_max:
                self.swing_delay_curr = 0
                if self.swing == False:
                    self.display_frame = self.main_sheet.subsurface(pygame.Rect(self.state[direction][3]))
                    self.swing = True
                    things.append(Thing((self.rect.x, self.rect.y + self.rectHeight/3), "arrow", direction))
                else:
                    self.swing = False
                    self.update(direction)
            else:
                self.display_frame = self.main_sheet.subsurface(pygame.Rect(self.state[direction][2]))
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
                    self.scroller(random.randint(75, 250))
                else:
                    self.scroller(-random.randint(75, 250))
                self.health -=1
        else:
            #movement behaviors
            if self.type == "grunt":
                #if to the left of player beyond close range, move right
                if self.rect.x < (player.rect.x - self.rectWidth/2):
                    self.scroller(self.speed)
                    self.update("right")
                #if to the right of player beyond close range, move left
                elif self.rect.x > (player.rect.x + self.rectWidth/2):
                    self.scroller(-self.speed)
                    self.update("left")
                #otherwise attack
                else:
                    if self.rect.x < player.rect.x:
                        self.attack("right",player, self.things)
                    else:
                        self.attack("left",player, self.things)
            elif self.type == "archer":
                #if to the left of player
                if self.rect.x < player.rect.x:
                    #if in close range, move left
                    if self.rect.x > (player.rect.x - self.rectWidth):
                        self.scroller(-self.speed)
                        self.update("left")
                    #if too far out of range, move closer
                    elif self.rect.x < (player.rect.x - self.rectWidth - 200):
                        self.scroller(self.speed)
                        self.update("right")
                    #otherwise attack facing right
                    else:
                        self.attack("right",player, self.things)
                #if to the right of player
                elif self.rect.x > player.rect.x:
                    #if in close range, move right
                    if self.rect.x < (player.rect.x + self.rectWidth):
                        self.scroller(self.speed)
                        self.update("right")
                    #if too far out of range, move closer
                    elif self.rect.x > (player.rect.x + self.rectWidth + 200):
                        self.scroller(-self.speed)
                        self.update("left")
                    #otherwise attack facing left
                    else:
                        self.attack("left",player, self.things)
