import pygame

class GameApp:
    def __init__(self, start_scene, window_size=(640, 480), caption="JoyBox"):
        self.scene = start_scene
        self.running = True

        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()

    def quit(self):
        self.running = False

    def set_scene(self, scene):
        self.scene = scene

    def run(self, fps_cap=60):
        while self.running:
            delta_time = self.clock.tick(fps_cap) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    break

                next_scene = self.scene.handle_event(event)
                if next_scene is not None:
                    self.set_scene(next_scene)

            next_scene = self.scene.update(delta_time)

            if next_scene is not None:
                self.set_scene(next_scene)

            self.scene.render(self.screen)
            pygame.display.flip()