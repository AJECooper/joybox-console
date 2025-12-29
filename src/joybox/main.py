import pygame

from joybox.engine.game_app import GameApp
from joybox.launcher.scenes.launcher_scene import LauncherScene


def main():
    pygame.init()

    app = GameApp(start_scene=None, window_size=(640, 480), caption="JoyBox - Day 1")

    app.set_scene(LauncherScene(app))

    app.run(fps_cap=60)
    pygame.quit()


if __name__ == "__main__":
    main()