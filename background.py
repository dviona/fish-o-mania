"""
Background Module for our game Fish-O-Mania.

This module manages all background visual elements including animated
water effects (waves, ripples, bubbles), decorative elements (seaweed,
rocks), and terrain (sand layers).

Classes:
    Ripple: Expanding circle animation on water surface.
    Seaweed: Moving underwater plant.
    Rock: Static decorative rock.
    Bubble: Rising bubble with wobble effect.
    Wave: Animated water surface wave.
    SandLayers: Tiled sand terrain at bottom.
    BackgroundManager: Coordinates all background elements.
"""

import pygame
import random
import math
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WATER_SURFACE,
    WATER_BOTTOM,
    WHITE
)


class Ripple:
    """
    Animated water ripple effect.

    Creates an expanding circular ripple that fades out over time,
    simulating disturbance on the water surface.

    Attributes:
        x (float): X-coordinate of ripple center.
        y (float): Y-coordinate of ripple center.
        radius (float): Current radius of the ripple.
        max_radius (int): Maximum radius before disappearing.
        alpha (int): Current transparency (255 = opaque, 0 = invisible).
        alive (bool): Whether the ripple should continue animating.
    """

    def __init__(self, x, y):
        """
        Initialize a ripple at the specified position.

        Args:
            x (float): X-coordinate for ripple center.
            y (float): Y-coordinate for ripple center.
        """
        self.x = x
        self.y = y
        self.radius = 0
        self.max_radius = random.randint(30, 80)
        self.alpha = 255
        self.growth_rate = random.uniform(0.5, 1.0)
        self.fade_rate = 8
        self.alive = True

    def update(self):
        """Update ripple animation (expand and fade)."""
        self.radius += self.growth_rate
        self.alpha -= self.fade_rate

        if self.alpha <= 0 or self.radius >= self.max_radius:
            self.alive = False

    def draw(self, surface):
        """
        Draw the ripple on the given surface.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        if not self.alive or self.alpha <= 0:
            return

        # Create transparent surface for ripple
        ripple_surf = pygame.Surface(
            (self.max_radius * 2, self.max_radius * 2),
            pygame.SRCALPHA
        )

        # Draw ripple circle
        color = (255, 255, 255, max(0, int(self.alpha)))
        pygame.draw.circle(
            ripple_surf,
            color,
            (self.max_radius, self.max_radius),
            int(self.radius),
            2  # Ring thickness
        )

        surface.blit(
            ripple_surf,
            (self.x - self.max_radius, self.y - self.max_radius)
        )


class Seaweed:
    """
    Animated swaying seaweed plant.

    Uses sine wave motion to simulate underwater plant movement,
    with more sway at the top than the base.

    Attributes:
        x (int): X-coordinate of seaweed base.
        base_y (int): Y-coordinate of seaweed base (screen bottom).
        height (int): Total height of the seaweed.
        segments (int): Number of segments for smooth curve.
    """

    def __init__(self, x):
        """
        Initialize seaweed at the specified X position.

        Args:
            x (int): X-coordinate for seaweed base.
        """
        self.x = x
        self.base_y = SCREEN_HEIGHT - 2
        self.height = random.randint(80, 150)
        self.segments = 8

        # Sway animation parameters
        self.sway_offset = random.uniform(0, math.pi * 2)
        self.sway_speed = random.uniform(0.02, 0.05)
        self.sway_amount = random.randint(10, 20)
        self.time = 0

        # Appearance
        self.color = (34, 139, 34)  # Forest green
        self.width = random.randint(8, 12)

    def update(self):
        """Update seaweed sway animation."""
        self.time += self.sway_speed

    def draw(self, surface):
        """
        Draw the swaying seaweed.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        segment_height = self.height / self.segments
        points = [(self.x, self.base_y)]

        # Calculate position of each segment
        for i in range(1, self.segments + 1):
            # Sway increases with height
            sway_factor = i / self.segments
            sway_angle = self.time + self.sway_offset + i * 0.3
            sway = math.sin(sway_angle) * self.sway_amount * sway_factor

            x = self.x + sway
            y = self.base_y - (segment_height * i)
            points.append((x, y))

        # Draw seaweed as connected line segments
        if len(points) > 1:
            for i in range(len(points) - 1):
                # Width decreases toward top
                width = max(2, self.width - i)
                pygame.draw.line(
                    surface,
                    self.color,
                    points[i],
                    points[i + 1],
                    width
                )


