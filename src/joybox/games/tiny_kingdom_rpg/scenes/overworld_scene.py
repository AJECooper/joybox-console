import pygame
import random

from joybox.engine.scene import Scene
from joybox.engine.input.actions import get_action_from_event, Action

class OverworldScene(Scene):
    TILE_SIZE = 16
    CHUNK_SIZE = 32
    MAX_CACHED_CHUNKS = 64

    GRASS = 0
    WATER = 1
    SAND = 2
    STONE = 3

    def __init__(self, app, state):
        self.app = app
        self.state = state

        self.font = pygame.font.SysFont("Arial", 16)

        self.world_seed = 12345

        self._chunks = {}

        self._tile_surfaces = {
            self.GRASS: self._create_tile_surface((34, 139, 34)),
            self.WATER: self._create_tile_surface((30, 144, 255)),
            self.SAND: self._create_tile_surface((194, 178, 128)),
            self.STONE: self._create_tile_surface((128, 128, 128)),
        }
        
        self._player_surface = self._create_tile_surface((220, 40, 40))

    def _create_tile_surface(self, colour):
        surface = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
        surface.fill(colour)

        return surface
    
    def _chunk_coords(self, tile_x, tile_y):
        chunk_x = tile_x // self.CHUNK_SIZE
        chunk_y = tile_y // self.CHUNK_SIZE

        return (chunk_x, chunk_y)
    
    def _ensure_chunks(self, chunk_x, chunk_y):
        key = (chunk_x, chunk_y)

        if key in self._chunks:
            return
        
        seed = (self.world_seed * 73856093) ^ (chunk_x * 19349663) ^ (chunk_y * 83492791)
        rnd = random.Random(seed)

        chunk_data = []
        for y in range(self.CHUNK_SIZE):
            row = []
            for x in range(self.CHUNK_SIZE):
                r = rnd.random()

                if r < 0.08:
                    tile_type = self.WATER
                elif r < 0.14:
                    tile_type = self.SAND
                elif r < 0.18:
                    tile_type = self.STONE
                else:
                    tile_type = self.GRASS

                row.append(tile_type)
            chunk_data.append(row)

        self._chunks[key] = chunk_data

        if len(self._chunks) > self.MAX_CACHED_CHUNKS:
            self.__evict_far_chunks()

    def __evict_far_chunks(self):
        pcx, pcy = self._chunk_coords(self.state.player_x, self.state.player_y)

        keys = list(self._chunks.keys())
        keys.sort(key=lambda k: (k[0] - pcx) * (k[0] - pcx) + (k[1] - pcy) * (k[1] - pcy), reverse=True)

        remove_count = max(1, len(self._chunks) - self.MAX_CACHED_CHUNKS)
        for i in range(remove_count):
            del self._chunks[keys[i]]

    def _get_tile(self, tx, ty):
        cx, cy = self._chunk_coords(tx, ty)
        self._ensure_chunks(cx, cy)

        lx = tx % self.CHUNK_SIZE
        ly = ty % self.CHUNK_SIZE
        return self._chunks[(cx, cy)][ly][lx]
    
    def handle_event(self, event):
        action = get_action_from_event(event)

        if action == Action.PAUSE:
            return None

        if action == Action.BACK:
            return None

        dx, dy = 0, 0
        if action == Action.UP:
            dy = -1
        elif action == Action.DOWN:
            dy = 1
        elif action == Action.LEFT:
            dx = -1
        elif action == Action.RIGHT:
            dx = 1

        if dx != 0 or dy != 0:
            self.state.player_x += dx
            self.state.player_y += dy

        return None
    
    def update(self, dt):
        return None
    
    def render(self, surface):
        surface.fill((0, 0, 0))

        w, h = surface.get_size()

        player_px = self.state.player_x * self.TILE_SIZE
        player_py = self.state.player_y * self.TILE_SIZE

        cam_left = player_px - (w // 2)
        cam_top = player_py - (h // 2)

        left_tx = cam_left // self.TILE_SIZE
        top_ty = cam_top // self.TILE_SIZE

        tiles_x = (w // self.TILE_SIZE) + 2
        tiles_y = (h // self.TILE_SIZE) + 2

        for y in range(tiles_y):
            ty = top_ty + y
            py = (ty * self.TILE_SIZE) - cam_top

            for x in range(tiles_x):
                tx = left_tx + x
                px = (tx * self.TILE_SIZE) - cam_left

                terrain = self._get_tile(tx, ty)
                surface.blit(self._tile_surfaces[terrain], (px, py))

        player_screen_x = (player_px - cam_left)
        player_screen_y = (player_py - cam_top)
        surface.blit(self._player_surface, (player_screen_x, player_screen_y))

        hud = self.font.render(
            f"{self.state.chosen_class}  Pos: ({self.state.player_x},{self.state.player_y})  Chunks: {len(self._chunks)}",
            True,
            (255, 255, 255),
        )
        surface.blit(hud, (8, 8))