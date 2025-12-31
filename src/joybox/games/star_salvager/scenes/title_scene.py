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
            from joybox.games.star_salvager.scenes.game_scene import GameScene
            
            return GameScene(self.app)
        
        if action == Action.BACK:
            from joybox.launcher.scenes.launcher_scene import LauncherScene

            return LauncherScene(self.app)

    def update(self, dt):
        return None
    
    def render(self, surface):
        surface.fill((0, 0, 0))

        w, h = surface.get_size()

        title = self.font_title.render("STAR SALVAGER", True, (255, 255, 255))
        subtitle = self.font_hint.render("Press CONFIRM to start", True, (200, 200, 200))
        back = self.font_hint.render("BACK: Launcher", True, (120, 120, 120))

        surface.blit(title, title.get_rect(center=(w // 2, h // 2 - 40)))
        surface.blit(subtitle, subtitle.get_rect(center=(w // 2, h // 2 + 20)))
        surface.blit(back, back.get_rect(center=(w // 2, h // 2 + 60)))