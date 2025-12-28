import pygame

from joybox.engine.scene import Scene
from joybox.engine.input.actions import get_action_from_event, Action

class TitleScene(Scene):
    def __init__(self, app):
        self.app = app
        self.font_title = pygame.font.SysFont("Arial", 28)
        self.font_hint = pygame.font.SysFont("Arial", 16)

    def handle_event(self, event):
        action = get_action_from_event(event)

        if action == Action.CONFIRM:
            from joybox.games.lantern_labyrinth.scenes.game_scene import GameScene
            
            return GameScene(self.app)

        if action == Action.BACK:
            self.app.quit()

        return None

    def update(self, delta_time):
        return None
    
    def render(self, surface):
        surface.fill((0, 0, 0))

        title = self.font_title.render("Lantern Labyrinth", True, (255, 255, 255))
        hint = self.font_hint.render("Press ENTER to start or ESC to quit", True, (200, 200, 200))

        surface.blit(title, title.get_rect(center=(640 / 2, 480 / 2 - 20)))
        surface.blit(hint, hint.get_rect(center=(640 / 2, 480 / 2 + 20)))

