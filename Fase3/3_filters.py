import argparse
import cv2
import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply live filters to webcam feed.")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {args.camera}")

    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
    print("Press q to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(frame, (7, 7), 0)
        sharpen = cv2.filter2D(frame, -1, sharpen_kernel)
        edges = cv2.Canny(gray, 100, 200)

        cv2.imshow("Original", frame)
        cv2.imshow("Blur", blur)
        cv2.imshow("Sharpen", sharpen)
        cv2.imshow("Edges", edges)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
