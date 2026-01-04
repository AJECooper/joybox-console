import pygame

from joybox.engine.scene import Scene
from joybox.engine.input.actions import get_action_from_event, Action

class TitleScene(Scene):
    def __init__(self, app):
        self.app = app

        self.font_title = pygame.font.SysFont("Arial", 28)
        self.font_hint = pygame.font.SysFont("Arial", 16)

        self._blink_timer = 0.0
        self._show_press = True

    def handle_event(self, event):
        action = get_action_from_event(event)

        if action == Action.CONFIRM:
            from joybox.games.tiny_kingdom_rpg.scenes.character_select_scene import CharacterSelectScene
            
            return CharacterSelectScene(self.app)
        
        if action == Action.BACK:
            from joybox.launcher.scenes.launcher_scene import LauncherScene

            return LauncherScene(self.app)
        
    def update(self, dt):
        self._blink_timer += dt

        if self._blink_timer >= 0.5:
            self._blink_timer -= 0.5
            self._show_press = not self._show_press
        return None
    
    def render(self, surface):
        surface.fill((0, 0, 0))

        title = self.font_title.render("Tiny Kingdom RPG", True, (255, 255, 255))
        surface.blit(title, (16, 16))

        subtitle = self.font_hint.render("A JoyBox 16x16 RPG", True, (180, 180, 180))
        surface.blit(subtitle, (16, 44))

        if self._show_press:
            press = self.font_hint.render("Press CONFIRM to start", True, (255, 255, 255))
            surface.blit(press, (16, 90))

        hint = self.font_hint.render("BACK will be wired to launcher later", True, (160, 160, 160))
        surface.blit(hint, (16, 120))
