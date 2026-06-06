import argparse
import cv2


def main() -> None:
    parser = argparse.ArgumentParser(description="Set camera resolution and FPS.")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    parser.add_argument("--width", type=int, default=1280, help="Target width")
    parser.add_argument("--height", type=int, default=720, help="Target height")
    parser.add_argument("--fps", type=float, default=30.0, help="Target FPS")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {args.camera}")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    cap.set(cv2.CAP_PROP_FPS, args.fps)

    actual_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Applied camera properties -> width={actual_w:.0f}, height={actual_h:.0f}, fps={actual_fps:.2f}")
    print("Press q to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        cv2.imshow("Camera with Properties", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
