import argparse
import cv2


def main() -> None:
    parser = argparse.ArgumentParser(description="Show live video feed from a camera.")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {args.camera}")

    print("Press q to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        cv2.imshow("Live Video", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
