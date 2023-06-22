"""Autor: Kevin Thalmann."""
from pathlib import Path

import pygame

ROOT_PATH = Path.cwd()

WIDHT, HEIGHT = 1800, 1000
SPACESHIP_WIDHT, SPACESHIP_HEIGT = 150, 150
FPS = 60
VELOCITY = 10
NUMBER_BULLETS = 4
VELOCITY_BULLETS = 20

pygame.font.init()
player_01_hit = pygame.USEREVENT + 1
player_02_hit = pygame.USEREVENT + 2

rand = pygame.Rect(WIDHT // 2 - 5, 0, 10, HEIGHT)

health_font = pygame.font.SysFont("comicsans", 40)
winner_font = pygame.font.SysFont("comicsans", 100)
bullet_font = pygame.font.SysFont("comicsane", 30)

win = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("Kevins Game")

backround = pygame.image.load(
    ROOT_PATH / "Assets" / "Hintergrund_01.jpg"
    )
backround = pygame.transform.scale(backround, (WIDHT, HEIGHT))

space_ship_01 = pygame.image.load(
    ROOT_PATH / "Assets" / "Spaceship.png"
    )
space_ship_01 = pygame.transform.scale(
    space_ship_01,
    (SPACESHIP_WIDHT, SPACESHIP_HEIGT)
    )

space_ship_02 = pygame.image.load(
    ROOT_PATH / "Assets" / "Spaceship.png"
    )
space_ship_02 = pygame.transform.scale(
    space_ship_02,
    (SPACESHIP_WIDHT, SPACESHIP_HEIGT)
    )
space_ship_02 = pygame.transform.rotate(space_ship_02, 180)


def draw_window(
    player_01: str,
    player_02: str,
    bullets_player_01: str,
    bullets_player_02: str,
    player_01_health: str,
    player_02_health: str,
) -> None:
    """Draw the window.

    Args:
        player_01: _description_
        player_02: _description_
        bullets_player_01: _description_
        bullets_player_02: _description_
        player_01_health: _description_
        player_02_health: _description_
    """
    win.blit(backround, (0, 0))
    pygame.draw.rect(win, (0, 0, 0), rand)

    player_01_health_text = health_font.render(
        "Leben: " + str(player_01_health), 1, (255, 255, 255)
    )
    player_02_health_text = health_font.render(
        "Leben: " + str(player_02_health), 1, (255, 255, 255)
    )

    player_01_bullet_text = bullet_font.render(
        "Anzahl an Kugeln: " + str(NUMBER_BULLETS - len(bullets_player_01)),
        1,
        (255, 0, 0),
    )
    player_02_bullet_text = bullet_font.render(
        "Anzahl an Kugeln: " + str(NUMBER_BULLETS - len(bullets_player_02)),
        1,
        (255, 255, 0),
    )
    win.blit(player_01_health_text, (10, 0))
    win.blit(
        player_02_health_text, (WIDHT - player_02_health_text.get_width() - 10, 0)
    )
    win.blit(player_01_bullet_text, (10, 60))
    win.blit(
        player_02_bullet_text, (WIDHT - player_02_bullet_text.get_width() - 10, 60)
    )
    win.blit(space_ship_01, (player_01.x, player_01.y))
    win.blit(space_ship_02, (player_02.x, player_02.y))

    for buttel in bullets_player_01:
        pygame.draw.rect(win, (255, 0, 0), buttel)
    for buttel in bullets_player_02:
        pygame.draw.rect(win, (255, 255, 0), buttel)

    pygame.display.update()


def move_player_01(key_pressed: str, player_01: str) -> None:
    """Move the Player 01.

    Args:
        key_pressed: _description_
        player_01: _description_
    """
    if key_pressed[pygame.K_a] and player_01.x - VELOCITY > 0:  # links
        player_01.x -= VELOCITY
    if (
        key_pressed[pygame.K_d]
        and player_01.x + VELOCITY < rand.x - SPACESHIP_HEIGT
    ):  # rechts
        player_01.x += VELOCITY
    if key_pressed[pygame.K_w] and player_01.y - VELOCITY > 0:  # hoch
        player_01.y -= VELOCITY
    if (
        key_pressed[pygame.K_s]
        and player_01.y + VELOCITY + SPACESHIP_HEIGT < HEIGHT
    ):  # runter
        player_01.y += VELOCITY


def move_player_02(key_pressed: str, player_02: str) -> None:
    """Move the Player 02.

    Args:
        key_pressed: _description_
        player_02: _description_
    """
    if (
        key_pressed[pygame.K_LEFT] and player_02.x - VELOCITY > rand.x + 10
    ):  # links
        player_02.x -= VELOCITY
    if (
        key_pressed[pygame.K_RIGHT]
        and player_02.x + VELOCITY < WIDHT - SPACESHIP_HEIGT
    ):  # rechts
        player_02.x += VELOCITY
    if key_pressed[pygame.K_UP] and player_02.y - VELOCITY > 0:  # hoch
        player_02.y -= VELOCITY
    if (
        key_pressed[pygame.K_DOWN]
        and player_02.y + VELOCITY + SPACESHIP_HEIGT < HEIGHT
    ):  # runter
        player_02.y += VELOCITY


def handle_bullets(bullets_player_01: str,
                   bullets_player_02: str,
                   player_01: str,
                   player_02: str) -> None:
    """Handle the bullets.

    Args:
        bullets_player_01: _description_
        bullets_player_02: _description_
        player_01: _description_
        player_02: _description_
    """
    for bullets in bullets_player_01:
        bullets.x += VELOCITY_BULLETS
        if player_02.colliderect(bullets):
            pygame.event.post(pygame.event.Event(player_02_hit))
            bullets_player_01.remove(bullets)
        elif bullets.x > WIDHT:
            bullets_player_01.remove(bullets)
    for bullets in bullets_player_02:
        bullets.x -= VELOCITY_BULLETS
        if player_01.colliderect(bullets):
            pygame.event.post(pygame.event.Event(player_01_hit))
            bullets_player_02.remove(bullets)
        elif bullets.x < 0:
            bullets_player_02.remove(bullets)


def draw_winner(winner_text: str) -> None:
    """Draw the winner text.

    Args:
        winner_text: _description_
    """
    draw_text = winner_font.render(winner_text, 1, (255, 255, 255))
    win.blit(
        draw_text,
        (
            (WIDHT / 2 - draw_text.get_width() / 2),
            HEIGHT / 2 - draw_text.get_height() // 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(5000)


def start_game() -> None:
    """Start the game."""
    player_01 = pygame.Rect(100, 200, SPACESHIP_WIDHT, SPACESHIP_HEIGT)
    player_02 = pygame.Rect(1250, 200, SPACESHIP_WIDHT, SPACESHIP_HEIGT)
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
                print("Game wurde beendet")
            if event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_LCTRL
                    and len(bullets_player_01) < NUMBER_BULLETS
                ):
                    bullet = pygame.Rect(
                        player_01.x + player_01.width,
                        player_01.y + player_01.height // 2 - 2,
                        25,
                        5,
                    )
                    bullets_player_01.append(bullet)
                if (
                    event.key == pygame.K_RCTRL
                    and len(bullets_player_02) < NUMBER_BULLETS
                ):
                    bullet = pygame.Rect(
                        player_02.x, player_02.y + player_02.height // 2 - 2, 25, 5
                    )
                    bullets_player_02.append(bullet)

            if event.type == player_01_hit:
                player_01_health -= 1
            if event.type == player_02_hit:
                player_02_health -= 1
        winner_text = ""
        if player_01_health <= 0:
            winner_text = "Player 2 hat gewonnen"
        if player_02_health <= 0:
            winner_text = "Player 1 hat gewonnen"
        if winner_text != "":
            draw_winner(winner_text)
        key_pressed = pygame.key.get_pressed()
        move_player_01(key_pressed, player_01)
        move_player_02(key_pressed, player_02)
        handle_bullets(bullets_player_01, bullets_player_02, player_01, player_02)
        draw_window(
            player_01,
            player_02,
            bullets_player_01,
            bullets_player_02,
            player_01_health,
            player_02_health,
        )
    pygame.quit()


if __name__ == "__main__":
    start_game()

