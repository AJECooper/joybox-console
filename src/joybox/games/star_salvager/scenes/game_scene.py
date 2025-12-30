import pygame

from joybox.engine.input.actions import get_action_from_event, Action
from joybox.engine.scene import Scene

class GameScene(Scene):
    def __init__(self, app):
        self.app = app
        self.font_title = pygame.font.SysFont("Arial", 26)
        self.font_hint = pygame.font.SysFont("Arial", 14)

    def handle_event(self, event):
        action = get_action_from_event(event)

        if action == Action.BACK:
            from joybox.games.star_salvager.scenes.title_scene import TitleScene
            
            return TitleScene(self.app)

        return None

    def update(self, dt):
        return None
    
    def render(self, surface):
        surface.fill((5, 5, 15))

        w, h = surface.get_size()
        text1 = self.font_title.render("Gameplay soon...", True, (255, 255, 255))
        text2 = self.font_hint.render("BACK: Landing   RESTART: Restart", True, (180, 180, 180))

        surface.blit(text1, text1.get_rect(center=(w // 2, h // 2)))
        surface.blit(text2, text2.get_rect(center=(w // 2, h // 2 + 40)))