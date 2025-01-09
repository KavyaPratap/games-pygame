import pygame
import sys
import random
import time

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800 
GROUND_HEIGHT = 100
BIRD_SIZE = 60
PILLAR_WIDTH = 50
PILLAR_SPACING = 3.5* BIRD_SIZE  
PILLAR_SPEED = 6
GRAVITY = 1.0098
JUMP_STRENGTH = 8
DAY_NIGHT_INTERVAL = 30 
DAY_COLOR = (173, 216, 230)  
NIGHT_COLOR = (25, 25, 112)  
GREEN = (0, 255, 0)  
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy DRONE-By KP")
bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))
font = pygame.font.Font(None, 36)
'''pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.5)  
pygame.mixer.music.play(-1)  '''
bird_x = 60
bird_y = (WINDOW_HEIGHT - GROUND_HEIGHT) // 2
bird_velocity = 0
pillars = []
score = 0
game_over = False
is_day = True
next_toggle_time = time.time() + DAY_NIGHT_INTERVAL  
highest_score = 0  

def create_pillar():
    gap_height = random.randint(100, 300) 
    top_pillar = pygame.Rect(WINDOW_WIDTH, 0, PILLAR_WIDTH, (gap_height+60) - PILLAR_SPACING// 2)
    bottom_pillar = pygame.Rect(WINDOW_WIDTH, gap_height + PILLAR_SPACING // 2, PILLAR_WIDTH, WINDOW_HEIGHT - gap_height - PILLAR_SPACING // 2)
    return top_pillar, bottom_pillar

def reset_game():
    global bird_x, bird_y, bird_velocity, score, game_over
    bird_x = 100  
    bird_y = int(0.30 * WINDOW_HEIGHT)  
    bird_velocity = 0
    score = 0
    game_over = False

reset_game()
def toggle_day_night():
    global is_day
    is_day = not is_day

reset_game()


background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))


background_x = 0


BACKGROUND_SCROLL_SPEED = 0


running = True
clock = pygame.time.Clock()
game_started = False
game_paused = False
bg_music_on = True  
game_paused = False
music_button = pygame.Rect(WINDOW_WIDTH - 40, 10, 30, 30)
pause_button = pygame.Rect(WINDOW_WIDTH - 80, 10, 30, 30)

running = True
clock = pygame.time.Clock()

game_started = False

bg_music_on = True
def toggle_music():
    global bg_music_on
    bg_music_on = not bg_music_on
    if bg_music_on:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_paused = not game_paused  
                if game_paused:
                    pygame.mixer.music.pause()  
                else:
                    pygame.mixer.music.unpause()  
            if not game_started and not game_paused:
                game_started = True
            if event.key == pygame.K_UP and not game_over and not game_paused:
                bird_velocity = -JUMP_STRENGTH
            elif event.key == pygame.K_DOWN and not game_over and not game_paused:
                bird_velocity = JUMP_STRENGTH
            if event.key == pygame.K_RETURN and game_over:
                reset_game()  
            if event.key == pygame.K_m:
                toggle_music() 



    if game_paused:
        continue  

    
    if time.time() > next_toggle_time:
        toggle_day_night()
        next_toggle_time += DAY_NIGHT_INTERVAL 


    if not game_over and game_started:
        bird_velocity += GRAVITY
        bird_y += bird_velocity

       
        if bird_y > WINDOW_HEIGHT - GROUND_HEIGHT or bird_y < 0:
            game_over = True

        if len(pillars) == 0:
            pillars.extend(create_pillar())
        elif pillars[-1].left < WINDOW_WIDTH - PILLAR_SPACING:
            pillars.extend(create_pillar())

        
        pillars = [p.move(-PILLAR_SPEED, 0) for p in pillars]


        pillars = [p for p in pillars if p.right > 0]

        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_SIZE, BIRD_SIZE)
        for pillar in pillars:
            if bird_rect.colliderect(pillar):
                game_over = True

       
        if pillars and bird_x > pillars[0].right:
            score += 1
            if score > highest_score:
                highest_score = score  
            pillars.pop(0)

    background_x -= BACKGROUND_SCROLL_SPEED
    if background_x < -background_image.get_width():
        background_x = 0


    window.fill(DAY_COLOR if is_day else NIGHT_COLOR)


    window.blit(background_image, (background_x, 0))


    pygame.draw.rect(window, GREEN, (0, WINDOW_HEIGHT - GROUND_HEIGHT, WINDOW_WIDTH, GROUND_HEIGHT))

    window.blit(bird_image, (bird_x, bird_y))

    for pillar in pillars:
        pygame.draw.rect(window, GREEN, pillar)

    score_text = font.render(f"Score: {score}", True, BLACK)
    highest_score_text = font.render(f"Highest Score: {highest_score}", True, RED)
    window.blit(score_text, (10, 10))
    window.blit(highest_score_text, (10, 50))

    
    pygame.draw.rect(window, RED if bg_music_on else BLACK, music_button)
    pygame.draw.polygon(window, WHITE, [(WINDOW_WIDTH - 35, 20), (WINDOW_WIDTH - 15, 20), (WINDOW_WIDTH - 25, 35)])

    
    pygame.draw.rect(window, RED if game_paused else BLACK, pause_button)
    pygame.draw.rect(window, WHITE, (WINDOW_WIDTH - 75, 20, 10, 30))
    pygame.draw.rect(window, WHITE, (WINDOW_WIDTH - 60, 20, 10, 30))

    
    if game_over:
        retry_text = font.render("Press 'R or Press ENTER' to Retry", True, BLACK)
        window.blit(retry_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))

    pygame.display.flip()


    clock.tick(30)


    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and game_over:
        reset_game()


    if pillars and pillars[0].right < 0:
        pillars.pop(0)
pygame.quit()
sys.exit()
