import math
import pygame
import random
from pygame import mixer

#Initialize the pygame
pygame.init()
clock = pygame.time.Clock()

#create the screen
screen = pygame.display.set_mode((800, 600))
# Background
background = pygame.image.load('background.jpg')

# Background Sound
mixer.music.load('space-background.mp3')
mixer.music.play(-1)

#Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player1
playerImg1 = pygame.image.load('player.png')
playerImg1 = pygame.transform.scale(playerImg1, (70, 80))


# Player2
playerImg2 = pygame.image.load('player2.png')
playerImg2 = pygame.transform.scale(playerImg2, (70, 80))

# Enemy
enemy = pygame.image.load('enemy.png')

# Bullet
bulletImg1 = pygame.image.load('bullet1.png')
bulletImg1 = pygame.transform.scale(bulletImg1, (30, 30))
bulletImg2 = pygame.image.load('bullet2.png')

# Fuente texto
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Variable global
ENEMY_SPEED = 5

# Clases
class Player:
    def __init__(self, img):
        self.image = img
        self.x = 370
        self.y = 480
        self.x_change = 0
        self.speed = 4

    def move(self):
        self.x += self.x_change
        # Limitar movimiento dentro de la pantalla
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Enemy:
    def __init__(self):
        self.image = enemy
        self.x = random.randint(0, 735)
        self.y = random.randint(50, 150)
        self.x_change = ENEMY_SPEED
        self.y_change = 40

    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = ENEMY_SPEED
            self.y += self.y_change
        elif self.x >= 736:
            self.x_change = -ENEMY_SPEED
            self.y += self.y_change

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Bullet:
    def __init__(self, img):
        self.image = img
        self.x = 0
        self.y = 480
        self.y_change = 10
        self.state = "ready"  # "ready" o "fire"
    def fire(self, x, y):
        self.state = "fire"
        self.x = x + 24  # Ajuste para centrar la bala
        self.y = y + 10
    def move(self):
        if self.state == "fire":
            self.y -= self.y_change
            if self.y <= 0:
                self.state = "ready"
                self.y = 480
    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self.image, (self.x, self.y))

# Funciones
def is_collision(enemy, bullet1):
    distance = math.sqrt((math.pow(enemy.x - bullet1.x, 2)) + (math.pow(enemy.y - bullet1.y, 2)))
    return distance < 27


def show_score(x, y, score):
    score_text = font.render("Score: " + str(score), True, (0, 255, 0))
    screen.blit(score_text, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (200, 250))

def you_win_text():
    win_text = over_font.render("YOU WIN!", True, (0, 255, 0))
    screen.blit(win_text, (250, 250))

# Crear instancias
player1 = Player(playerImg1)
player2 = Player(playerImg2)

enemies = [Enemy() for _ in range(6)]
bullet1 = Bullet(bulletImg1)
bullet2 = Bullet(bulletImg2)
score_value = 0


# Loop principal del juego
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detectar teclas presionadas
        if event.type == pygame.KEYDOWN:
            # Player 1
            if event.key == pygame.K_LEFT:
                player1.x_change = -player1.speed
            if event.key == pygame.K_RIGHT:
                player1.x_change = player1.speed
            if event.key == pygame.K_SPACE:
                if bullet1.state == "ready":
                    bullet_sound = mixer.Sound('laser.mp3')
                    bullet_sound.play()
                    bullet1.fire(player1.x, player1.y)
            # Player 2
            if event.key == pygame.K_a:
                player2.x_change = -player2.speed
            if event.key == pygame.K_d:
                player2.x_change = player2.speed
            if event.key == pygame.K_p:
                if bullet2.state == "ready":
                    bullet_sound = mixer.Sound('laser.mp3')
                    bullet_sound.play()
                    bullet2.fire(player2.x, player2.y)

        if event.type == pygame.KEYUP:
            # Player 1
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player1.x_change = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player2.x_change = 0

    # Mover jugador
    player1.move()
    player2.move()

    # Mover y dibujar enemigos
    for enemy in enemies:
        # Verificar game over
        if enemy.y > 440:
            for e in enemies:
                e.y = 2000  # Sacar enemigos de la pantalla
            game_over_text()
            break

        enemy.move()

        # Verificar colisión con bala
        if is_collision(enemy, bullet1):
            explosion_sound = mixer.Sound('impact.mp3')
            explosion_sound.play()
            bullet1.state = "ready"
            bullet1.y = 480
            score_value += 1
            enemies.remove(enemy) # quita enemigo
            if not enemies:  # Verifica si queda enemigos
                you_win_text()
                running = False

        if is_collision(enemy, bullet2):
            explosion_sound = mixer.Sound('impact.mp3')
            explosion_sound.play()
            bullet2.state = "ready"
            bullet2.y = 480
            score_value += 1
            enemies.remove(enemy)
            if not enemies:
                you_win_text()
                running = False

        enemy.draw(screen)

    # Mover y dibujar bala
    bullet1.move()
    bullet1.draw(screen)

    bullet2.move()
    bullet2.draw(screen)

    # Dibujar jugador y score
    player1.draw(screen)
    player2.draw(screen)
    show_score(10, 10, score_value)

    pygame.display.update()
    clock.tick(60)


