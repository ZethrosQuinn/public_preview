import pygame
import player
from mob import Mob
from boss import Boss
from thing import Thing
import random

pygame.init()

#screen settings and main character spawn location
screen_width = 800
screen_height = 455
posx = 345
posy = 345

#mob holders
mobs = []
bosses = []
things = []

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Twilight Hammer")
player_character = player.Character((posx, posy),things)
clock = pygame.time.Clock()

#menu options and vars
menu_options = ["Resume", "Quit"]
gameover_menu_options = ["Restart", "Quit"]
selected_option = 0
win = False
loss = False
player_health = 0
First_grunt = False
First_archer = False

#spawn vars
spawn_interval = 200
  
#font and text box vars
MENU_FONT = pygame.font.Font(None, 36)
Health_FONT = pygame.font.Font(None, 24)
Distance_FONT = pygame.font.Font(None, 24)
Message_Font = pygame.font.Font(None, 16)
win_message = MENU_FONT.render("You Win!", True, (255, 255, 255))
lose_message = MENU_FONT.render("You Lose!", True, (255, 255, 255))
option_message = MENU_FONT.render("Menu", True, (255, 255, 255))

message = ""

#scroll settings
FPS = 15
scroll = 0
scrollspeed = 20
blockeractive = False
scroll_lock = 0
blockerpositions = [2000,4000,6000]

bg_image = pygame.image.load("castle_trimmed_long.png").convert_alpha()
bg_width = bg_image.get_width()

#function to draw background
def draw_bg():
    screen.blit(bg_image, (0 - scroll, 0))

def spawn_mob(type,direction):
    if direction == "right":
        mobs.append(Mob((posx + 300, posy), type, things))
    else:
        mobs.append(Mob((posx - 300, posy), type, things))

def spawn_boss(type):
    bosses.append(Boss((posx + 300, posy - 100), type, things))

def spawncheck(scroll,spawn_interval):
    if scroll > 1000:
        if scroll % spawn_interval == 0:
            spawn_mob("grunt","right")
            if scroll % 400 == 0:
                spawn_mob("grunt","left")
            if scroll % 600 == 0:
                spawn_mob("archer","right")
            spawn_interval += 200
    return spawn_interval

def textcontroller(scroll):
    if scroll < 150:
        return "You, a vampire lord awaken after thousands of years of slumber, move right to progress"
    elif scroll < 300:
        return "You must fight to retake your castle"
    elif scroll < 500:
        return "Controls: arrow keys to move, c is jump, z is attack"
    elif scroll < 700:
        return "grunts will charge straight at you and swing"
    elif scroll < 900:
        return "archers will try to stay a certain distance from you and fire"
    elif scroll < 1200:
        return "clear all enemies in a distance of 7000 paces to reclaim your castle"
    else:
        return ""

#blocker related functions
def blockerspawn():
    for i in range(5):
        mobs.append(Mob((posx + random.randint(200 + i, 300), posy), "grunt", things))
        mobs.append(Mob((posx - random.randint(200 + i, 300), posy), "grunt", things))
    for i in range(2):
        mobs.append(Mob((posx + random.randint(200 + i, 300), posy), "archer", things))
        mobs.append(Mob((posx - random.randint(200 + i, 300), posy), "archer", things))
    spawn_boss("grunt")

def blockerchecker(scroll, blockerpositions):
    positions_copy = blockerpositions.copy()
    for position in positions_copy:
        if position == scroll:
            blockerpositions.remove(position)
            return True
    else:
        return False

