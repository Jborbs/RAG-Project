from __future__ import annotations

import json
import os
from typing import Iterable, List, Tuple


def ensure_dirs(*paths: str) -> None:
    for path in paths:
        os.makedirs(path, exist_ok=True)


def read_tsv_pairs(path: str) -> List[Tuple[str, str]]:
    rows: List[Tuple[str, str]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            left, right = line.rstrip("\n").split("\t", 1)
            rows.append((left, right))
    return rows


def write_json(obj: object, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