class Rock:
    """
    Static rock decoration.

    Draws an elliptical rock with simple shading for depth.

    Attributes:
        x (int): X-coordinate of rock.
        y (int): Y-coordinate of rock.
        width (int): Rock width in pixels.
        height (int): Rock height in pixels.
    """

    def __init__(self, x, y):
        """
        Initialize a rock at the specified position.

        Args:
            x (int): X-coordinate for rock.
            y (int): Y-coordinate for rock.
        """
        self.x = x
        self.y = y
        self.width = random.randint(30, 80)
        self.height = random.randint(20, 50)

        # Color with highlight and shadow variants
        self.color = random.choice([
            (105, 105, 105),  # Dim gray
            (119, 136, 153),  # Light slate gray
            (112, 128, 144),  # Slate gray
        ])
        self.highlight_color = tuple(min(c + 30, 255) for c in self.color)
        self.shadow_color = tuple(max(c - 30, 0) for c in self.color)

    def draw(self, surface):
        """
        Draw the rock with shading.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        # Main rock body
        pygame.draw.ellipse(
            surface,
            self.color,
            (self.x, self.y, self.width, self.height)
        )

        # Highlight (top-left area)
        highlight_rect = (
            self.x + 5,
            self.y + 5,
            self.width // 3,
            self.height // 3
        )
        pygame.draw.ellipse(surface, self.highlight_color, highlight_rect)

        # Shadow arc (bottom-right edge)
        pygame.draw.arc(
            surface,
            self.shadow_color,
            (self.x, self.y, self.width, self.height),
            math.pi,
            math.pi * 1.5,
            3
        )


class Bubble:
    """
    Rising bubble effect with horizontal wobble.

    Simulates air bubbles rising through water with slight
    side-to-side movement.

    Attributes:
        x (float): Current X-coordinate.
        y (float): Current Y-coordinate.
        radius (int): Bubble size in pixels.
        speed (float): Vertical rise speed.
        alive (bool): Whether bubble should continue animating.
    """

    def __init__(self, x, y):
        """
        Initialize a bubble at the specified position.

        Args:
            x (float): X-coordinate for bubble start.
            y (float): Y-coordinate for bubble start.
        """
        self.x = x
        self.y = y
        self.radius = random.randint(3, 8)
        self.speed = random.uniform(0.5, 1.5)

        # Wobble parameters
        self.wobble = random.uniform(-0.3, 0.3)
        self.wobble_offset = random.uniform(0, math.pi * 2)
        self.time = 0

        self.alive = True

    def update(self):
        """Update bubble position (rise and wobble)."""
        self.y -= self.speed
        self.x += math.sin(self.time + self.wobble_offset) * self.wobble
        self.time += 0.1

        # Remove bubble when it reaches the surface
        if self.y < WATER_SURFACE:
            self.alive = False

    def draw(self, surface):
        """
        Draw the bubble with shine effect.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        if not self.alive:
            return

        # Main bubble
        pygame.draw.circle(
            surface,
            (173, 216, 230),  # Light blue
            (int(self.x), int(self.y)),
            self.radius
        )

        # Shine highlight (upper-left)
        shine_x = int(self.x - self.radius // 3)
        shine_y = int(self.y - self.radius // 3)
        pygame.draw.circle(
            surface,
            WHITE,
            (shine_x, shine_y),
            max(1, self.radius // 3)
        )


class Wave:
    """
    Animated water surface wave.

    Uses multiple overlapping sine waves to create a natural-looking
    animated water surface.

    Attributes:
        time (float): Animation time counter.
        y_position (int): Y-coordinate of the wave line.
        layers (list): Configuration for multiple wave layers.
    """

    def __init__(self):
        """Initialize the wave with multiple layers."""
        self.time = 0
        self.wave_speed = 0.05
        self.y_position = WATER_SURFACE

        # Multiple wave layers for depth effect
        self.layers = [
            {
                'speed': 0.05,
                'amplitude': 8,
                'frequency': 0.02,
                'offset': 0
            },
            {
                'speed': 0.03,
                'amplitude': 5,
                'frequency': 0.015,
                'offset': math.pi
            },
            {
                'speed': 0.02,
                'amplitude': 8,
                'frequency': 0.01,
                'offset': 1.1 * math.pi / 2
            },
        ]

    def update(self):
        """Update wave animation."""
        self.time += self.wave_speed

    def get_wave_points(self, layer_index=0):
        """
        Generate points for a wave curve.

        Args:
            layer_index (int): Which wave layer to generate.

        Returns:
            list: List of (x, y) tuples forming the wave.
        """
        layer = self.layers[layer_index]
        points = []

        # Sample points across screen width
        for x in range(0, SCREEN_WIDTH + 1, 5):
            y = self.y_position + math.sin(
                x * layer['frequency'] +
                self.time * layer['speed'] +
                layer['offset']
            ) * layer['amplitude']
            points.append((x, y))

        return points

    def draw(self, surface):
        """
        Draw the animated waves.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        # Draw primary wave
        main_points = self.get_wave_points(0)
        if len(main_points) > 1:
            pygame.draw.lines(surface, WHITE, False, main_points, 3)

        # Draw secondary wave for depth
        if len(self.layers) > 1:
            secondary_points = self.get_wave_points(1)
            if len(secondary_points) > 1:
                pygame.draw.lines(
                    surface,
                    (200, 230, 255),  # Lighter blue
                    False,
                    secondary_points,
                    2
                )


class SandLayers:
    """
    Sand terrain layers at the bottom of the screen.

    Loads and tiles sand texture images horizontally across
    the screen bottom.

    Attributes:
        base_layers (list): Bottom sand layer images.
        top_layer (pygame.Surface): Top outline layer image.
    """

    def __init__(self, layer_files=None, use_terrain_files=False):
        """
        Initialize sand layers from image files.

        Args:
            layer_files (list): List of image file paths.
            use_terrain_files (bool): If True, auto-load terrain files.
        """
        self.base_layers = []
        self.top_layer = None

        if use_terrain_files and not layer_files:
            self._load_terrain_files()

    def _load_terrain_files(self):
        """Load the standard terrain sand files."""
        # Randomly choose a top variation
        top_variant = random.choice(
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        )

        # Base layer files (bottom to top)
        base_files = [
            "graphics/terrain_sand_d.png",
            "graphics/terrain_sand_c.png",
            "graphics/terrain_sand_b.png",
            "graphics/terrain_sand_a.png",
        ]

        # Load base layers
        for layer_file in base_files:
            try:
                layer_image = pygame.image.load(layer_file).convert_alpha()
                self.base_layers.append(layer_image)
                print(f"Loaded base sand layer: {layer_file}")
            except pygame.error as e:
                print(f"Error loading sand layer {layer_file}: {e}")

        # Load top outline layer
        top_outline_file = f"graphics/terrain_sand_top_{top_variant}_outline.png"
        try:
            self.top_layer = pygame.image.load(top_outline_file).convert_alpha()
            print(f"Loaded top sand layer: {top_outline_file}")
        except pygame.error as e:
            print(f"Error loading top sand layer: {e}")
            self.top_layer = None

    def draw(self, surface):
        """
        Draw the sand layers tiled across the screen.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        base_y = WATER_BOTTOM

        # Draw base layers (stacked vertically, tiled horizontally)
        for i, layer in enumerate(self.base_layers):
            if layer:
                tile_width = layer.get_width()
                num_tiles = (SCREEN_WIDTH // tile_width) + 2

                for tile_num in range(num_tiles):
                    x_pos = tile_num * tile_width
                    y_pos = base_y + (i * 10)
                    surface.blit(layer, (x_pos, y_pos))

        # Draw top outline layer
        if self.top_layer:
            tile_width = self.top_layer.get_width()
            num_tiles = (SCREEN_WIDTH // tile_width) + 2
            top_y = WATER_BOTTOM - 10

            for tile_num in range(num_tiles):
                x_pos = tile_num * tile_width
                surface.blit(self.top_layer, (x_pos, top_y))


class BackgroundManager:
    """
    Manages all background visual elements.

    Coordinates updating and drawing of all background elements
    in the proper z-order.

    Attributes:
        ripples (list): Active ripple animations.
        seaweeds (list): Seaweed decorations.
        rocks (list): Rock decorations.
        bubbles (list): Active bubble animations.
        wave (Wave): Water surface wave.
        sand (SandLayers): Sand terrain.
    """

    def __init__(self, sand_layer_files=None, use_terrain_files=False):
        """
        Initialize the background manager.

        Args:
            sand_layer_files (list): Custom sand layer image paths.
            use_terrain_files (bool): If True, load default terrain files.
        """
        self.ripples = []
        self.seaweeds = []
        self.rocks = []
        self.bubbles = []
        self.wave = Wave()
        self.sand = SandLayers(sand_layer_files, use_terrain_files)

        # Generate static decorations
        self._generate_seaweed()
        self._generate_rocks()

        # Timers for spawning dynamic elements
        self.ripple_timer = 0
        self.bubble_timer = 0

    def _generate_seaweed(self):
        """Generate seaweed plants at random positions."""
        num_seaweed = random.randint(8, 12)
        for _ in range(num_seaweed):
            x = random.randint(0, SCREEN_WIDTH)
            self.seaweeds.append(Seaweed(x))

    def _generate_rocks(self):
        """Generate rocks at random positions near the bottom."""
        num_rocks = random.randint(5, 10)
        for _ in range(num_rocks):
            x = random.randint(0, SCREEN_WIDTH - 80)
            y = WATER_BOTTOM - random.randint(0, 40)
            self.rocks.append(Rock(x, y))

    def add_ripple(self, x, y):
        """
        Add a ripple at a specific position.

        Args:
            x (float): X-coordinate for ripple.
            y (float): Y-coordinate for ripple.
        """
        self.ripples.append(Ripple(x, y))

    def update(self):
        """Update all background elements."""
        # Update wave animation
        self.wave.update()

        # Update and clean up ripples
        self.ripples = [r for r in self.ripples if r.alive]
        for ripple in self.ripples:
            ripple.update()

        # Spawn random surface ripples
        self.ripple_timer += 1
        if self.ripple_timer > random.randint(30, 90):
            self.ripple_timer = 0
            x = random.randint(50, SCREEN_WIDTH - 50)
            self.add_ripple(x, WATER_SURFACE + 10)

        # Update seaweed animation
        for seaweed in self.seaweeds:
            seaweed.update()

        # Update and clean up bubbles
        self.bubbles = [b for b in self.bubbles if b.alive]
        for bubble in self.bubbles:
            bubble.update()

        # Spawn random bubbles
        self.bubble_timer += 1
        if self.bubble_timer > random.randint(20, 60):
            self.bubble_timer = 0
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(WATER_SURFACE + 50, WATER_BOTTOM - 20)
            self.bubbles.append(Bubble(x, y))

    def draw(self, surface):
        """
        Draw all background elements in proper z-order.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        # Bottom layer: sand
        self.sand.draw(surface)

        # Rocks on top of sand
        for rock in self.rocks:
            rock.draw(surface)

        # Seaweed
        for seaweed in self.seaweeds:
            seaweed.draw(surface)

        # Bubbles
        for bubble in self.bubbles:
            bubble.draw(surface)

        # Water surface wave
        self.wave.draw(surface)

        # Top layer: ripples
        for ripple in self.ripples:
            ripple.draw(surface)

