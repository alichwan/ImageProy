import argparse
import cv2


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Show webcam frames in BGR, Grayscale, and HSV."
    )
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {args.camera}")

    print("Press q to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        cv2.imshow("BGR", frame)
        cv2.imshow("Grayscale", gray)
        cv2.imshow("HSV", hsv)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
