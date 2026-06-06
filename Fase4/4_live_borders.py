import argparse
import cv2


def _noop(_: int) -> None:
    pass


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Show live video edges (borders) using Canny detection."
    )
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    parser.add_argument(
        "--threshold1", type=int, default=100, help="First Canny threshold"
    )
    parser.add_argument(
        "--threshold2", type=int, default=200, help="Second Canny threshold"
    )
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {args.camera}")

    window_name = "Live Borders"
    cv2.namedWindow(window_name)
    cv2.createTrackbar("Lower", window_name, max(0, min(args.threshold1, 255)), 255, _noop)
    cv2.createTrackbar("Upper", window_name, max(0, min(args.threshold2, 255)), 255, _noop)

    print("Press q to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        lower = cv2.getTrackbarPos("Lower", window_name)
        upper = cv2.getTrackbarPos("Upper", window_name)
        if lower > upper:
            lower = upper
            cv2.setTrackbarPos("Lower", window_name, lower)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, lower, upper)
        cv2.imshow(window_name, edges)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
