import argparse
from pathlib import Path

import cv2


def main() -> None:
    parser = argparse.ArgumentParser(description="Read a video and save an edited grayscale copy.")
    parser.add_argument("input", type=Path, help="Input video path")
    parser.add_argument("--output", type=Path, default=Path("edited_video.avi"), help="Output video")
    args = parser.parse_args()

    cap = cv2.VideoCapture(str(args.input))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open input video: {args.input}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(str(args.output), fourcc, fps, (width, height), isColor=False)
    if not out.isOpened():
        cap.release()
        raise RuntimeError(f"Could not open output video: {args.output}")

    print("Press q to stop preview.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(gray)
        cv2.imshow("Edited Video (Gray)", gray)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Saved edited video: {args.output.resolve()}")


if __name__ == "__main__":
    main()
