import pgzrun
import random
from pygame import Rect

WIDTH = 800
HEIGHT = 600

background = Actor("background")

jumping = False
vertical_speed = 0
gravity = 1.25
jump_force = -25
floor = 550

state = "startscreen"

RED = 200, 0, 0
BOX = Rect((20, 20), (100, 100))

#funcionamento de um Rect meu_rect = Rect((x, y), (largura, altura))




def iniciarJogo():
    global state
    if keyboard[keys.SPACE] and state == "startscreen":
        generate_platforms()
        sounds.click.play()
        state = "game"

main_character = Actor("principal/principal")
main_character.x = 400
main_character.y = 550


platforms = []

platforms_xy = [  
    (100, 550),
    (200, 470,),
    (300, 390),
    (400, 310),
    (500, 230),
    (600, 150),
    (700, 70)
    ]

def generate_platforms():
    global platforms
    for x in range(len(platforms_xy)):
       platform = Actor("plataforma") 
       platform.x = platforms_xy[x][0]
       platform.y = platforms_xy[x][1]
       platforms.append(platform)
        




def update():
    global jumping, vertical_speed




    iniciarJogo()

    
    if keyboard.left:
        main_character.x -= 5
    if keyboard.right:
        main_character.x += 5
    if main_character.x < 35:
        main_character.x = 35
    if main_character.x > WIDTH - 35:
        main_character.x = WIDTH - 35


    if not jumping and keyboard.space:
        jumping = True
        vertical_speed = jump_force
        sounds.jump.play()
        sounds.jump.set_volume(0.3)

    if jumping:

 
        main_character.y += vertical_speed
        vertical_speed += gravity

        if main_character.y >= floor:
            main_character.y = floor
            jumping = False
            vertical_speed = 0 

def draw():
    screen.clear()
    background.draw()

    if state == "startscreen":
        screen.draw.text("Meu Jogo", center=(WIDTH // 2,100), fontsize=100)
        screen.draw.text("Pressione Espaço para iniciar o jogo", center=(WIDTH// 2 , 300), fontsize=50)



    if state == "game":
        for platform in platforms:
            platform.draw()
        main_character.draw()
        screen.draw.rect(BOX, RED)



pgzrun.go()

