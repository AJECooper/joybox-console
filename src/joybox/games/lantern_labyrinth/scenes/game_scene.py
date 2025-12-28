import pygame

from joybox.engine.scene import Scene
from joybox.engine.input.actions import get_action_from_event, Action
from joybox.games.lantern_labyrinth.maze import generate_maze, place_exit, place_orbs

class GameScene(Scene):
    TILE_SIZE = 16
    WINDOW_W, WINDOW_H = 640, 480
    HUD_HEIGHT = 60

    def __init__(self, app, level=1):
        self.app = app
        self.level = level

        self.font_hint = pygame.font.SysFont("Arial", 16)

        self.grid = generate_maze(21, 13, seed=None)
        place_orbs(self.grid, count=3 + (self.level // 2))
        self.exit_pos = place_exit(self.grid)

        self.dark_overlay = pygame.Surface((640, 480))
        self.dark_overlay.fill((0, 0, 0))

        self.px, self.py = 1, 1

        self.offset_x = 20
        self.offset_y = 20

        self.fuel = 100.0
        self.fuel_consumption_rate_per_second = 8.0


    def is_wall(self, x, y):
        if y < 0 or y >= len(self.grid):
            return True
        if x < 0 or x >= len(self.grid[0]):
            return True
        
        return self.grid[y][x] == "#"
    
    def is_exit(self, x, y):
        return self.grid[y][x] == "E"
    
    def is_orb(self, x, y):
        return self.grid[y][x] == "O"

    def collect_orb(self, x, y):
        self.grid[y][x] = "."
        self.fuel = min(100.0, self.fuel + 30.0)

    def try_move(self, dx, dy):
        nx = self.px + dx
        ny = self.py + dy

        if not self.is_wall(nx, ny):
            self.px, self.py = nx, ny

    def handle_event(self, event):
        action = get_action_from_event(event)

        if action == Action.BACK:
            from joybox.games.lantern_labyrinth.scenes.title_scene import TitleScene
            return TitleScene(self.app)

        if action == Action.UP:
            self.try_move(0, -1)
        elif action == Action.DOWN:
            self.try_move(0, 1)
        elif action == Action.LEFT:
            self.try_move(-1, 0)
        elif action == Action.RIGHT:
            self.try_move(1, 0)

        return None

    def update(self, dt):
        self.fuel -= self.fuel_consumption_rate_per_second * dt

        if self.is_orb(self.px, self.py):
            self.collect_orb(self.px, self.py)

        if self.fuel <= 0:
            from joybox.games.lantern_labyrinth.scenes.game_over_scene import GameOverScene

            return GameOverScene(self.app)

        if self.is_exit(self.px, self.py):
            from joybox.games.lantern_labyrinth.scenes.win_scene import WinScene

            return WinScene(self.app)
        
        return None

    def render(self, surface):
        surface.fill((0, 0, 0))

        for y, row in enumerate(self.grid):
            for x, ch in enumerate(row):
                rect = pygame.Rect(
                    self.offset_x + x * self.TILE_SIZE,
                    self.offset_y + y * self.TILE_SIZE,
                    self.TILE_SIZE,
                    self.TILE_SIZE
                )

                if ch == "#":
                    pygame.draw.rect(surface, (40, 40, 40), rect)
                elif ch == "E":
                    pygame.draw.rect(surface, (80, 200, 120), rect)
                elif ch == "O":
                    pygame.draw.rect(surface, (255, 240, 120), rect.inflate(-8, -8))
                else:
                    pygame.draw.rect(surface, (12, 12, 12), rect)

        player_rect = pygame.Rect(
            self.offset_x + self.px * self.TILE_SIZE,
            self.offset_y + self.py * self.TILE_SIZE,
            self.TILE_SIZE,
            self.TILE_SIZE
        )
        pygame.draw.rect(surface, (255, 240, 120), player_rect)

        hint = self.font_hint.render("Arrows: Move   ESC: Back", True, (200, 200, 200))

        bar_x = 20
        bar_y = self.WINDOW_H - 30
        bar_w, bar_h = 200, 12

        pygame.draw.rect(surface, (200, 200, 200), (bar_x, bar_y, bar_w, bar_h), 1)

        fuel_ratio = max(0.0, min(1.0, self.fuel / 100.0))
        fill_w = int((bar_w - 2) * fuel_ratio)
        pygame.draw.rect(surface, (255, 240, 120), (bar_x + 1, bar_y + 1, fill_w, bar_h - 2))

        label = self.font_hint.render(f"Fuel: {int(self.fuel)}", True, (200, 200, 200))
        surface.blit(label, (bar_x + bar_w + 10, bar_y - 2))

        fuel_ratio = max(0.0, min(1.0, self.fuel / 100.0))

        max_dark = 220
        min_dark = 0
        alpha = int(min_dark + (1.0 - fuel_ratio) * (max_dark - min_dark))

        if alpha > 0:
            self.dark_overlay.set_alpha(alpha)
            surface.blit(self.dark_overlay, (0, 0))

        surface.blit(hint, (20, 200))
