import pygame
import sys
import math

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
SLINGSHOT_LENGTH = 100
SLINGSHOT_WIDTH = 5
TARGET_RADIUS = 30
MAX_BIRD_COUNT = 5

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, bird_type):
        super().__init__()
        self.bird_type = bird_type
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, bird_type.color, (20, 20), 20)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = [0, 0]
        self.in_sling = True


    def update(self):
        if not self.in_sling:
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
            self.velocity[1] += GRAVITY

    def launch(self, angle, power):
        self.in_sling = False
        radians = math.radians(angle)
        self.velocity = [power * math.cos(radians), -power * math.sin(radians)]


# Target class
class Target(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TARGET_RADIUS * 2, TARGET_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (TARGET_RADIUS, TARGET_RADIUS), TARGET_RADIUS)
        self.rect = self.image.get_rect(center=(x, y))

# Slingshot class
class Slingshot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((SLINGSHOT_LENGTH, SLINGSHOT_WIDTH), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

# Bird types
class BirdType:
    def __init__(self, color, power_multiplier):
        self.color = color
        self.power_multiplier = power_multiplier

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angry Birds")
clock = pygame.time.Clock()

# Load sounds
pygame.mixer.init()

# Create bird, slingshot, and targets
bird_types = [
    BirdType((255, 0, 0), 1.0),    # Red bird
    BirdType((0, 255, 0), 1.5),    # Green bird
    BirdType((0, 0, 255), 2.0)     # Blue bird (more powerful)
]

bird_index = 0
bird = Bird(WIDTH // 8, HEIGHT * 3 // 4, bird_types[bird_index])
slingshot = Slingshot(WIDTH // 8, HEIGHT * 3 // 4)
targets = [Target(WIDTH * 3 // 4, HEIGHT // 2)]

all_sprites = pygame.sprite.Group()
all_sprites.add(bird, slingshot, *targets)

# Game loop
running = True
bird_launched = False
score = 0
level = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and bird.in_sling:
            bird_launched = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and bird.in_sling and bird_launched:
            mouse_x, mouse_y = event.pos
            angle = math.atan2(slingshot.rect.centery - mouse_y, mouse_x - slingshot.rect.centerx)
            power = min(math.hypot(mouse_x - slingshot.rect.centerx, slingshot.rect.centery - mouse_y), SLINGSHOT_LENGTH)
            bird.launch(math.degrees(angle), power * bird_types[bird_index].power_multiplier)

    # Update
    all_sprites.update()

    # Check for collisions
    if not bird.in_sling:
        collisions = pygame.sprite.spritecollide(bird, targets, True)
        if collisions:
            score += 100
            if len(targets) == 0:
                # Level complete condition (all targets hit)
                level += 1
                score += 500
                bird_index = (bird_index + 1) % len(bird_types)
                bird = Bird(WIDTH // 8, HEIGHT * 3 // 4, bird_types[bird_index])
                all_sprites.add(bird)

                bird_launched = False
                targets = [Target(WIDTH * 3 // 4, HEIGHT // 2)]
                all_sprites.add(*targets)

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display level and score
    font = pygame.font.Font(None, 36)
    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(level_text, (10, 10))
    screen.blit(score_text, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
