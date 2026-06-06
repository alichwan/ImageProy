import argparse
import cv2


def detect_cameras(max_index: int) -> list[int]:
    available = []
    for idx in range(max_index + 1):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            ok, _ = cap.read()
            if ok:
                available.append(idx)
        cap.release()
    return available


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect available camera indices.")
    parser.add_argument("--max-index", type=int, default=10, help="Highest index to scan")
    args = parser.parse_args()

    cameras = detect_cameras(args.max_index)
    if cameras:
        print("Detected camera indices:", cameras)
    else:
        print("No cameras detected.")


if __name__ == "__main__":
    main()
