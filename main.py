import pygame
import sys
import random

pygame.init()

pygame.mixer.init()
hit_sound = pygame.mixer.Sound("hit.mp3")  # Ölünce çalacak ses
score_sound = pygame.mixer.Sound("score.mp3")  # Hedefe ulaşınca çalacak ses

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Pygame")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (50, 50))

enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (50, 50))

target_image = pygame.image.load("target.png")
target_image = pygame.transform.scale(target_image, (30, 30))

obstacle_image = pygame.image.load("obstacle.png")
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))

player_size = player_image.get_width(), player_image.get_height()
enemy_size = enemy_image.get_width(), enemy_image.get_height()
target_size = target_image.get_width(), target_image.get_height()
obstacle_size = obstacle_image.get_width(), obstacle_image.get_height()


def game_loop():
    global score
    player_x = screen_width // 4
    player_y = screen_height // 2

    target_x = random.randint(0, screen_width - target_size[0])
    target_y = random.randint(0, screen_height - target_size[1])

    enemy_x = screen_width - 100
    enemy_y = random.randint(0, screen_height - enemy_size[1])
    enemy_speed = 1

    num_obstacles = 5
    obstacles = []
    for i in range(num_obstacles):
        obs_x = random.randint(0, screen_width - obstacle_size[0])
        obs_y = random.randint(0, screen_height - obstacle_size[1])
        obstacles.append((obs_x, obs_y))

    score = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        screen.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= 5
        if keys[pygame.K_RIGHT]:
            player_x += 5
        if keys[pygame.K_UP]:
            player_y -= 5
        if keys[pygame.K_DOWN]:
            player_y += 5

        if enemy_x < player_x:
            enemy_x += enemy_speed
        if enemy_x > player_x:
            enemy_x -= enemy_speed
        if enemy_y < player_y:
            enemy_y += enemy_speed
        if enemy_y > player_y:
            enemy_y -= enemy_speed

        if (player_x < target_x + target_size[0] and
                player_x + player_size[0] > target_x and
                player_y < target_y + target_size[1] and
                player_y + player_size[1] > target_y):
            score += 1
            score_sound.play()
            target_x = random.randint(0, screen_width - target_size[0])
            target_y = random.randint(0, screen_height - target_size[1])

        for obstacle in obstacles:
            if (player_x < obstacle[0] + obstacle_size[0] and
                    player_x + player_size[0] > obstacle[0] and
                    player_y < obstacle[1] + obstacle_size[1] and
                    player_y + player_size[1] > obstacle[1]):
                hit_sound.play()
                game_over(score)
                return

        if (player_x < enemy_x + enemy_size[0] and
                player_x + player_size[0] > enemy_x and
                player_y < enemy_y + enemy_size[1] and
                player_y + player_size[1] > enemy_y):
            hit_sound.play()
            game_over(score)
            return

        screen.blit(player_image, (player_x, player_y))
        screen.blit(target_image, (target_x, target_y))
        screen.blit(enemy_image, (enemy_x, enemy_y))

        for obstacle in obstacles:
            screen.blit(obstacle_image, (obstacle[0], obstacle[1]))

        score_text = font.render(f"Puan: {score}", True, black)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        pygame.time.Clock().tick(60)


def game_over(final_score):
    screen.fill(white)

    font_large = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)

    game_over_text = font_large.render("Kaybettin!", True, red)
    score_text = font_small.render(f"Skor: {final_score}", True, black)
    restart_text = font_small.render("Yeniden Oyna (R)", True, black)

    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 3))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height * 2 // 3))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()


game_loop()

pygame.quit()
sys.exit()
