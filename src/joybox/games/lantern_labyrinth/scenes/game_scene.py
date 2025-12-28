import pygame

from joybox.engine.scene import Scene
from joybox.engine.input.actions import get_action_from_event, Action

class GameScene(Scene):
    TILE_SIZE = 16

    MAZE = [
        "####################",
        "#..#...............#",
        "#..#..######..###..#",
        "#......#..........##",
        "###.####..####..#..#",
        "#.............#.#..#",
        "#..######.###.#.#..#",
        "#...........#....E.#",
        "####################",
    ]

    def __init__(self, app):
        self.app = app
        self.font_hint = pygame.font.SysFont("Arial", 16)

        self.px, self.py = 1, 1

        self.offset_x = 20
        self.offset_y = 20

        self.fuel = 100.0
        self.fuel_consumption_rate_per_second = 8.0


    def is_wall(self, x, y):
        if y < 0 or y >= len(self.MAZE):
            return True
        if x < 0 or x >= len(self.MAZE[0]):
            return True
        return self.MAZE[y][x] == "#"
    
    def is_exit(self, x, y):
        return self.MAZE[y][x] == "E"

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

        if self.fuel <= 0:
            from joybox.games.lantern_labyrinth.scenes.game_over_scene import GameOverScene

            return GameOverScene(self.app)

        if self.is_exit(self.px, self.py):
            from joybox.games.lantern_labyrinth.scenes.win_scene import WinScene

            return WinScene(self.app)
        
        return None

    def render(self, surface):
        surface.fill((0, 0, 0))

        for y, row in enumerate(self.MAZE):
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

        bar_x, bar_y = 20, 220
        bar_w, bar_h = 200, 12

        pygame.draw.rect(surface, (200, 200, 200), (bar_x, bar_y, bar_w, bar_h), 1)

        fuel_ratio = max(0.0, min(1.0, self.fuel / 100.0))
        fill_w = int((bar_w - 2) * fuel_ratio)
        pygame.draw.rect(surface, (255, 240, 120), (bar_x + 1, bar_y + 1, fill_w, bar_h - 2))

        label = self.font_hint.render(f"Fuel: {int(self.fuel)}", True, (200, 200, 200))
        surface.blit(label, (bar_x + bar_w + 10, bar_y - 2))

        surface.blit(hint, (20, 200))
