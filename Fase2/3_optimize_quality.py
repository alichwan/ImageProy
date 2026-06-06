import argparse
from pathlib import Path

import cv2


CODECS = {
    "XVID": "XVID",
    "MJPG": "MJPG",
    "MP4V": "mp4v",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Record video choosing codec and quality.")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    parser.add_argument("--codec", choices=sorted(CODECS.keys()), default="MJPG")
    parser.add_argument("--output", type=Path, default=Path("optimized.avi"), help="Output video")
    parser.add_argument("--fps", type=float, default=30.0, help="Output FPS")
    parser.add_argument("--width", type=int, default=1280, help="Output width")
    parser.add_argument("--height", type=int, default=720, help="Output height")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {args.camera}")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    cap.set(cv2.CAP_PROP_FPS, args.fps)

    fourcc = cv2.VideoWriter_fourcc(*CODECS[args.codec])
    out = cv2.VideoWriter(str(args.output), fourcc, args.fps, (args.width, args.height))
    if not out.isOpened():
        cap.release()
        raise RuntimeError(f"Could not open output file for writing: {args.output}")

    print(f"Recording with codec={args.codec}, fps={args.fps}, size={args.width}x{args.height}")
    print("Press q to stop recording.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.resize(frame, (args.width, args.height))
        out.write(frame)
        cv2.imshow("Optimized Recording", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Saved optimized video: {args.output.resolve()}")


if __name__ == "__main__":
    main()
