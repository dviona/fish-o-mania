"""
    This is the Classic Mode for the game
"""
# Importing the different libraries and methods
import pygame, sys
from constants import *
from fish_manager import FishManager
from background import BackgroundManager

# Initialize pygame
pygame.init()

# Main parameters for the scene
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
screen.fill(SKY_BLUE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 36)

# DV - defining parameters for the boat
boat_image = pygame.image.load("graphics/boat.png")
boat_image = pygame.transform.scale(boat_image, (310, 260))

boat_x = SCREEN_WIDTH // 2 - boat_image.get_width() // 2 - 300
boat_y = WATER_SURFACE - boat_image.get_height() // 2 - 52
boat_speed = 8

#DV - defining parameters for the fishing hook
fishing_hook_img = pygame.image.load("graphics/fishing_hook.png")
fishing_hook_img = pygame.transform.scale(fishing_hook_img, (30, 30))
hook_rect = fishing_hook_img.get_rect()

#DV - defining parameters for fishing rod and casting
rod_length = 0
rod_max_length = SCREEN_HEIGHT - 300
is_casting = False
rod_speed = 6

"""
    This is the main game loop where all in-game features will be defined and called
"""
def main():
    # Initialize Pygame
    pygame.init()
    # 'running' boolean detects if game is running
    running = True
    pygame.display.set_caption("Fish-O-Mania: Classic Mode")

    # Call the function FishManager() and BackgroundManager() that allows to control fish behaviours
    fish_manager = FishManager()
    background_manager = BackgroundManager()

    # Spawn initial fishes
    for i in range(start_fishes):
        fish_manager.spawn_fish()

    # Defining the Scoreboard and Fish Net variables
    score = 0
    caught_fish = []

    #DV- defining global casting variables
    global boat_x, is_casting, rod_length

    # Main Game
    while running:
        # Event Handling Section - Monitor keypresses, mouse movements etc
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Monitor for any key-presses
            elif event.type == pygame.KEYDOWN:
                # exit if 'esc' button pressed
                if event.key == pygame.K_ESCAPE:
                    running = False
                # DV - logic for pressing space to cast
                if event.key == pygame.K_SPACE:
                    is_casting = True

            # Monitor for any mouse-presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Click on Fish to catch it
                fish = fish_manager.get_fish_at_position(event.pos)
                # Get fish info if fish was caught
                if fish:
                    info = fish.get_info()
                    score += info["value"]
                    caught_fish.append(info)
                    fish_manager.remove_fish(fish)
                    print(f"Caught: {info['type']} (+{info['value']} points)")

                    # Add ripple effect where fish was caught
                    background_manager.add_ripple(event.pos[0], event.pos[1])


        # Update the fish and background animations
        fish_manager.update()
        background_manager.update()

        #DV- move boat left/right with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            boat_x -= boat_speed
        if keys[pygame.K_RIGHT]:
            boat_x += boat_speed

        rod_x = boat_x + boat_image.get_width() - 83
        rod_top_y = boat_y + 175  # person’s hand area

        #DV Handle casting
        if is_casting:
            if rod_length < rod_max_length:
                rod_length += rod_speed
            else:
                is_casting = False
        else:
            # DVReel back up
            if rod_length > 0:
                fish = fish_manager.get_fish_at_position((hook_rect.centerx, hook_rect.bottom))
                if fish:
                    info = fish.get_info()
                    score += info["value"]
                    caught_fish.append(info)
                    fish_manager.remove_fish(fish)
                    is_casting = False  # optionally auto reel
                    #rod_length = 0  # snap back up
                    print(f"Caught by casting: {info['type']} (+{info['value']} points)")
                rod_length -= rod_speed

        # DvFinal hook position
        hook_x = rod_x
        hook_y = rod_top_y + rod_length

        #dv - # Define hook rect for clicking
        hook_rect.x = hook_x - fishing_hook_img.get_width() // 2
        hook_rect.y = hook_y

        # Sky Backdrops
        screen.fill(SKY_BLUE)
        pygame.draw.rect(screen, DEEP_BLUE,
                         (0, WATER_SURFACE, SCREEN_WIDTH, SCREEN_HEIGHT - WATER_SURFACE))
        pygame.draw.line(screen, WHITE, (0, WATER_SURFACE), (SCREEN_WIDTH, WATER_SURFACE), 2)

        # Water background with gradient effect
        for y in range(WATER_SURFACE, SCREEN_HEIGHT):
            # Create gradient from lighter to darker blue
            ratio = (y - WATER_SURFACE) / (SCREEN_HEIGHT - WATER_SURFACE)
            color = tuple(int(AZURE[i] + (DEEP_BLUE[i] - AZURE[i]) * ratio) for i in range(3))
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

        # Draw background elements (rocks, seaweed, bubbles, ripples)
        background_manager.draw(screen)

        #DV- put boat on top of the water line
        screen.blit(boat_image, (boat_x, boat_y))

        #DV - draw fishing line
        pygame.draw.line(screen, WHITE, (rod_x, rod_top_y), (hook_x, hook_y), 3)

        #DV - display fishing hook
        screen.blit(fishing_hook_img, hook_rect)

        # Fish
        fish_manager.draw(screen)

        # Get Fish Stats
        stats = fish_manager.get_stats()

        # Display Score
        score_text = big_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Fish count
        stats = fish_manager.get_stats()
        count_text = font.render(f"Fish in water: {stats['total']}", True, WHITE)
        screen.blit(count_text, (10, 50))

        # In Game Instructions
        instructions = [
            "Press SPACE to cast and catch fish!",
            "ESC: Quit"
        ]
        y_offset = 80
        for instruction in instructions:
            text = font.render(instruction, True, WHITE)
            screen.blit(text, (10, y_offset))
            y_offset += 25

        # Recent catches
        if caught_fish:
            recent_text = font.render("Recent Catches:", True, WHITE)
            screen.blit(recent_text, (SCREEN_WIDTH - 250, 10))
            for i, catch in enumerate(caught_fish[-5:]):
                catch_text = font.render(
                    f"{catch['type']} (+{catch['value']})",
                    True,
                    (255, 215, 0) if catch['rarity'] == 'rare' else WHITE
                )
                screen.blit(catch_text, (SCREEN_WIDTH - 250, 40 + i * 25))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()