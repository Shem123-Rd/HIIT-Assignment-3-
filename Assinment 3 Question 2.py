#Assignment 3
#Question 2
# By Md Abdullah Al Mamun S371482
# By Shem Ramudan S372783
# Zenith Sharma S371125
# Md Khasru S372473


import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Frame rate
clock = pygame.time.Clock()
FPS = 60

# Player class
class Player(pygame.sprite.Sprite):
    """Represents the player character in the game."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = 5
        self.jump_speed = -15
        self.gravity = 0.8
        self.dx = 0
        self.dy = 0
        self.on_ground = False
        self.health = 100
        self.lives = 3

    def update(self, *args, **kwargs ):
        """Update the player's position based on key presses."""
        keys = args[0]  # Assuming the first positional argument is always the keys
        self.dx = 0
        self.dy += self.gravity
        if keys[pygame.K_LEFT]:
            self.dx = -self.velocity
        if keys[pygame.K_RIGHT]:
            self.dx = self.velocity
        if keys[pygame.K_UP] and self.on_ground:
            self.dy = self.jump_speed
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.dy = 0
            self.on_ground = True
        else:
            self.on_ground = False

# Projectile class
class Projectile(pygame.sprite.Sprite):
    """Represents projectiles shot by the player."""
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 10
        self.direction = direction

    def update(self, *args, **kwargs):
        """Move the projectile; remove it if it goes off-screen."""
        angle = math.atan2(self.direction[1], self.direction[0])
        self.rect.x += self.velocity * math.cos(angle)
        self.rect.y += self.velocity * math.sin(angle)
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or \
           self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    """Represents enemies in the game."""
    def __init__(self, x, y, shape):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        if shape == 1:
            pygame.draw.circle(self.image, GREEN, (15, 15), 15)
        elif shape == 2:
            pygame.draw.rect(self.image, GREEN, (0, 0, 30, 30))
        elif shape == 3:
            pygame.draw.polygon(self.image, GREEN, [(0, 30), (15, 0), (30, 30)])
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = random.randint(1, 3)  # Randomize enemy speed
        self.attack_delay = random.randint(60, 120)  # Randomize attack delay
        self.last_attack = pygame.time.get_ticks()  # Track time of last attack

    def update(self, *args, **kwargs):
        """Move the enemy horizontally and initiate attacks."""
        self.rect.x += self.velocity
        now = pygame.time.get_ticks()
        if now - self.last_attack > self.attack_delay:
            self.attack(args[0])  # Pass player sprite group to attack function
            self.last_attack = now

    def attack(self, player_group):
        """Initiate an attack."""
        # Create and shoot a projectile towards the player
        player = player_group.sprites()[0]  # Get the first player sprite
        direction = (player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        magnitude = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        if magnitude != 0:
            direction = (direction[0] / magnitude, direction[1] / magnitude)
            projectile = Projectile(self.rect.centerx, self.rect.centery, direction)
            all_sprites.add(projectile)

# Boss class
class Boss(pygame.sprite.Sprite):
    """Represents the boss enemy in the game."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 3
        self.health = 100  # Boss starts with 100% health
        self.attack_delay = 90  # Set boss attack delay
        self.last_attack = pygame.time.get_ticks()  # Track time of last attack

    def update(self, *args, **kwargs):
        """Move the boss horizontally and initiate attacks."""
        self.rect.x += self.velocity
        now = pygame.time.get_ticks()
        if now - self.last_attack > self.attack_delay:
            self.attack(args[0])  # Pass player sprite group to attack function
            self.last_attack = now

    def attack(self, player_group):
        """Initiate an attack."""
        # Create and shoot a projectile towards the player
        player = player_group.sprites()[0]  # Get the first player sprite
        direction = (player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        magnitude = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        if magnitude != 0:
            direction = (direction[0] / magnitude, direction[1] / magnitude)
            projectile = Projectile(self.rect.centerx, self.rect.centery, direction)
            all_sprites.add(projectile)

def start_screen():
    """Display the start screen."""
    font = pygame.font.Font(None, 60)
    title_text = font.render("2D Game", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.fill(BLACK)
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def game_over_screen(score):
    """Display the game over screen."""
    font = pygame.font.Font(None, 60)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press SPACE to Restart", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.fill(BLACK)
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def main():
    start_screen()

    # Game setup
    all_sprites = pygame.sprite.Group()
    player = Player(400, 300)
    all_sprites.add(player)

    enemy_sprites = pygame.sprite.Group()

    score = 0  # Initialize score
    lives = 3  # Initialize lives
    level = 1  # Initialize level
    boss_spawned = False  # Boss spawn status

    # Game loop
    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create and shoot a projectile
                    direction = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP])
                    projectile = Projectile(player.rect.centerx, player.rect.centery, direction)
                    all_sprites.add(projectile)
                    score += 10  # Increment score when shooting

        # Update
        all_sprites.update(keys)
        enemy_sprites.update()  # Update enemy sprites

        # Check collisions between player's projectiles and enemies
        for projectile in pygame.sprite.groupcollide(all_sprites, enemy_sprites, True, True):
            score += 10  # Increase score when enemy killed

        # Check collisions between enemy projectiles and player
        for projectile in pygame.sprite.spritecollide(player, all_sprites, True):
            lives -= 1  # Decrease player lives when hit

        # Check if level completed
        if len(enemy_sprites) == 0 and not boss_spawned:
            level += 1
            if level <= 3:
                # Spawn enemies for the next level
                for _ in range(5 + level * 2):  # Increase enemy count with level
                    shape = random.randint(1, 3)  # Randomize enemy shape
                    enemy = Enemy(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 200), shape)
                    all_sprites.add(enemy)
                    enemy_sprites.add(enemy)
                # Display level warning
                print(f"Level {level} - Danger!")
            else:
                # Spawn boss for the final level
                boss = Boss(SCREEN_WIDTH // 2, 100)
                all_sprites.add(boss)
                enemy_sprites.add(boss)  # Add boss to enemy group
                boss_spawned = True
                # Display boss warning
                print("Boss Incoming - Danger!")

        # Render
        screen.fill(BLACK)
        all_sprites.draw(screen)
        enemy_sprites.draw(screen)  # Draw enemy sprites

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Display lives
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 50))

        # Check if lives are zero or boss defeated
        if lives <= 0 or (boss_spawned and boss.health <= 0):
            game_over_screen(score)
            main()  # Restart the game

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
