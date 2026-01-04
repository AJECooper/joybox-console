import pygame

from joybox.engine.input.actions import get_action_from_event, Action
from joybox.engine.scene import Scene

class CharacterSelectScene(Scene):
    CLASSES = ["Warrior", "Mage", "Rogue"]

    def __init__(self, app):
        self.app = app

        self.font_title = pygame.font.Font(None, 26)
        self.font_body = pygame.font.Font(None, 18)

        self.selected_index = 0

        self.chosen_class = None

    def handle_event(self, event):
        action = get_action_from_event(event)

        if action == Action.UP:
            if self.chosen_class is None:
                self.selected_index = (self.selected_index - 1) % len(self.CLASSES)
            return None
        
        if action == Action.DOWN:
            if self.chosen_class is None:
                self.selected_index = (self.selected_index + 1) % len(self.CLASSES)
            return None
        
        if action == Action.CONFIRM:
            if self.chosen_class is None:
                self.chosen_class = self.CLASSES[self.selected_index]

                from joybox.games.tiny_kingdom_rpg.state import GameState
                from joybox.games.tiny_kingdom_rpg.scenes.overworld_scene import OverworldScene

                state = GameState(self.chosen_class)
                return OverworldScene(self.app, state)

            return None
        
        if action == Action.BACK:
            if self.chosen_class is not None:
                self.chosen_class = None
                return None
            
            from joybox.games.tiny_kingdom_rpg.scenes.title_scene import TitleScene
            return TitleScene(self.app)
        
        return None

    def update(self, dt):
        pass

    def render(self, surface):
        surface.fill((0, 0, 0))

        title = self.font_title.render("Choose Your Class", True, (255, 255, 255))
        surface.blit(title, (16, 16))

        y = 60
        for i, name in enumerate(self.CLASSES):
            is_selected = (i == self.selected_index) and (self.chosen_class is None)

            prefix = "> " if is_selected else "  "
            color = (255, 255, 255) if is_selected else (180, 180, 180)

            line = self.font_body.render(prefix + name, True, color)
            surface.blit(line, (16, y))
            y += 22

        y += 10
        if self.chosen_class is None:
            hint1 = self.font_body.render("UP/DOWN: Select   CONFIRM: Choose", True, (160, 160, 160))
            hint2 = self.font_body.render("BACK: Return", True, (160, 160, 160))
            surface.blit(hint1, (16, y))
            surface.blit(hint2, (16, y + 18))
        else:
            ok = self.font_body.render(f"Selected: {self.chosen_class}", True, (120, 255, 120))
            hint = self.font_body.render("BACK: Change selection", True, (160, 160, 160))
            surface.blit(ok, (16, y))
            surface.blit(hint, (16, y + 18))