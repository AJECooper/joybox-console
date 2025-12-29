from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class GameManifest:
    id: str
    title: str
    version: str
    description: str
    entrypoint: str

    supported_profiles: List[str]
    pi_lite: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_dict(data: Dict[str, Any], *, source: str) -> "GameManifest":
        def require_str(key: str) -> str:
            value = data.get(key)

            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Manifest field '{key}' must be a non-empty string (source: {source})")
            return value.strip()
        
        def require_list_str(key: str) -> List[str]:
            value = data.get(key)

            if not isinstance(value, list) or not all(isinstance(x, str) and x.strip() for x in value):
                raise ValueError(f"Manifest field '{key}' must be a list of non-empty strings (source: {source})")
            return [x.strip() for x in value]
        
        manifest_id = require_str("id")
        title = require_str("title")
        version = require_str("version")
        description = require_str("description")
        entrypoint = require_str("entrypoint")

        supported_profiles = require_list_str("supported_profiles")

        pi_lite = data.get("pi_lite")
        if pi_lite is not None and not isinstance(pi_lite, dict):
            raise ValueError(f"Manifest field 'pi_lite' must be an object/dict if present (source: {source})")

        return GameManifest(
            id=manifest_id,
            title=title,
            version=version,
            description=description,
            entrypoint=entrypoint,
            supported_profiles=supported_profiles,
            pi_lite=pi_lite,
        )