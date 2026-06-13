"""Configuration loading for the hand-tab controller.

The JSON config has two sections:

``mappings``  -- maps a gesture-type name (see :class:`gestures.GestureType`)
                 to an *action name* understood by :mod:`actions`.
``thresholds``-- tunable numeric parameters:

    swipe_velocity     Minimum horizontal palm velocity (normalized units per
                       frame) to count as a swipe. Lower = more sensitive.
    pinch_sensitivity  Minimum change in normalized thumb-index distance per
                       frame to register a PINCH / SPREAD.
    pinch_threshold    Normalized thumb-index distance below which the hand is
                       considered "pinched" (used for GRAB detection).
    smoothing_window   Number of recent frames used for velocity estimation.
    cooldown_ms        Debounce time (ms) between repeated firings of the same
                       action, so one swipe doesn't switch many tabs.
    move_speed         Pixels moved per drag step.
    resize_step        Fractional scale change per PINCH / SPREAD step.

No camera or MediaPipe imports here -- this module is pure and testable.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Dict

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "gestures.json")

DEFAULT_MAPPINGS: Dict[str, str] = {
    "SWIPE_LEFT": "prev_tab",
    "SWIPE_RIGHT": "next_tab",
    "PINCH": "resize_shrink",
    "SPREAD": "resize_grow",
    "POINT": "begin_move",
    "GRAB": "drag_move",
    "OPEN_PALM": "release",
    "TWO_HAND_PINCH": "resize_two_hand",
    "V_SIGN": "toggle_double_view",
}

DEFAULT_THRESHOLDS: Dict[str, float] = {
    "swipe_velocity": 0.04,
    "pinch_sensitivity": 0.05,
    "pinch_threshold": 0.4,
    "smoothing_window": 5,
    "cooldown_ms": 600,
    "move_speed": 40,
    "resize_step": 0.1,
}


@dataclass
class Config:
    """Resolved configuration with defaults applied."""

    mappings: Dict[str, str] = field(default_factory=lambda: dict(DEFAULT_MAPPINGS))
    thresholds: Dict[str, float] = field(
        default_factory=lambda: dict(DEFAULT_THRESHOLDS)
    )

    def action_for(self, gesture_type: str) -> str | None:
        """Return the action name mapped to a gesture type, or None."""
        return self.mappings.get(gesture_type)

    def threshold(self, name: str) -> float:
        """Return a threshold value, falling back to the default."""
        return float(self.thresholds.get(name, DEFAULT_THRESHOLDS[name]))


def load_config(path: str | None = None) -> Config:
    """Load configuration from JSON, merging over defaults.

    Missing file or missing keys fall back to the documented defaults.
    """
    path = path or DEFAULT_CONFIG_PATH
    mappings = dict(DEFAULT_MAPPINGS)
    thresholds = dict(DEFAULT_THRESHOLDS)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        mappings.update(data.get("mappings", {}))
        thresholds.update(data.get("thresholds", {}))
    return Config(mappings=mappings, thresholds=thresholds)


def write_default_config(path: str | None = None) -> str:
    """Write the default gestures.json to disk and return the path."""
    path = path or DEFAULT_CONFIG_PATH
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(
            {"mappings": DEFAULT_MAPPINGS, "thresholds": DEFAULT_THRESHOLDS},
            fh,
            indent=2,
        )
    return path


if __name__ == "__main__":
    written = write_default_config()
    print(f"Wrote default config to {written}")
