from turtle import color
import pgzrun
import random
from pygame import Rect

WIDTH = 800
HEIGHT = 600

background = Actor("background")
sound = Actor("mute")
sound.x = 20
sound.y = 580

song_playing = False
jumping = False
vertical_speed = 0
gravity = 1.25
jump_force = -25
floor = 550

state = "startscreen"

def iniciarJogo():
    global state
    if keyboard[keys.SPACE] and state == "startscreen":
        generate_platforms()
        coin_generate()
        sounds.click.play()
        state = "game"

main_character = Actor("principal/principal")
main_character.x = 400
main_character.y = 550

enemy_one = Actor("enemies/saw")
enemy_one.x = 50
enemy_one.y = 340


enemy_two = Actor("enemies/mouse")
enemy_two.x = 610
enemy_two.y = 182
enemy_two_direction = -1

platforms = []
platforms_xy = [
    (400, 550),
    (140, 390),
    (610, 230),
    ]

def generate_platforms():
    global platforms
    for x in range(len(platforms_xy)):
       platform = Actor("platform") 
       platform.x = platforms_xy[x][0]
       platform.y = platforms_xy[x][1]
       platforms.append(platform)


coins = []

coin_count = 0

coin_one = True

coins_xy = [
    (400, 440),
    (50, 250),
    (550, 140)
]
def coin_generate():
    for x in range(3):
        coin = Actor("coin_one")
        coin.x = coins_xy[x][0]
        coin.y = coins_xy[x][1]
        coins.append(coin)

def coin_flip():
    global coin_one
    coin_one = not coin_one
    if coin_one:
        for coin in coins:
            coin.image = "coin_one"
    else:
        for coin in coins:
            coin.image = "coin_two"

def check_victory():
    global state
    if len(coins) == 0 and state == "game":
        main_character.image = "principal/victory"
        state = "victory"
    
clock.schedule_interval(coin_flip, 0.5)

def on_mouse_down(pos,button):
    if sound.collidepoint(pos) and button == mouse.LEFT:
        if sound.image == "mute":
            sound.image = "unmute"
        else:
            sound.image = "mute"

def song_play():
    global song_playing 
    if sound.image == "mute" and not song_playing:
        sounds.song.play()
        sounds.song.set_volume(0.08)
        song_playing = True
    elif sound.image == "unmute":
        sounds.song.stop()
        song_playing = False
    if state == "game" : 
        sounds.song.stop()




def check_platform_colision():
    global jumping, vertical_speed
    onplatform = False

    if vertical_speed >= 0: 
        for platform in platforms:
            character_bottom = main_character.y + main_character.height // 2
            next_bottom = character_bottom + vertical_speed

            platform_top = platform.y - platform.height // 2
            platform_left = platform.x - platform.width // 2
            platform_right = platform.x + platform.width // 2
            character_left = main_character.x - main_character.width // 2
            character_right = main_character.x + main_character.width // 2

            horizontal_colision = character_right > platform_left and character_left < platform_right
            will_colide_top = character_bottom <= platform_top and next_bottom >= platform_top

            if horizontal_colision and will_colide_top:
                main_character.y = platform_top - main_character.height // 2
                vertical_speed = 0
                jumping = False
                onplatform = True
                break
           

    if not onplatform and not jumping:
        jumping = True
        vertical_speed = 0

def check_coin_colision():
    global coin_count
    for coin in coins[:]:
        if main_character.colliderect(coin):
            coins.remove(coin)
            coin_count += 1
            sounds.coin.play()
            sounds.coin.set_volume(0.3)

def check_enemy_colision():
    global state
    if main_character.colliderect(enemy_one) or main_character.colliderect(enemy_two):
        main_character.image = "principal/gameover"
        state = "gameover"
        sounds.gameover.play()

def mouse_movement():  
    global enemy_two_direction

    enemy_two.x += 2 * enemy_two_direction

    if enemy_two.x >= 730:
        enemy_two_direction = -1
        enemy_two.image = "enemies/mouse"
    elif enemy_two.x <= 480:
        enemy_two_direction = 1
        enemy_two.image = "enemies/mouse_flipped"



def update():
    global jumping, vertical_speed,state
    
    if state == "gameover" or state =="victory":
        return
    song_play()
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

    
    check_platform_colision()


    if jumping:
        main_character.image = "principal/jumping"
        main_character.y += vertical_speed
        vertical_speed += gravity

        if main_character.y >= floor:
            main_character.y = floor
            jumping = False
            vertical_speed = 0 
    
    

    if not jumping:
        main_character.image = "principal/principal"



    check_coin_colision()
    check_enemy_colision()
    check_victory()
    mouse_movement()

def draw():
    screen.clear()
    background.draw()

    if state == "startscreen":
        screen.draw.text("Meu Jogo", center=(WIDTH // 2,100), fontsize=100)
        screen.draw.text("Pressione Espaço para iniciar o jogo", center=(WIDTH// 2 , 300), fontsize=50)
        sound.draw()


    if state == "game":
        main_character.draw()
        for platform in platforms:
            platform.draw()
        for coin in coins:
            coin.draw()
        screen.draw.text(f"Moedas : {coin_count}", topleft=(20,20), fontsize=40)
        enemy_one.draw()
        enemy_two.draw()
    if state == "gameover":
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=100, color="black")
        main_character.draw()
    if state == "victory":
        screen.draw.text("VICTORY", center=(WIDTH//2, HEIGHT//2), fontsize=100,color="yellow")
        main_character.draw()


pgzrun.go()

