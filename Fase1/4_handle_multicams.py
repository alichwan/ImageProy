import argparse
import math

import cv2
import numpy as np


def detect_cameras(max_index: int = 10) -> list[int]:
    available = []
    for idx in range(max_index + 1):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            ok, _ = cap.read()
            if ok:
                available.append(idx)
        cap.release()
    print(f"Detected cameras: {available}")
    return available


def build_grid(frames: list[np.ndarray], cols: int) -> np.ndarray:
    rows = math.ceil(len(frames) / cols)
    h, w = frames[0].shape[:2]
    blank = np.zeros((h, w, 3), dtype=np.uint8)
    grid_rows = []
    for r in range(rows):
        row_frames = frames[r * cols : (r + 1) * cols]
        while len(row_frames) < cols:
            row_frames.append(blank)
        grid_rows.append(cv2.hconcat(row_frames))
    return cv2.vconcat(grid_rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Display all detected camera feeds in a dynamic grid."
    )
    parser.add_argument(
        "--cameras",
        type=int,
        nargs="+",
        default=None,
        help="Camera indices to use (auto-detect all if omitted)",
    )
    parser.add_argument(
        "--max-index",
        type=int,
        default=10,
        help="Highest camera index to scan when auto-detecting",
    )
    parser.add_argument(
        "--cell-size",
        type=int,
        nargs=2,
        metavar=("W", "H"),
        default=(640, 480),
        help="Width and height of each camera cell in the grid",
    )
    args = parser.parse_args()

    indices = args.cameras if args.cameras is not None else detect_cameras(args.max_index)
    if not indices:
        raise RuntimeError("No cameras found.")

    caps: list[tuple[int, cv2.VideoCapture]] = []
    for idx in indices:
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            caps.append((idx, cap))
        else:
            print(f"Warning: could not open camera {idx}, skipping.")
            cap.release()

    if not caps:
        raise RuntimeError("Could not open any cameras.")

    cell_w, cell_h = args.cell_size
    n = len(caps)
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    print(f"Displaying {n} camera(s) in a {rows}x{cols} grid. Press q to quit.")

    while True:
        frames: list[np.ndarray] = []
        all_ok = True
        for idx, cap in caps:
            ok, frame = cap.read()
            if not ok:
                all_ok = False
                break
            frame = cv2.resize(frame, (cell_w, cell_h))
            cv2.putText(
                frame,
                f"Cam {idx}",
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            frames.append(frame)

        if not all_ok:
            break

        cv2.imshow("Multi-camera Feed", build_grid(frames, cols))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    for _, cap in caps:
        cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
