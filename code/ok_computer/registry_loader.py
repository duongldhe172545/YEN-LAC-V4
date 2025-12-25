from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
import yaml


def repo_root_from_here() -> Path:
    # repo_root/code/ok_computer/registry_loader.py -> repo_root
    return Path(__file__).resolve().parents[2]


def load_yaml(path: Path) -> Any:
    with path.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def load_alias(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    data = load_yaml(path) or {}
    if isinstance(data, dict) and 'aliases' in data and isinstance(data['aliases'], dict):
        data = data['aliases']
    if not isinstance(data, dict):
        return {}
    out: Dict[str, str] = {}
    for k, v in data.items():
        if isinstance(v, str):
            out[str(k)] = v
    return out


def load_registries(repo_root: Optional[Path] = None) -> Dict[str, Any]:
    root = repo_root or repo_root_from_here()
    reg = root / 'registry'
    return {
        'repo_root': str(root),
        'events': load_yaml(reg / 'events.yaml'),
        'metrics': pd.read_csv(reg / 'metrics.csv'),
        'metric_alias': load_alias(reg / 'metric_alias.yaml'),
        'gate_matrix': load_yaml(reg / 'gate_matrix.yaml'),
        'causal_edges': load_yaml(reg / 'causal_edges.yaml'),
        'runbook_actions': load_yaml(reg / 'runbook_actions.yaml'),
        'registry_lints': load_yaml(reg / 'registry_lints.yaml'),
        'thresholds': load_yaml(reg / 'thresholds.yaml'),
    }
