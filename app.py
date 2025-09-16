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

# Player
playerImg = pygame.image.load('player.png')
playerImg = pygame.transform.scale(playerImg, (70, 80))
playerX = 370
playerY = 480
playerX_change = 0

# Fuente texto
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Clases
class Player:
    def __init__(self):
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, (70, 80))
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
        self.image = pygame.image.load('enemy.png')
        self.x = random.randint(0, 735)
        self.y = random.randint(50, 150)
        self.x_change = 1
        self.y_change = 40

    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 1
            self.y += self.y_change
        elif self.x >= 736:
            self.x_change = -1
            self.y += self.y_change

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Bullet:
    def __init__(self):
        self.image = pygame.image.load('bullet.png')
        self.x = 0
        self.y = 480
        self.y_change = 10
        self.state = "ready"  # "ready" o "fire"
    def fire(self, x, y):
        self.state = "fire"
        self.x = x + 16  # Ajuste para centrar la bala
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
def is_collision(enemy, bullet):
    distance = math.sqrt((math.pow(enemy.x - bullet.x, 2)) + (math.pow(enemy.y - bullet.y, 2)))
    return distance < 27

def show_score(x, y, score):
    score_text = font.render("Score: " + str(score), True, (0, 255, 0))
    screen.blit(score_text, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (200, 250))


# Crear instancias
player = Player()
enemies = [Enemy() for _ in range(6)]
bullet = Bullet()
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
            if event.key == pygame.K_LEFT:
                player.x_change = -player.speed
            if event.key == pygame.K_RIGHT:
                player.x_change = player.speed
            if event.key == pygame.K_SPACE:
                if bullet.state == "ready":
                    bullet_sound = mixer.Sound('laser.mp3')
                    bullet_sound.play()
                    bullet.fire(player.x, player.y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0

    # Mover jugador
    player.move()

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
        if is_collision(enemy, bullet):
            explosion_sound = mixer.Sound('impact.mp3')
            explosion_sound.play()
            bullet.state = "ready"
            bullet.y = 480
            score_value += 1
            # Reposicionar enemigo
            enemy.x = random.randint(0, 736)
            enemy.y = random.randint(50, 150)

        enemy.draw(screen)

    # Mover y dibujar bala
    bullet.move()
    bullet.draw(screen)

    # Dibujar jugador y score
    player.draw(screen)
    show_score(10, 10, score_value)

    pygame.display.update()
    clock.tick(60)


