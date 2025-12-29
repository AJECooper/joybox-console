"""
Game discovery for JoyBox.

In development, this typically scans src/joybox/games/.
On devices, this will later scan an installed games directory
(e.g. /opt/joybox/games or ~/joybox/games).

The discovery logic is intentionally filesystem-based so games
can be added via marketplace downloads or USB sideloading.
"""


from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from joybox.launcher.manifest import GameManifest


@dataclass(frozen=True)
class DiscoveredGame:
    manifest: GameManifest
    manifest_path: Path


def _games_root() -> Path:
    joybox_pkg_dir = Path(__file__).resolve().parents[1]
    return joybox_pkg_dir / "games"


def discover_games(*, root: Optional[Path] = None) -> List[DiscoveredGame]:
    games_dir = root if root is not None else _games_root()
    manifests = sorted(games_dir.glob("*/manifest.json"))

    discovered: List[DiscoveredGame] = []

    for manifest_path in manifests:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest = GameManifest.from_dict(data, source=str(manifest_path))
        discovered.append(DiscoveredGame(manifest=manifest, manifest_path=manifest_path))

    discovered.sort(key=lambda g: (g.manifest.title.lower(), g.manifest.id.lower()))
    return discovered
