from dataclasses import dataclass, field
from typing import Set

from joybox.engine.input.actions import Action

@dataclass
class InputState:
    actions: Set[Action] = field(default_factory=set)

    def press(self, action: Action) -> None:
        self.actions.add(action)

    def release(self, action: Action) -> None:
        self.actions.discard(action)

    def clear(self) -> None:
        self.actions.clear()