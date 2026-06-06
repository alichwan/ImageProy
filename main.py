import datetime
from pathlib import Path

import cv2
import numpy as np

OUTPUT_DIR = Path("output")
WINDOW = "Live Feed"

_save_requested = False
_btn = {"x": 0, "y": 0, "w": 130, "h": 44}


def _noop(_: int) -> None:
    pass


def _on_mouse(event, x, y, flags, param) -> None:
    global _save_requested
    if event == cv2.EVENT_LBUTTONDOWN:
        bx, by, bw, bh = _btn["x"], _btn["y"], _btn["w"], _btn["h"]
        if bx <= x <= bx + bw and by <= y <= by + bh:
            _save_requested = True


def _apply(frame: np.ndarray, r: int, g: int, b: int, brightness: int) -> np.ndarray:
    # 128 = neutral (x1.0 gain, 0 brightness offset)
    offset = brightness - 128
    b_ch, g_ch, r_ch = cv2.split(frame)
    r_ch = cv2.convertScaleAbs(r_ch, alpha=r / 128.0, beta=offset)
    g_ch = cv2.convertScaleAbs(g_ch, alpha=g / 128.0, beta=offset)
    b_ch = cv2.convertScaleAbs(b_ch, alpha=b / 128.0, beta=offset)
    return cv2.merge([b_ch, g_ch, r_ch])


def _draw_button(frame: np.ndarray) -> np.ndarray:
    fh, fw = frame.shape[:2]
    margin = 12
    bx = fw - _btn["w"] - margin
    by = fh - _btn["h"] - margin
    _btn["x"], _btn["y"] = bx, by

    out = frame.copy()
    cv2.rectangle(out, (bx, by), (bx + _btn["w"], by + _btn["h"]), (34, 177, 76), -1)
    cv2.rectangle(out, (bx, by), (bx + _btn["w"], by + _btn["h"]), (255, 255, 255), 1)
    cv2.putText(
        out, "[ SAVE ]", (bx + 12, by + 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA,
    )
    return out


def main() -> None:
    global _save_requested

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open main camera (index 0).")

    cv2.namedWindow(WINDOW)
    cv2.createTrackbar("R Saturation", WINDOW, 128, 255, _noop)
    cv2.createTrackbar("G Saturation", WINDOW, 128, 255, _noop)
    cv2.createTrackbar("B Saturation", WINDOW, 128, 255, _noop)
    cv2.createTrackbar("Brightness  ", WINDOW, 128, 255, _noop)
    cv2.setMouseCallback(WINDOW, _on_mouse)

    print("128 = neutral for all sliders. Press q to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        r = cv2.getTrackbarPos("R Saturation", WINDOW)
        g = cv2.getTrackbarPos("G Saturation", WINDOW)
        b = cv2.getTrackbarPos("B Saturation", WINDOW)
        brightness = cv2.getTrackbarPos("Brightness  ", WINDOW)

        adjusted = _apply(frame, r, g, b, brightness)

        if _save_requested:
            _save_requested = False
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = OUTPUT_DIR / f"capture_{ts}.jpg"
            cv2.imwrite(str(path), adjusted)
            print(f"Saved: {path}")

        cv2.imshow(WINDOW, _draw_button(adjusted))

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
