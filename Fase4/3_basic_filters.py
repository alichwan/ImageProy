import argparse
from pathlib import Path

import cv2
import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply blur, sharpen, and edge filters.")
    parser.add_argument("input", type=Path, help="Input image path")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Directory to store generated images",
    )
    args = parser.parse_args()

    image = cv2.imread(str(args.input))
    if image is None:
        raise RuntimeError(f"Could not read image: {args.input}")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
    sharpened = cv2.filter2D(image, -1, sharpen_kernel)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    cv2.imwrite(str(args.output_dir / "blurred.jpg"), blurred)
    cv2.imwrite(str(args.output_dir / "sharpened.jpg"), sharpened)
    cv2.imwrite(str(args.output_dir / "edges.jpg"), edges)

    print(f"Saved outputs to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
