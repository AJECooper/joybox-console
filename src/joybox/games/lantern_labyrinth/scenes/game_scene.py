import pygame

from joybox.engine.scene import Scene
from joybox.engine.input.actions import get_action_from_event, Action

class GameScene(Scene):
    def __init__(self, app):
        self.app = app
        self.font_title = pygame.font.SysFont("Arial", 24)
        self.font_hint = pygame.font.SysFont("Arial", 16)

    def handle_event(self, event):
        action = get_action_from_event(event)

        if action == Action.BACK:
            from joybox.games.lantern_labyrinth.scenes.title_scene import TitleScene

            return TitleScene(self.app)
        
        return None
    
    def update(self, delta_time):
        return None
    
    def render(self, surface):
        surface.fill((10, 10, 10))

        title = self.font_title.render("Game Scene (placeholder)", True, (255, 255, 255))
        hint = self.font_hint.render("ESC: Back to Title", True, (200, 200, 200))

        surface.blit(title, (20, 30))
        surface.blit(hint, (20, 70))