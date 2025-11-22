"""
This file manages the background elements like ripples, seaweed, and rocks.
"""

import pygame
import random
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WATER_SURFACE, WATER_BOTTOM, LIGHT_PINK, DEEP_PINK, WHITE


class Ripple:
    """Animated water ripple effect."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 0
        self.max_radius = random.randint(30, 80)
        self.alpha = 255
        self.growth_rate = random.uniform(0.5, 1.0)
        self.fade_rate = 8
        self.alive = True

    def update(self):
        """Update ripple animation."""
        self.radius += self.growth_rate
        self.alpha -= self.fade_rate

        if self.alpha <= 0 or self.radius >= self.max_radius:
            self.alive = False

    def draw(self, surface):
        """Draw the ripple."""
        if self.alive and self.alpha > 0:
            # Create a temporary surface for transparency
            ripple_surf = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)

            # Draw concentric circles for ripple effect
            color = (255, 255, 255, max(0, int(self.alpha)))
            pygame.draw.circle(ripple_surf, color,
                             (self.max_radius, self.max_radius),
                             int(self.radius), 2)

            surface.blit(ripple_surf, (self.x - self.max_radius, self.y - self.max_radius))


class Seaweed:
    """Animated seaweed plant."""

    def __init__(self, x):
        self.x = x
        self.base_y = SCREEN_HEIGHT - 2
        self.height = random.randint(80, 150)
        self.segments = 8
        self.sway_offset = random.uniform(0, math.pi * 2)
        self.sway_speed = random.uniform(0.02, 0.05)
        self.sway_amount = random.randint(10, 20)
        self.color = (34, 139, 34)  # Forest green
        self.width = random.randint(8, 12)
        self.time = 0

    def update(self):
        """Update seaweed animation."""
        self.time += self.sway_speed

    def draw(self, surface):
        """Draw swaying seaweed."""
        segment_height = self.height / self.segments

        points = [(self.x, self.base_y)]

        for i in range(1, self.segments + 1):
            # Calculate sway based on height (more sway at the top)
            sway_factor = i / self.segments
            sway = math.sin(self.time + self.sway_offset + i * 0.3) * self.sway_amount * sway_factor

            x = self.x + sway
            y = self.base_y - (segment_height * i)
            points.append((x, y))

        # Draw the seaweed as a thick line with varying width
        if len(points) > 1:
            for i in range(len(points) - 1):
                width = max(2, self.width - i)
                pygame.draw.line(surface, self.color, points[i], points[i + 1], width)


class Rock:
    """Static rock decoration."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = random.randint(30, 80)
        self.height = random.randint(20, 50)
        self.color = random.choice([
            (105, 105, 105),  # Dim gray
            (119, 136, 153),  # Light slate gray
            (112, 128, 144),  # Slate gray
        ])
        self.highlight_color = tuple(min(c + 30, 255) for c in self.color)
        self.shadow_color = tuple(max(c - 30, 0) for c in self.color)

    def draw(self, surface):
        """Draw a rock with simple shading."""
        # Main rock body (ellipse)
        pygame.draw.ellipse(surface, self.color,
                          (self.x, self.y, self.width, self.height))

        # Highlight (top-left)
        highlight_rect = (self.x + 5, self.y + 5, self.width // 3, self.height // 3)
        pygame.draw.ellipse(surface, self.highlight_color, highlight_rect)

        # Shadow (bottom-right edge)
        pygame.draw.arc(surface, self.shadow_color,
                       (self.x, self.y, self.width, self.height),
                       math.pi, math.pi * 1.5, 3)


class Bubble:
    """Rising bubble effect."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(3, 8)
        self.speed = random.uniform(0.5, 1.5)
        self.wobble = random.uniform(-0.3, 0.3)
        self.wobble_offset = random.uniform(0, math.pi * 2)
        self.time = 0
        self.alive = True

    def update(self):
        """Update bubble movement."""
        self.y -= self.speed
        self.x += math.sin(self.time + self.wobble_offset) * self.wobble
        self.time += 0.1

        # Remove bubble if it reaches the surface
        if self.y < WATER_SURFACE:
            self.alive = False

    def draw(self, surface):
        """Draw bubble with shine effect."""
        if self.alive:
            # Main bubble
            pygame.draw.circle(surface, (173, 216, 230),
                             (int(self.x), int(self.y)), self.radius)

            # Shine highlight
            shine_x = int(self.x - self.radius // 3)
            shine_y = int(self.y - self.radius // 3)
            pygame.draw.circle(surface, WHITE,
                             (shine_x, shine_y), max(1, self.radius // 3))


class Wave:
    """Animated water surface wave."""

    def __init__(self):
        self.time = 0
        self.wave_speed = 0.05
        self.wave_amplitude = 8  # Height of waves
        self.wave_frequency = 0.02  # How many waves across screen
        self.y_position = WATER_SURFACE

        # Create multiple wave layers for depth
        self.layers = [
            {'speed': 0.05, 'amplitude': 8, 'frequency': 0.02, 'offset': 0},
            {'speed': 0.03, 'amplitude': 5, 'frequency': 0.015, 'offset': math.pi},
            {'speed': 0.02, 'amplitude': 8, 'frequency': 0.01, 'offset': 1.1 * math.pi / 2},
        ]

    def update(self):
        """Update wave animation."""
        self.time += self.wave_speed

    def get_wave_points(self, layer_index=0):
        """Generate points for the wave curve."""
        layer = self.layers[layer_index]
        points = []

        # Generate points across the screen width
        for x in range(0, SCREEN_WIDTH + 1, 5):  # Sample every 5 pixels
            y = self.y_position + math.sin(
                x * layer['frequency'] + self.time * layer['speed'] + layer['offset']
            ) * layer['amplitude']
            points.append((x, y))

        return points

    def draw(self, surface):
        """Draw the animated wave."""
        # Draw the main wave with a thick white line
        main_points = self.get_wave_points(0)
        if len(main_points) > 1:
            pygame.draw.lines(surface, WHITE, False, main_points, 3)

        # Draw a secondary, subtler wave for depth
        if len(self.layers) > 1:
            secondary_points = self.get_wave_points(1)
            if len(secondary_points) > 1:
                # Slightly transparent/lighter color
                pygame.draw.lines(surface, (200, 230, 255), False, secondary_points, 2)


class Sand:
    """Sandy ocean floor with texture."""

    def __init__(self):
        self.sand_y = WATER_BOTTOM
        self.sand_height = SCREEN_HEIGHT - WATER_BOTTOM

        # Sand colors - various shades of tan/beige
        self.base_color = (194, 178, 128)
        self.light_color = (210, 195, 145)
        self.dark_color = (150, 135, 90)

        # Generate random sand particles for texture
        self.particles = []
        self.generate_particles()
        # NEW: Added humps list to store wave patterns
        self.humps = []
        self.generate_humps()

        # NEW: This method creates 3-5 random sine waves
    def generate_humps(self):
        """Generate wavy sand humps/dunes for texture."""
        num_waves = random.randint(3, 5)
        for _ in range(num_waves):
            self.humps.append({
                'frequency': random.uniform(0.008, 0.02),  # Wave tightness
                'amplitude': random.randint(0, 5),  # Wave height
                'offset': random.uniform(0, math.pi * 2)  # Starting position
            })

    # NEW: Calculates the wavy surface height at any x position
    def get_sand_surface_y(self, x):
        """Calculate the y-position of sand surface at given x (with humps)."""
        y = WATER_BOTTOM
        # Add all the hump waves together for natural variation
        for hump in self.humps:
            y += math.sin(x * hump['frequency'] + hump['offset']) * hump['amplitude']
        return y

    def generate_particles(self):
        """Generate small particles to create sand texture."""
        num_particles = 200
        for _ in range(num_particles):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(WATER_BOTTOM, SCREEN_HEIGHT)
            size = random.randint(1, 3)
            # Random shade of sand color
            shade = random.choice([self.light_color, self.dark_color, self.base_color])
            self.particles.append({
                'x': x,
                'y': y,
                'size': size,
                'color': shade
            })

    def draw(self, surface):
        # 1. Generate wavy surface points
        sand_surface_points = []
        for x in range(0, SCREEN_WIDTH + 1, 5):
            y = self.get_sand_surface_y(x)  # Uses our hump calculation!
            sand_surface_points.append((x, y))

        # 2. Create polygon from wavy top to screen bottom
        polygon_points = sand_surface_points.copy()
        polygon_points.append((SCREEN_WIDTH, SCREEN_HEIGHT))
        polygon_points.append((0, SCREEN_HEIGHT))
        pygame.draw.polygon(surface, self.base_color, polygon_points)

        # 3. Add gradient shading on the humps
        for x in range(0, SCREEN_WIDTH, 5):
            y_start = self.get_sand_surface_y(x)
            for y_offset in range(0, SCREEN_HEIGHT - int(y_start), 3):
                y = y_start + y_offset
                if y < SCREEN_HEIGHT:
                    ratio = y_offset / (SCREEN_HEIGHT - y_start) if (SCREEN_HEIGHT - y_start) > 0 else 0
                    color = tuple(
                        int(self.base_color[i] + (self.dark_color[i] - self.base_color[i]) * ratio * 0.3) for i in
                        range(3))
                    pygame.draw.circle(surface, color, (x, int(y)), 2)

        # 4. Draw highlight and shadow lines on wavy surface
        shadow_points = [(p[0], p[1] + 3) for p in sand_surface_points]
        pygame.draw.lines(surface, self.dark_color, False, shadow_points, 2)
        pygame.draw.lines(surface, self.light_color, False, sand_surface_points, 2)

        # 5. Smart particle placement - only below sand surface!
        for particle in self.particles:
            sand_surface_y = self.get_sand_surface_y(particle['x'])
            if particle['y'] >= sand_surface_y:  # Only draw if below surface
                pygame.draw.circle(surface, particle['color'],
                                   (particle['x'], particle['y']),
                                   particle['size'])


class BackgroundManager:
    """Manages all background elements."""

    def __init__(self):
        self.ripples = []
        self.seaweeds = []
        self.rocks = []
        self.bubbles = []
        self.wave = Wave()  # Add wave animation
        self.sand = Sand()  # Add sand layer

        # Generate static elements
        self.generate_seaweed()
        self.generate_rocks()

        # Timers for dynamic elements
        self.ripple_timer = 0
        self.bubble_timer = 0

    def generate_seaweed(self):
        """Generate seaweed plants at the bottom."""
        num_seaweed = random.randint(8, 12)
        for _ in range(num_seaweed):
            x = random.randint(0, SCREEN_WIDTH)
            self.seaweeds.append(Seaweed(x))

    def generate_rocks(self):
        """Generate rocks at the bottom."""
        num_rocks = random.randint(5, 10)
        for i in range(num_rocks):
            x = random.randint(0, SCREEN_WIDTH - 80)
            y = WATER_BOTTOM - random.randint(0, 40)
            self.rocks.append(Rock(x, y))

    def add_ripple(self, x, y):
        """Add a ripple at a specific position."""
        self.ripples.append(Ripple(x, y))

    def update(self):
        """Update all background elements."""
        # Update wave
        self.wave.update()

        # Update ripples
        self.ripples = [r for r in self.ripples if r.alive]
        for ripple in self.ripples:
            ripple.update()

        # Random ripples on water surface
        self.ripple_timer += 1
        if self.ripple_timer > random.randint(30, 90):
            self.ripple_timer = 0
            x = random.randint(50, SCREEN_WIDTH - 50)
            self.add_ripple(x, WATER_SURFACE + 10)

        # Update seaweed
        for seaweed in self.seaweeds:
            seaweed.update()

        # Update bubbles
        self.bubbles = [b for b in self.bubbles if b.alive]
        for bubble in self.bubbles:
            bubble.update()

        # Random bubbles
        self.bubble_timer += 1
        if self.bubble_timer > random.randint(20, 60):
            self.bubble_timer = 0
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(WATER_SURFACE + 50, WATER_BOTTOM - 20)
            self.bubbles.append(Bubble(x, y))

    def draw(self, surface):
        """Draw all background elements in proper order."""
        # Draw sand first (bottom-most layer)
        self.sand.draw(surface)

        # Draw rocks on top of sand
        for rock in self.rocks:
            rock.draw(surface)

        # Draw seaweed
        for seaweed in self.seaweeds:
            seaweed.draw(surface)

        # Draw bubbles
        for bubble in self.bubbles:
            bubble.draw(surface)

        # Draw animated wave on water surface
        self.wave.draw(surface)

        # Draw ripples (top layer)
        for ripple in self.ripples:
            ripple.draw(surface)