run = True
menu = False
while run:
    clock.tick(FPS) 
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if menu:
                    menu = False
                else:
                    menu = True

    #temporary win condition of reaching the end of the level and beating all mobs
    if scroll >= 7000 and not mobs and not bosses:
        win = True
        menu = True

    #if user is in the menu
    if menu:

        if win or loss:
            #move through menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(gameover_menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(gameover_menu_options)
                elif event.key == pygame.K_RETURN:
                    #do the selected menu option (Resume, Options, Quit)
                    if selected_option == 0:
                        menu = False
                        loss = False
                        win = False
                        player_character.healSelf()
                        scroll = 0
                        mobs = []
                        bosses = []
                        things = []
                        spawn_interval = 200
                        First_grunt = False
                        First_archer = False
                        blockerpositions = [2000,4000,6000]
                    elif selected_option == 1:
                        run = False
                        
            elif event.type == pygame.KEYUP:
                pass
                
            #show the menu
            for i, option in enumerate(gameover_menu_options):
                text = MENU_FONT.render(option, True, (255, 255, 255))
                menu_message_rect = lose_message.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
                text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + i * 50))
                #highlight selected option
                if i == selected_option:
                    pygame.draw.rect(screen, (255, 0, 0), text_rect, 2)  
                #unhighlight other options
                else:
                    pygame.draw.rect(screen, (0, 0, 0), text_rect, 2)  
                screen.blit(text, text_rect)
                if win:
                    screen.blit(win_message, menu_message_rect)
                else:
                    screen.blit(lose_message, menu_message_rect)
        else:
            #move through menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    #do the selected menu option (Resume, Options, Quit)
                    if selected_option == 0:
                        menu = False
                    elif selected_option == 1:
                        run = False
            elif event.type == pygame.KEYUP:
                pass

            #show the menu
            for i, option in enumerate(menu_options):
                text = MENU_FONT.render(option, True, (255, 255, 255))
                menu_message_rect = option_message.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
                text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + i * 50))
                #highlight selected option
                if i == selected_option:
                    pygame.draw.rect(screen, (255, 0, 0), text_rect, 2)  
                #unuhighlight other options
                else:
                    pygame.draw.rect(screen, (0, 0, 0), text_rect, 2)  
                screen.blit(text, text_rect)
                screen.blit(option_message, menu_message_rect)

    #otherwise run the game
    else:
        if First_grunt == False and scroll == 500:
            First_grunt = True
            mobs.append(Mob((posx + 300, posy), "grunt", things))

        if First_archer == False and scroll == 700:
            First_archer = True
            mobs.append(Mob((posx + 300, posy), "archer", things))
        
        spawn_interval = spawncheck(scroll,spawn_interval)
        #updates message for display over the characters head
        message = textcontroller(scroll)
        overhead_text = MENU_FONT.render(message, True, (255, 255, 255))

        #process entity behavior
        player_character.handle_event(event)
        for mob in mobs:
            mob.handle_event(player_character,event, mobs)
        for boss in bosses:
            boss.handle_event(player_character,event, bosses)
        for thing in things:
            thing.handle_event(player_character,event, things)

        player_health = player_character.getHealth()
        if player_health <= 0:
            loss = True
            menu = True

        #handle scrolling and blockers
        key = pygame.key.get_pressed()
        if blockeractive == False:
            if blockerchecker(scroll,blockerpositions):
                scroll_lock = scroll
                blockeractive = True
                for position in blockerpositions:
                    if scroll_lock == position:
                        blockerpositions.remove(position)
                        break
                blockerspawn()
        if blockeractive:
            message = "The enemies surround you. Defeat them all to continue"
            if key[pygame.K_LEFT] and scroll > scroll_lock - 300:
                scroll -= scrollspeed
                for mob in mobs:
                    mob.scroller(scrollspeed)
                for boss in bosses:
                    boss.scroller(scrollspeed)
                for thing in things:
                    thing.scroller(scrollspeed)
            if key[pygame.K_RIGHT] and scroll < scroll_lock + 300:
                scroll += scrollspeed
                for mob in mobs:
                    mob.scroller(-scrollspeed)
                for boss in bosses:
                    boss.scroller(-scrollspeed)
                for thing in things:
                    thing.scroller(-scrollspeed)
            if len(mobs) == 0 and len(bosses) == 0:
                blockeractive = False
        else:
            if key[pygame.K_LEFT] and scroll > 0:
                scroll -= scrollspeed
                for mob in mobs:
                    mob.scroller(scrollspeed)
                for boss in bosses:
                    boss.scroller(scrollspeed)
            if key[pygame.K_RIGHT] and scroll < 7200:
                scroll += scrollspeed
                for mob in mobs:
                    mob.scroller(-scrollspeed)
                for boss in bosses:
                    boss.scroller(-scrollspeed)        

        #redraw screen and entities
        screen.fill((0, 0, 0))
        draw_bg() 
        screen.blit(player_character.display_frame, player_character.rect)
        for mob in mobs:
            screen.blit(mob.display_frame, mob.rect)
        for boss in bosses:
            screen.blit(boss.display_frame, boss.rect)
        for thing in things:
            screen.blit(thing.display_frame, thing.rect)
        
        message_text = Message_Font.render(f"{message}", True, (255, 255, 255))
        screen.blit(message_text, (250, 100))

        health_text = Health_FONT.render(f"Health: {player_health}", True, (255, 255, 255))
        Distance = Distance_FONT.render(f"Distance: {scroll}", True, (255, 255, 255))
        screen.blit(health_text, (10, 10))
        screen.blit(Distance, (670, 10))
    
    pygame.display.flip()
#quit game
pygame.quit()
