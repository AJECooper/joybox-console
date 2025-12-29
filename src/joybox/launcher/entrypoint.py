from __future__ import annotations

import importlib
from typing import Callable


def load_entrypoint(entrypoint: str) -> Callable:
    if not isinstance(entrypoint, str) or ":" not in entrypoint:
        raise ValueError(f"Invalid entrypoint '{entrypoint}'. Expected format 'module.path:function_name'")

    module_path, func_name = entrypoint.split(":", 1)
    module_path = module_path.strip()
    func_name = func_name.strip()

    if not module_path or not func_name:
        raise ValueError(f"Invalid entrypoint '{entrypoint}'. Expected format 'module.path:function_name'")

    module = importlib.import_module(module_path)
    fn = getattr(module, func_name)

    if not callable(fn):
        raise TypeError(f"Entrypoint '{entrypoint}' resolved to a non-callable: {fn!r}")

    return fn
