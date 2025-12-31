import pygame


class Hazard:
    __slots__ = ("pos", "vel", "radius")

    def __init__(self, pos: pygame.Vector2, vel: pygame.Vector2, radius: int = 10):
        self.pos = pos
        self.vel = vel
        self.radius = radius

    def update(self, dt: float, bounds: pygame.Vector2):
        self.pos += self.vel * dt

        if self.pos.x < 0:
            self.pos.x += bounds.x
        elif self.pos.x > bounds.x:
            self.pos.x -= bounds.x

        if self.pos.y < 0:
            self.pos.y += bounds.y
        elif self.pos.y > bounds.y:
            self.pos.y -= bounds.y

    def render(self, surface):
        pygame.draw.circle(surface, (160, 160, 160), self.pos, self.radius)
