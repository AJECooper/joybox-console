from __future__ import annotations

import pygame

from joybox.engine.scene import Scene
from joybox.engine.input.actions import get_action_from_event, Action
from joybox.launcher.discovery import discover_games
from joybox.launcher.entrypoint import load_entrypoint

class LauncherScene(Scene):
    def __init__(self, app):
        self.app = app
        self.games = discover_games()
        self.selected_index = 0

        self.font_title = pygame.font.SysFont(None, 48)
        self.font_item = pygame.font.SysFont(None, 28)
        self.font_meta = pygame.font.SysFont(None, 22)

        self.error_message = None

    def handle_event(self, event):
        action = get_action_from_event(event)

        if action == Action.UP and self.games:
            self.selected_index = (self.selected_index - 1) % len(self.games)

        elif action == Action.DOWN and self.games:
            self.selected_index = (self.selected_index + 1) % len(self.games)

        elif action == Action.CONFIRM:
            self.error_message = None

            if not self.games:
                self.error_message = "No games discovered."
                return None

            selected = self.games[self.selected_index].manifest

            try:
                create_game_fn = load_entrypoint(selected.entrypoint)
                next_scene = create_game_fn(self.app)

                if next_scene is None:
                    raise ValueError(f"Entrypoint returned None for game '{selected.id}'")

                return next_scene

            except Exception as ex:
                self.error_message = f"Failed to launch '{selected.title}': {ex}"
                return None

        elif action == Action.BACK:
            self.app.quit()

        return None

    def update(self, dt):
        return None

    def render(self, surface):
        surface.fill((10, 10, 14))

        title_surf = self.font_title.render("JoyBox", True, (240, 240, 240))
        surface.blit(title_surf, (24, 18))

        subtitle_surf = self.font_meta.render("Select a game", True, (180, 180, 180))
        surface.blit(subtitle_surf, (26, 62))

        if self.error_message:
            err = self.font_meta.render(self.error_message, True, (255, 120, 120))
            surface.blit(err, (24, surface.get_height() - 55))

        if not self.games:
            empty_surf = self.font_item.render("No games found.", True, (220, 220, 220))
            surface.blit(empty_surf, (24, 120))
            hint = self.font_meta.render(
                "Add a game manifest under joybox/games/<id>/manifest.json",
                True,
                (160, 160, 160),
            )
            surface.blit(hint, (24, 150))
            return

        start_y = 110
        line_h = 34
        max_visible = (surface.get_height() - start_y - 50) // line_h
        max_visible = max(1, max_visible)

        top = 0
        if self.selected_index >= max_visible:
            top = self.selected_index - max_visible + 1

        visible = self.games[top : top + max_visible]

        for i, g in enumerate(visible):
            actual_index = top + i
            m = g.manifest
            y = start_y + i * line_h

            is_selected = (actual_index == self.selected_index)
            if is_selected:
                pygame.draw.rect(
                    surface,
                    (40, 40, 60),
                    pygame.Rect(18, y - 4, surface.get_width() - 36, line_h),
                )

            text_surf = self.font_item.render(
                m.title,
                True,
                (255, 255, 255) if is_selected else (210, 210, 210),
            )
            surface.blit(text_surf, (28, y))

            ver_surf = self.font_meta.render(f"v{m.version}", True, (160, 160, 160))
            surface.blit(ver_surf, (surface.get_width() - 90, y + 4))

        footer = "UP/DOWN: select    CONFIRM: choose    BACK: quit"
        footer_surf = self.font_meta.render(footer, True, (160, 160, 160))
        surface.blit(footer_surf, (24, surface.get_height() - 30))
