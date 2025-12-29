import pygame

from joybox.engine.input.actions import get_action_from_event, Action

class GameApp:
    def __init__(self, start_scene, window_size=(640, 480), caption="JoyBox", home_scene_factory=None):
        self.scene = start_scene
        self.running = True
        self.home_scene_factory = home_scene_factory

        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()

    def quit(self):
        self.running = False

    def set_scene(self, scene):
        self.scene = scene

    def go_home(self):
        if self.home_scene_factory:
            self.set_scene(self.home_scene_factory(self))

    def run(self, fps_cap=60):
        while self.running:
            delta_time = self.clock.tick(fps_cap) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    break

                action = get_action_from_event(event)
                if action == Action.HOME:
                    self.go_home()
                    continue
                
                next_scene = self.scene.handle_event(event)
                if next_scene is not None:
                    self.set_scene(next_scene)

            next_scene = self.scene.update(delta_time)

            if next_scene is not None:
                self.set_scene(next_scene)

            self.scene.render(self.screen)
            pygame.display.flip()