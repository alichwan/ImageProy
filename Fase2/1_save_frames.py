import argparse
from pathlib import Path

import cv2


def main() -> None:
    parser = argparse.ArgumentParser(description="Save single frames from webcam.")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output_frames"),
        help="Directory to save captured frames",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {args.camera}")

    count = 0
    print("Press s to save frame, q to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        cv2.imshow("Capture Frames", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            out = args.output_dir / f"frame_{count:04d}.jpg"
            cv2.imwrite(str(out), frame)
            print(f"Saved {out}")
            count += 1
        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
