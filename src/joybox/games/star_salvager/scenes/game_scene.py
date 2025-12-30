import math
import random
import pygame

from joybox.engine.input.actions import get_action_from_event, Action
from joybox.engine.scene import Scene

from joybox.games.star_salvager.entities.salvage_pod import SalvagePod
from joybox.games.star_salvager.scenes.title_scene import TitleScene

class GameScene(Scene):
    def __init__(self, app):
        self.app = app
        self.rand = random.Random()

        self.pos = pygame.Vector2(160, 120)
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0.0

        self.rotation_speed = 180.0
        self.thrust = 120.0
        self.friction = 0.99

        self.score = 0
        self.salvage_pods = []
        self.max_pods = 6

        self.font_hint = pygame.font.SysFont("Arial", 24)

        for _ in range(self.max_pods):
            self.salvage_pods.append(self._spawn_salvage_pod())

    def _spawn_salvage_pod(self) -> SalvagePod:
        w, h = self.app.screen.get_size()

        margin = 20

        for _ in range(20):
            x = self.rand.randint(margin, w - margin)
            y = self.rand.randint(margin, h - margin)
            pos = pygame.Vector2(x, y)

            if pos.distance_to(self.pos) > 60:
                return SalvagePod(pos)
        
        return SalvagePod(pygame.Vector2(w // 2, h // 2))

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

        ship_radius = 10
        collected_pods = []

        for pod in self.salvage_pods:
            if self.pos.distance_to(pod.pos) <= (ship_radius + pod.radius):
                collected_pods.append(pod)

        if collected_pods:
            for pod in collected_pods:
                self.salvage_pods.remove(pod)
                self.score += 10

            while len(self.salvage_pods) < self.max_pods:
                self.salvage_pods.append(self._spawn_salvage_pod()) 

        return None
    
    def render(self, surface):
        surface.fill((5, 5, 15))

        for pod in self.salvage_pods:
            pod.render(surface)

        rad = math.radians(self.angle)
        forward = pygame.Vector2(math.cos(rad), math.sin(rad))
        right = forward.rotate(90)

        p1 = self.pos + forward * 12
        p2 = self.pos - forward * 8 + right * 6
        p3 = self.pos - forward * 8 - right * 6

        pygame.draw.polygon(surface, (255, 255, 255), [p1, p2, p3])

        score_text = self.font_hint.render(f"Score: {self.score}", True, (255, 255, 255))
        hint = self.font_hint.render("Collect pods (+10). UP thrust, LEFT/RIGHT rotate, BACK landing", True, (180, 180, 180))
        surface.blit(score_text, (10, 10))
        surface.blit(hint, (10, 32))