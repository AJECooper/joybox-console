from enum import Enum, auto
import pygame

class Action(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    CONFIRM = auto()
    BACK = auto()
    PAUSE = auto()
    RESTART = auto()
    HOME = auto()

DEFAULT_KEYMAP = {
    pygame.K_UP: Action.UP,
    pygame.K_DOWN: Action.DOWN,
    pygame.K_LEFT: Action.LEFT,
    pygame.K_RIGHT: Action.RIGHT,
    pygame.K_RETURN: Action.CONFIRM,
    pygame.K_ESCAPE: Action.BACK,
    pygame.K_p: Action.PAUSE,
    pygame.K_r: Action.RESTART,
    pygame.K_F1: Action.HOME,
}

def get_action_from_event(event, keymap=DEFAULT_KEYMAP):
    if event.type == pygame.KEYDOWN:
        return keymap.get(event.key)
    return None