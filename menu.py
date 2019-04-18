import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

block_color = (53,115,255)

car_width = 73

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Macarena of Time')
clock = pygame.time.Clock()

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def quitgame():
    pygame.quit()
    quit()


def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def game_intro():

    intro = True
    menuColor = (0,0,0)
    colorArray = [100, 0, 100]
    incArray = [True, True, True]
    random.seed(None)

    while intro:
        #Get the each event
        for event in pygame.event.get():
            #print(event) #print the event
            #quit the fame when the user chooses to quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        element = random.randint(0,2) #random int between 0 and 2
        print(element)
        if colorArray[element] <= 100:
            incArray[element] = True
        elif colorArray[element] >= 252:
            incArray[element] = False
        if incArray[element] == True:
            colorArray[element] += 3
        else:
            colorArray[element] -= 3

        menuColor = (colorArray[0], colorArray[1], colorArray[2])

        gameDisplay.fill(menuColor)
        largeText = pygame.font.Font('CuteFont-Regular.ttf',105)
        TextSurf, TextRect = text_objects("Macarena of Time", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()

        #print(mouse)

        if 150+100 > mouse[0] > 150 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(gameDisplay, bright_green,(150,450,100,50))
        else:
            pygame.draw.rect(gameDisplay, green,(150,450,100,50))

        #button("Start",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)


        pygame.display.update()
        clock.tick(15)

game_intro()
