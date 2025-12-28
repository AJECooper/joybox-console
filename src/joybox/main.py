import pygame

from joybox.engine.game_app import GameApp
from joybox.engine.scene import Scene
from joybox.engine.input.actions import get_action_from_event, Action

class BootScene(Scene):
    def __init__(self, app):
        self.app = app
        self.font = pygame.font.SysFont(None, 32)

    def handle_event(self, event):
        action = get_action_from_event(event)

        if action == Action.BACK:
            self.app.quit()

    def render(self, surface):
        surface.fill((0, 0, 30))
        text = self.font.render("JoyBox Started!", True, (255, 255, 255))
        surface.blit(text, text.get_rect(center=(640 / 2, 480 / 2)))

def main():
    pygame.init()

    app = GameApp(start_scene=None, window_size=(640, 480), caption="JoyBox - Day 1")
    app.set_scene(BootScene(app))

    app.run(fps_cap=60)
    pygame.quit()

if __name__ == "__main__":
    main()
