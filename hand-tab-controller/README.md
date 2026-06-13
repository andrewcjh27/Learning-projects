# Hand Tab Controller

A webcam-based hand-motion gesture controller for a tab/panel workspace. Wave,
pinch, point, and grab to switch, move, resize, and split tabs — all mappings
are customizable through a JSON config.

It uses [MediaPipe Hands](https://developers.google.com/mediapipe) for hand
tracking and OpenCV for the camera feed and workspace rendering. The gesture
math and workspace logic are kept in pure, dependency-light modules so they can
be unit-tested without a camera.

## Install

```bash
pip install -r requirements.txt
```

Requires Python 3.10+. `mediapipe` and `opencv-python` are only needed to run
the live app; the logic modules and tests do not import them.

## Run

```bash
python main.py
```

Press `q` to quit. The window shows the workspace with tabs plus a mirrored
camera thumbnail (top-right) with hand-landmark dots, and an on-screen list of
the active gesture mappings.

## Gestures

| Gesture           | Type             | Default action       | What it does                                  |
|-------------------|------------------|----------------------|-----------------------------------------------|
| Open-hand swipe ← | `SWIPE_LEFT`     | `prev_tab`           | Switch to the previous tab                    |
| Open-hand swipe → | `SWIPE_RIGHT`    | `next_tab`           | Switch to the next tab                        |
| Pinch in          | `PINCH`          | `resize_shrink`      | Shrink the active tab                         |
| Pinch out (spread)| `SPREAD`         | `resize_grow`        | Grow the active tab                           |
| Point (index)     | `POINT`          | `begin_move`         | Start dragging the active tab                 |
| Grab / fist       | `GRAB`           | `drag_move`          | Drag the active tab to follow the hand        |
| Open palm         | `OPEN_PALM`      | `release`            | Release a drag                                |
| Two-hand pinch    | `TWO_HAND_PINCH` | `resize_two_hand`    | Resize using the distance between both palms  |
| V / peace sign    | `V_SIGN`         | `toggle_double_view` | Toggle the split (double-tab) view            |

### Split / double view

Hold up a **V / peace sign** (index + middle finger) to toggle the split
(double-tab) view, which lays the active and next tab side by side. This is
bound by default; you can move it to any other gesture by editing the
`toggle_double_view` mapping in `gestures.json`, e.g.:

```json
"mappings": { "OPEN_PALM": "toggle_double_view" }
```

## Customizing gestures (`gestures.json`)

`gestures.json` has two sections:

- **`mappings`** — gesture type → action name. Available actions: `next_tab`,
  `prev_tab`, `resize_grow`, `resize_shrink`, `resize_two_hand`, `begin_move`,
  `drag_move`, `release`, `toggle_double_view`.
- **`thresholds`** — tunable numbers:

| Field              | Meaning                                                            |
|--------------------|-------------------------------------------------------------------|
| `swipe_velocity`   | Min horizontal palm velocity (norm. units/frame) for a swipe      |
| `pinch_sensitivity`| Min per-frame change in thumb-index distance for PINCH/SPREAD     |
| `pinch_threshold`  | Thumb-index distance below which a hand counts as pinched (GRAB)   |
| `smoothing_window` | Frames used for velocity estimation                               |
| `cooldown_ms`      | Debounce between repeated firings of a discrete action            |
| `move_speed`       | Pixels moved per drag step                                        |
| `resize_step`      | Fractional size change per PINCH/SPREAD                           |

Regenerate the default config any time with:

```bash
python config.py
```

## Tests

Pure-logic tests run without a camera or MediaPipe:

```bash
python -m pytest -q
```

## Troubleshooting

- **Camera won't open / `VideoCapture(0)` fails**: grant camera permission to
  your terminal/IDE (macOS: System Settings → Privacy & Security → Camera;
  Linux: ensure your user can access `/dev/video0`). Close other apps using the
  camera, or try a different index (`VideoCapture(1)`).
- **`Missing required packages`**: run `pip install -r requirements.txt`.
- **`mediapipe` won't install**: it ships wheels only for certain
  Python/OS combinations; check the supported versions and use a matching
  Python (3.10–3.12 generally work).
