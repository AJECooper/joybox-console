import math
import pygame

from joybox.engine.input.actions import get_action_from_event, Action
from joybox.engine.scene import Scene

class GameScene(Scene):
    def __init__(self, app):
        self.app = app
        self.font_hint = pygame.font.SysFont("Arial", 24)

        self.pos = pygame.Vector2(160, 120)
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0.0

        self.rotation_speed = 180.0
        self.thrust = 120.0
        self.friction = 0.99

    def handle_event(self, event):
        action = get_action_from_event(event)

        if action == Action.BACK:
            from joybox.games.star_salvager.scenes.title_scene import TitleScene
            
            return TitleScene(self.app)

        return None

    def update(self, dt):
        actions = self.app.input_state.actions

        if Action.LEFT in actions:
            self.angle -= self.rotation_speed * dt
        if Action.RIGHT in actions:
            self.angle += self.rotation_speed * dt

        if Action.UP in actions:
            rad = math.radians(self.angle)
            direction = pygame.Vector2(math.cos(rad), math.sin(rad))
            self.velocity += direction * self.thrust * dt

        self.pos += self.velocity * dt
        self.velocity *= self.friction

        w, h = self.app.screen.get_size()
        self.pos.x = max(0, min(w, self.pos.x))
        self.pos.y = max(0, min(h, self.pos.y))

        return None
    
    def render(self, surface):
        surface.fill((5, 5, 15))

        rad = math.radians(self.angle)
        forward = pygame.Vector2(math.cos(rad), math.sin(rad))
        right = forward.rotate(90)

        p1 = self.pos + forward * 12
        p2 = self.pos - forward * 8 + right * 6
        p3 = self.pos - forward * 8 - right * 6

        pygame.draw.polygon(surface, (255, 255, 255), [p1, p2, p3])

        hint = self.font_hint.render("UP: Thrust  LEFT/RIGHT: Rotate  BACK: Landing", True, (180, 180, 180))
        surface.blit(hint, (10, 10))