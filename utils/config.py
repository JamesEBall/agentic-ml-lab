"""YAML config management for the Agentic ML Research Lab."""

import os
import copy
import yaml


def load_config(path: str) -> dict:
    """Load a YAML config file.

    Args:
        path: Path to the YAML file.

    Returns:
        Dict of config values.
    """
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config or {}


def save_config(config: dict, path: str):
    """Save a config dict to a YAML file.

    Args:
        config: Dict of config values.
        path: Path to write to.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def merge_configs(base: dict, override: dict) -> dict:
    """Deep merge two config dicts. Override values take precedence.

    Args:
        base: Base config.
        override: Override config (values here win).

    Returns:
        Merged config (new dict, inputs unchanged).
    """
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def validate_config(config: dict, required_fields: list[str]) -> list[str]:
    """Validate that required fields exist in config.

    Supports dot notation for nested fields: "model.type", "training.epochs".

    Args:
        config: Config dict to validate.
        required_fields: List of required field paths (dot notation).

    Returns:
        List of missing field paths (empty if valid).
    """
    missing = []
    for field in required_fields:
        parts = field.split(".")
        current = config
        found = True
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                found = False
                break
        if not found:
            missing.append(field)
    return missing


def config_diff(config_a: dict, config_b: dict, prefix: str = "") -> list[str]:
    """Show differences between two configs.

    Returns list of human-readable diff strings.
    """
    diffs = []
    all_keys = set(list(config_a.keys()) + list(config_b.keys()))
    for key in sorted(all_keys):
        full_key = f"{prefix}.{key}" if prefix else key
        a_val = config_a.get(key)
        b_val = config_b.get(key)
        if isinstance(a_val, dict) and isinstance(b_val, dict):
            diffs.extend(config_diff(a_val, b_val, full_key))
        elif a_val != b_val:
            diffs.append(f"{full_key}: {a_val} → {b_val}")
    return diffs
