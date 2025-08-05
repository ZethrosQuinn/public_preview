# -*- coding: utf-8 -*-

import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, position, things):
    
        #load the main character sprite sheet
        self.main_sheet = pygame.image.load("main_char.png")
        self.attack_sheet = pygame.image.load("main_char_attack.png")
        self.jump_sheet = pygame.image.load("main_char_jump.png")

        #set the size of the individual frames, and the frame count to 0
        self.rectWidth = 100
        self.rectHeight = 100
        self.frame = 0
        self.buffer = 10
        self.jump_buffer = 10
        self.direction = "right"
        self.swing = 0
        self.jump = 0
        #optimal 10, if not then then it will gradually climb the screen
        self.jumpmax = 10
        self.swinging = False
        self.idle_frames = 0
        self.idle_max_frames = 5
        self.health = 1000
        self.max_health = 1000

        #define the area of a single sprite on the image
        self.main_sheet.set_clip(pygame.Rect(0, self.buffer, self.rectWidth, self.rectHeight))
        self.attack_sheet.set_clip(pygame.Rect(0, self.buffer, self.rectWidth, self.rectHeight))
        self.jump_sheet.set_clip(pygame.Rect(0, self.buffer, self.rectWidth, self.rectHeight))

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
            'right':  [(self.buffer, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight),
                    (self.rectWidth + self.buffer, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight),
                    (self.rectWidth * 2 + self.buffer, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight)]
        }

        # Define animation frames for each direction
        self.jump_state = {
            'swing': [(0, self.jump_buffer, self.rectWidth, self.rectHeight),
                    (self.rectWidth + self.buffer, self.buffer, self.rectWidth, self.rectHeight),
                    (self.rectWidth * 2 + self.jump_buffer * 2, self.buffer, self.rectWidth + self.buffer, self.rectHeight),
                    (self.rectWidth * 3 + self.jump_buffer * 3, self.buffer, self.rectWidth + self.buffer, self.rectHeight)],
            'not':  [(self.buffer, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight),
                    (self.rectWidth + self.buffer, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight),
                    (self.rectWidth * 2, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight),
                    (self.rectWidth * 3, self.rectHeight + self.buffer * 2, self.rectWidth, self.rectHeight)]
        }

    ##Functional Methods##

    def iterate_frame(self):
        if self.frame == 1:
            self.frame = 2
        else:
            self.frame = 1
    
    def show(self, direction):
        self.display_frame = self.main_sheet.subsurface(pygame.Rect(self.state[direction][self.frame]))

    def update(self, direction):
        
        if direction == 'stand_left':
            self.frame = 0
            self.show('left')

        elif direction == 'stand_right':
            self.frame = 0
            self.show('right')
            
        elif direction in self.state:
            self.iterate_frame()
            self.show(direction)

        self.image = self.main_sheet.subsurface(self.main_sheet.get_clip())

    def attack(self):
        #not jumping, go through normal swing sequence
        if self.jump == 0:
            self.display_frame = self.attack_sheet.subsurface(pygame.Rect(self.state[self.direction][self.swing]))
            self.swing = (self.swing + 1) % 3
        #else we need to go through jump swinging options. Probably hardcoded for now
        else:
            if self.direction == "right":
                if self.jump < self.jumpmax/2:
                    self.display_frame = self.jump_sheet.subsurface(pygame.Rect(self.jump_state['swing'][3]))
                else:
                    self.display_frame = self.jump_sheet.subsurface(pygame.Rect(self.jump_state['swing'][2]))
            else:
                if self.jump < self.jumpmax/2:
                    self.display_frame = self.jump_sheet.subsurface(pygame.Rect(self.jump_state['swing'][1]))
                else:
                    self.display_frame = self.jump_sheet.subsurface(pygame.Rect(self.jump_state['swing'][0]))
        
        self.swinging = True

    #controls merely moving the character up and down on the screen, not display picture
    def jumper(self):
        if self.jump > self.jumpmax/2:
            self.rect.y -= 15
            self.jump -= 1
            if(self.swinging == False):
                if self.direction == "right":
                    self.display_frame = self.jump_sheet.subsurface(pygame.Rect(self.jump_state['not'][2]))
                else:
                    self.display_frame = self.jump_sheet.subsurface(pygame.Rect(self.jump_state['not'][0]))
        else:
            self.rect.y += 15
            self.jump -= 1
            if(self.swinging == False):
                if self.direction == "right":
                    self.display_frame = self.jump_sheet.subsurface(pygame.Rect(self.jump_state['not'][3]))
                else:
                    self.display_frame = self.jump_sheet.subsurface(pygame.Rect(self.jump_state['not'][1]))

    def handle_event(self, event):

        self.swinging = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.update('left')
                self.direction = "left"
                self.idle_frames = 0

            elif event.key == pygame.K_RIGHT:
                self.update('right')
                self.direction = "right"
                self.idle_frames = 0

        if self.jump != 0:
            self.jumper()

        #sprite display options
        if event.type == pygame.TEXTINPUT:
            if event.text == 'z':
                self.attack()
                self.idle_frames = 0

            elif event.text == 'c':
                if self.jump == 0:
                    self.jump = self.jumpmax
                    self.idle_frames = 0

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.update('stand_left')
                self.direction = "left"
                self.idle_frames = 0
        
            elif event.key == pygame.K_RIGHT:
                self.update('stand_right')
                self.direction = "right"
                self.idle_frames = 0

        #Increase idle frames if no movement or attack
        if event.type != pygame.KEYDOWN and event.type != pygame.TEXTINPUT:
            self.idle_frames += 1

        #If idle for 5 frames, revert to standing in the last direction
        if self.idle_frames >= self.idle_max_frames:
            if self.direction == "left":
                self.update('stand_left')
            else:
                self.update('stand_right')

    ##getsetfunctions##
    def getHealth(self):
        return self.health
    
    def healSelf(self):
        self.health = self.max_health

    def damage_Self(self,damage):
        self.health -= damage
