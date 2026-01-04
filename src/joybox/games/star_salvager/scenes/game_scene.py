import math
import random
import pygame

from joybox.engine.input.actions import get_action_from_event, Action
from joybox.engine.scene import Scene

from joybox.games.star_salvager.entities.hazard import Hazard
from joybox.games.star_salvager.entities.salvage_pod import SalvagePod
from joybox.games.star_salvager.scenes.title_scene import TitleScene


class GameScene(Scene):
    def __init__(self, app):
        self.app = app
        self.rand = random.Random()

        # Ship state
        self.pos = pygame.Vector2(160, 120)
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0.0

        self.rotation_speed = 180.0
        self.thrust = 120.0
        self.friction = 0.99

        # Salvage / score
        self.score = 0
        self.salvage_pods = []
        self.max_pods = 6

        # Hazards
        self.hazards = []
        self.max_hazards = 6
        self.hazard_spawn_timer = 0.0
        self.hazard_spawn_interval = 6.0

        # Health / damage
        self.health = 3
        self.invuln_time = 0.0
        self.invuln_duration = 1.0

        # Game state
        self.is_game_over = False
        self.time_alive = 0.0

        self.font = pygame.font.SysFont("Arial", 24)

        # Initial spawns
        for _ in range(self.max_pods):
            self.salvage_pods.append(self._spawn_salvage_pod())

        self.hazards.append(self._spawn_hazard())

    # ---------- Spawning ----------

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

    def _spawn_hazard(self) -> Hazard:
        w, h = self.app.screen.get_size()

        pos = pygame.Vector2(w // 2, h // 2)
        for _ in range(30):
            pos = pygame.Vector2(self.rand.randint(0, w), self.rand.randint(0, h))
            if pos.distance_to(self.pos) > 100:
                break

        speed = self.rand.randint(20, 60)
        ang = self.rand.random() * (2 * math.pi)
        vel = pygame.Vector2(math.cos(ang), math.sin(ang)) * speed

        radius = self.rand.randint(10, 16)
        return Hazard(pos, vel, radius)

    # ---------- Input ----------

    def handle_event(self, event):
        action = get_action_from_event(event)
        
        if action == Action.BACK and event.type == pygame.KEYDOWN:
            return TitleScene(self.app)

        if event.type == pygame.KEYDOWN and self.is_game_over:
            if action in (Action.CONFIRM, Action.RESTART):
                return GameScene(self.app)

        if action == Action.RESTART and event.type == pygame.KEYDOWN:
            return GameScene(self.app)

        return None

    # ---------- Update ----------

    def update(self, dt):
        actions = self.app.input_state.actions

        if self.is_game_over:
            return None

        self.time_alive += dt

        if self.invuln_time > 0:
            self.invuln_time = max(0.0, self.invuln_time - dt)

        # Rotation (mutually exclusive)
        if Action.LEFT in actions and Action.RIGHT not in actions:
            self.angle -= self.rotation_speed * dt
        elif Action.RIGHT in actions and Action.LEFT not in actions:
            self.angle += self.rotation_speed * dt

        # Thrust
        if Action.UP in actions:
            rad = math.radians(self.angle)
            direction = pygame.Vector2(math.cos(rad), math.sin(rad))
            self.velocity += direction * self.thrust * dt

        # Move ship
        self.pos += self.velocity * dt
        self.velocity *= self.friction

        w, h = self.app.screen.get_size()
        self.pos.x = max(0, min(w, self.pos.x))
        self.pos.y = max(0, min(h, self.pos.y))

        # Difficulty ramp
        self.hazard_spawn_interval = max(2.5, 6.0 - (self.time_alive / 30.0))
        self.hazard_spawn_timer += dt

        if self.hazard_spawn_timer >= self.hazard_spawn_interval and len(self.hazards) < self.max_hazards:
            self.hazard_spawn_timer = 0.0
            self.hazards.append(self._spawn_hazard())

        # Update hazards
        bounds = pygame.Vector2(w, h)
        for hz in self.hazards:
            hz.update(dt, bounds)

        # Hazard collision
        ship_radius = 10

        if self.invuln_time <= 0.0:
            for hz in self.hazards:
                if self.pos.distance_to(hz.pos) <= (ship_radius + hz.radius):
                    self.health -= 1
                    self.invuln_time = self.invuln_duration

                    if self.health <= 0:
                        self.is_game_over = True
                    break

        # Salvage collection
        collected = []
        for pod in self.salvage_pods:
            if self.pos.distance_to(pod.pos) <= (ship_radius + pod.radius):
                collected.append(pod)

        if collected:
            for pod in collected:
                self.salvage_pods.remove(pod)
                self.score += 10

            while len(self.salvage_pods) < self.max_pods:
                self.salvage_pods.append(self._spawn_salvage_pod())

        return None

    # ---------- Render ----------

    def render(self, surface):
        surface.fill((5, 5, 15))

        for pod in self.salvage_pods:
            pod.render(surface)

        for hz in self.hazards:
            hz.render(surface)

        # Ship
        rad = math.radians(self.angle)
        forward = pygame.Vector2(math.cos(rad), math.sin(rad))
        right = forward.rotate(90)

        p1 = self.pos + forward * 12
        p2 = self.pos - forward * 8 + right * 6
        p3 = self.pos - forward * 8 - right * 6

        pygame.draw.polygon(surface, (255, 255, 255), [p1, p2, p3])

        # UI
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        health_text = self.font.render(f"Health: {self.health}", True, (255, 255, 255))
        hint = self.font.render(
            "UP thrust  LEFT/RIGHT rotate  BACK landing",
            True,
            (180, 180, 180),
        )

        surface.blit(score_text, (10, 10))
        surface.blit(health_text, (10, 34))
        surface.blit(hint, (10, 58))

        # Game over overlay
        if self.is_game_over:
            w, h = surface.get_size()
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            surface.blit(overlay, (0, 0))

            title = pygame.font.Font(None, 56).render("GAME OVER", True, (255, 255, 255))
            msg = self.font.render("CONFIRM: Restart   BACK: Landing", True, (220, 220, 220))

            surface.blit(title, title.get_rect(center=(w // 2, h // 2 - 10)))
            surface.blit(msg, msg.get_rect(center=(w // 2, h // 2 + 30)))
