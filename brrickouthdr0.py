import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Breakout - No PNG Edition with Sound")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

# Paddle details
paddle_width = 100
paddle_height = 10
paddle_x = (width - paddle_width) / 2
paddle_y = height - 40
paddle_speed = 10

# Ball details
ball_radius = 10
ball_x = width / 2
ball_y = height / 2
ball_dx = 5
ball_dy = -5

# Brick details
brick_width = 80
brick_height = 20
brick_rows = 5
brick_cols = 10
bricks = []

for r in range(brick_rows):
    for c in range(brick_cols):
        bricks.append(pygame.Rect(c * (brick_width + 5) + 50, r * (brick_height + 5) + 50, brick_width, brick_height))

# Sound effect generation (using NumPy for simplicity)
def create_sound(frequency, duration=100):
    sample_rate = 44100
    length = int(sample_rate * duration / 1000)  # Duration in milliseconds
    t = np.linspace(0, duration / 1000, length, False)
    wave = np.sin(2 * np.pi * frequency * t) * 32767  # Generate sine wave
    wave = wave.astype(np.int16)
    
    # Stack the wave to create a stereo sound (duplicate for left and right channels)
    stereo_wave = np.stack((wave, wave), axis=1)

    sound = pygame.sndarray.make_sound(stereo_wave)
    return sound

paddle_hit_sound = create_sound(440)  # A tone
brick_hit_sound = create_sound(880)  # A higher tone
wall_hit_sound = create_sound(220)  # A lower tone

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < width - paddle_width:
        paddle_x += paddle_speed

    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with walls
    if ball_x + ball_radius > width or ball_x - ball_radius < 0:
        ball_dx = -ball_dx
        wall_hit_sound.play()
    if ball_y - ball_radius < 0:
        ball_dy = -ball_dy
        wall_hit_sound.play()
    if ball_y + ball_radius > height:
        running = False  # Game over if ball hits bottom

    # Ball collision with paddle
    if paddle_x < ball_x < paddle_x + paddle_width and paddle_y < ball_y + ball_radius < paddle_y + paddle_height:
        ball_dy = -abs(ball_dy)
        paddle_hit_sound.play()

    # Ball collision with bricks
    for brick in bricks:
        if brick.collidepoint(ball_x, ball_y):
            bricks.remove(brick)
            ball_dy = -ball_dy
            brick_hit_sound.play()

    # Drawing
    screen.fill(black)
    
    # Draw paddle
    pygame.draw.rect(screen, blue, (paddle_x, paddle_y, paddle_width, paddle_height))
    
    # Draw ball
    pygame.draw.circle(screen, red, (int(ball_x), int(ball_y)), ball_radius)
    
    # Draw bricks
    for brick in bricks:
        pygame.draw.rect(screen, white, brick)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
