"""Live entry point for the hand-tab controller.

Opens the webcam, runs MediaPipe Hands, converts landmarks to gesture events,
routes them through the action router onto the workspace, and renders with
OpenCV. Heavy dependencies (cv2, mediapipe) are import-guarded with a clear
install hint so running without them fails gracefully instead of crashing on
import.

Run:
    python main.py
Press 'q' to quit.
"""

from __future__ import annotations

import sys

from config import load_config
from gestures import GestureRecognizer, HandLandmarks
from actions import ActionRouter
from workspace import Workspace
import ui

_MISSING = []
try:
    import cv2
except Exception:
    cv2 = None
    _MISSING.append("opencv-python")
try:
    import mediapipe as mp
except Exception:
    mp = None
    _MISSING.append("mediapipe")


def _help_lines(config) -> list[str]:
    lines = ["Gesture mappings (q to quit):"]
    for gesture, action in config.mappings.items():
        lines.append(f"  {gesture:<16} -> {action}")
    return lines


def build_workspace() -> Workspace:
    ws = Workspace()
    for title in ("Editor", "Browser", "Terminal", "Docs"):
        ws.add_tab(title)
    ws.set_active(0)
    return ws


def run() -> int:
    """Run the live pipeline. Returns a process exit code."""
    if _MISSING:
        print(
            "Missing required packages: "
            + ", ".join(_MISSING)
            + "\nInstall them with:\n    pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 1

    config = load_config()
    workspace = build_workspace()
    router = ActionRouter(workspace, config)
    recognizer = GestureRecognizer(
        {
            "swipe_velocity": config.threshold("swipe_velocity"),
            "pinch_sensitivity": config.threshold("pinch_sensitivity"),
            "pinch_threshold": config.threshold("pinch_threshold"),
            "smoothing_window": int(config.threshold("smoothing_window")),
        }
    )
    help_lines = _help_lines(config)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(
            "Could not open webcam (VideoCapture(0)). Check camera permissions.",
            file=sys.stderr,
        )
        return 2

    hands_solution = mp.solutions.hands
    with hands_solution.Hands(
        max_num_hands=2,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.5,
    ) as hands:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            detected: list[HandLandmarks] = []
            points_for_overlay: list = []
            if result.multi_hand_landmarks:
                labels = result.multi_handedness or []
                for i, hand_lms in enumerate(result.multi_hand_landmarks):
                    label = "Right"
                    if i < len(labels):
                        label = labels[i].classification[0].label
                    hl = HandLandmarks.from_mediapipe(hand_lms, label=label)
                    detected.append(hl)
                    points_for_overlay.append(hl.points)

            events = recognizer.update(detected)
            router.handle_all(events)

            canvas = ui.render_workspace(workspace, help_lines + router.log[-4:])
            ui.draw_landmarks(frame, points_for_overlay)
            canvas = ui.overlay_camera(canvas, frame)
            if canvas is not None:
                cv2.imshow("Hand Tab Controller", canvas)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
