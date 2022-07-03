import pygame
import os


black = pygame.Color(0, 0, 0)



# bg = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer../Assets/startMenu.png'), (1536,896))

# # bg = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer../Assets/startMenu.png')


# bg2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer../Assets/levelSelector/levelSBG.png'), (1216,608))

# button = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer../Assets/startUnchecked.png'), (315,72))
# button2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer../Assets/startChecked.png'), (315,72))



# helpScreenIMG = [
#     pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer../Assets/story1.png'),
#     pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer../Assets/story2.png'),
#     pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer../Assets/help1.png'),
#     pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer../Assets/help2.png'),
#     pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer../Assets/helpBG.png')
# ]


bg = pygame.transform.scale(pygame.image.load(('../Assets/startMenu.png')), (1536,896))

# bg = pygame.image.load(('../Assets/startMenu.png')


# bg2 = pygame.transform.scale(pygame.image.load(('../Assets/levelSelector/levelSBG.png'), (1216,608))

button = pygame.transform.scale(pygame.image.load(('../Assets/startUnchecked.png')), (315,72))
button2 = pygame.transform.scale(pygame.image.load(('../Assets/startChecked.png')), (315,72))



helpScreenIMG = [
    pygame.image.load(('../Assets/story1.png')),
    pygame.image.load(('../Assets/story2.png')),
    pygame.image.load(('../Assets/help1.png')),
    pygame.image.load(('../Assets/help2.png')),
    pygame.image.load(('../Assets/helpBG.png'))
]



buttonPos = [600,600]

def startPage(displaysurface,FramePerSec,FPS):
    clicked = False
    toGame = False
    mouse = pygame.mouse.get_pos()
    displaysurface.fill(black)
    displaysurface.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True


    if mouse[0] >= buttonPos[0] and mouse[0] <= 315+buttonPos[0] and mouse[1] >= buttonPos[1] and mouse[1] <= 72+buttonPos[1]:
        displaysurface.blit(button2, buttonPos)
        if clicked:
            toGame = True
    else:
        displaysurface.blit(button, buttonPos)


    pygame.display.update()
    FramePerSec.tick(FPS)
    return toGame

helpIndex = 0

def resetHelp():
    global helpIndex
    helpIndex = 0

def helpScreen(displaysurface,FramePerSec, FPS):
    global helpIndex
    clicked = False
    displaysurface.fill(black)
    
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                helpIndex += 1
                if helpIndex == 4:
                    return True


    
    displaysurface.blit(helpScreenIMG[4], (0,0))
    displaysurface.blit(helpScreenIMG[helpIndex], (0,0))


    pygame.display.update()
    FramePerSec.tick(FPS)
    return False

def endMenu(displaysurface, FramePerSec, FPS):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    displaysurface.blit(gameover, (200,200))
    pygame.display.update()
    FramePerSec.tick(FPS)

def storyInstructions(displaysurface, font,FramePerSec, FPS):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    
    pygame.display.update()
    FramePerSec.tick(FPS)

    