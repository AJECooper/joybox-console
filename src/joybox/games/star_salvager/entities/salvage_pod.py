import pygame

class SalvagePod:
    __slots__ = ("pos", "radius")

    def __init__(self, pos: pygame.Vector2, radius: int = 6):
        self.pos = pos
        self.radius = radius

    def render(self, surface):
        pygame.draw.circle(surface, (200, 200, 255), self.pos, self.radius)