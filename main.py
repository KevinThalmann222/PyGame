import pygame
import os
pygame.font.init()

WIDHT, HEIGHT = 1800, 1000
Spaceship_WIDHT, Spaceship_HEIGT = 150, 150
FPS = 60
Geschwindigkeit = 10
Nummer_bullets = 4

Geschwindigkeit_bullets = 20

player_01_hit = pygame.USEREVENT + 1
player_02_hit = pygame.USEREVENT + 2

Rand = pygame.Rect(WIDHT//2 -5, 0, 10, HEIGHT)

Health_Font = pygame.font.SysFont('comicsans', 40)
Winner_Font = pygame.font.SysFont('comicsans', 100)
Bullet_Font = pygame.font.SysFont('comicsane', 30)

WIN = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("Kevins Game")


Hintergrund = pygame.image.load(r'D:\04_TG-C23\02_Python\PyGame\Assets\Hintergrund_01.jpg')
Hintergrund = pygame.transform.scale(Hintergrund, (WIDHT,HEIGHT))

SpaceShip_01 = pygame.image.load(r'D:\04_TG-C23\02_Python\PyGame\Assets\Spaceship.png')
SpaceShip_01 = pygame.transform.scale(SpaceShip_01, (Spaceship_WIDHT,Spaceship_HEIGT))

SpaceShip_02 = pygame.image.load(r'D:\04_TG-C23\02_Python\PyGame\Assets\Spaceship.png')
SpaceShip_02 = pygame.transform.scale(SpaceShip_02, (Spaceship_WIDHT,Spaceship_HEIGT))
SpaceShip_02 = pygame.transform.rotate(SpaceShip_02, 180)




def draw_window(player_01, player_02, bullets_player_01, bullets_player_02,player_01_health,player_02_health):
    WIN.blit(Hintergrund, (0,0))
    pygame.draw.rect(WIN, (0,0,0), Rand)

    player_01_health_text = Health_Font.render("Leben: " + str(player_01_health), 1, (255,255,255))
    player_02_health_text = Health_Font.render("Leben: " + str(player_02_health), 1, (255, 255, 255))

    player_01_bullet_text = Bullet_Font.render("Anzahl an Kugeln: " + str(Nummer_bullets-len(bullets_player_01)),1, (255,0,0) )
    player_02_bullet_text = Bullet_Font.render("Anzahl an Kugeln: " + str(Nummer_bullets - len(bullets_player_02)), 1,(255,255,0) )


    WIN.blit(player_01_health_text, (10,10))
    WIN.blit(player_02_health_text, (WIDHT-player_02_health_text.get_width()-10,10))

    WIN.blit(player_01_bullet_text, (10,50))
    WIN.blit(player_02_bullet_text, (WIDHT-player_02_bullet_text.get_width()-10,50))

    WIN.blit(SpaceShip_01, (player_01.x, player_01.y))
    WIN.blit(SpaceShip_02, (player_02.x, player_02.y))


    for buttel in bullets_player_01:
        pygame.draw.rect(WIN, (255,0,0), buttel)

    for buttel in bullets_player_02:
        pygame.draw.rect(WIN, (255,255,0), buttel)

    pygame.display.update()

def move_player01(key_pressed, player_01):
    if key_pressed[pygame.K_a] and player_01.x - Geschwindigkeit > 0:                               # links
        player_01.x -= Geschwindigkeit
    if key_pressed[pygame.K_d] and player_01.x + Geschwindigkeit < Rand.x-Spaceship_HEIGT:          # rechts
        player_01.x += Geschwindigkeit
    if key_pressed[pygame.K_w] and player_01.y - Geschwindigkeit > 0:                               # hoch
        player_01.y -= Geschwindigkeit
    if key_pressed[pygame.K_s] and player_01.y + Geschwindigkeit + Spaceship_HEIGT < HEIGHT:        # runter
        player_01.y += Geschwindigkeit

def move_player02(key_pressed, player_02):
    if key_pressed[pygame.K_LEFT] and player_02.x - Geschwindigkeit > Rand.x+10:        # links
        player_02.x -= Geschwindigkeit
    if key_pressed[pygame.K_RIGHT] and player_02.x + Geschwindigkeit < WIDHT-Spaceship_HEIGT:     # rechts
        player_02.x += Geschwindigkeit
    if key_pressed[pygame.K_UP] and player_02.y - Geschwindigkeit > 0:        # hoch
        player_02.y -= Geschwindigkeit
    if key_pressed[pygame.K_DOWN] and player_02.y + Geschwindigkeit + Spaceship_HEIGT < HEIGHT:      # runter
        player_02.y += Geschwindigkeit

def handle_bullets(bullets_player_01, bullets_player_02, player_01, player_02):
    for bullets in bullets_player_01:
        bullets.x += Geschwindigkeit_bullets
        if player_02.colliderect(bullets):
            pygame.event.post(pygame.event.Event(player_02_hit))
            bullets_player_01.remove(bullets)
        elif bullets.x > WIDHT:
            bullets_player_01.remove(bullets)

    for bullets in bullets_player_02:
        bullets.x -= Geschwindigkeit_bullets
        if player_01.colliderect(bullets):
            pygame.event.post(pygame.event.Event(player_01_hit))
            bullets_player_02.remove(bullets)
        elif bullets.x < 0:
            bullets_player_02.remove(bullets)

def draw_winner(Winner_Text):
    draw_text = Winner_Font.render(Winner_Text,1, (255,255,255))
    WIN.blit(draw_text, ((WIDHT/2-draw_text.get_width()/2),HEIGHT/2-draw_text.get_height()//2))

    pygame.display.update()
    pygame.time.delay(5000)



def game():
    player_01 = pygame.Rect(100,200, Spaceship_WIDHT, Spaceship_HEIGT)
    player_02 = pygame.Rect(1250,200, Spaceship_WIDHT, Spaceship_HEIGT)

    bullets_player_01 = []
    bullets_player_02 = []

    player_01_health = 10
    player_02_health = 10

    run = True
    clock = pygame.time.Clock()

    while run:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print('Game wurde beendet')

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(bullets_player_01) < Nummer_bullets:
                    bullet = pygame.Rect(player_01.x + player_01.width,player_01.y + player_01.height//2 -2, 25, 5)
                    bullets_player_01.append(bullet)


                if event.key == pygame.K_RCTRL and len(bullets_player_02) < Nummer_bullets:
                    bullet = pygame.Rect(player_02.x, player_02.y + player_02.height//2 - 2, 25,5)
                    bullets_player_02.append(bullet)

            if event.type == player_01_hit:
                player_01_health -=1

            if event.type == player_02_hit:
                player_02_health -= 1

        Winner_Text = ""
        if player_01_health <= 0:
            Winner_Text = "Player 2 hat gewonnen"

        if player_02_health <= 0:
            Winner_Text = "Player 1 hat gewonnen"

        if Winner_Text != "":
            draw_winner(Winner_Text)


        key_pressed = pygame.key.get_pressed()
        move_player01(key_pressed, player_01)
        move_player02(key_pressed, player_02)
        handle_bullets(bullets_player_01, bullets_player_02, player_01, player_02)
        draw_window(player_01, player_02, bullets_player_01, bullets_player_02,player_01_health, player_02_health)

    pygame.quit()

if __name__ == "__main__":
    game()

