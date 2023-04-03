import inspect

from typing import Any, Callable


def _filter_config(config: dict[str, Any], func: Callable) -> dict[str, Any]:
    sig = inspect.signature(func)
    filter_keys = [param.name for param in sig.parameters.values() if param.kind == param.POSITIONAL_OR_KEYWORD]
    filtered_config = {filter_key: config[filter_key] for filter_key in filter_keys if filter_key in config}

    return filtered_config
