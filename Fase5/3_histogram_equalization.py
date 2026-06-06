import argparse
from pathlib import Path

import cv2


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply grayscale histogram equalization and color normalization."
    )
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

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_gray = cv2.equalizeHist(gray)
    normalized_color = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)

    cv2.imwrite(str(args.output_dir / "gray.jpg"), gray)
    cv2.imwrite(str(args.output_dir / "equalized_gray.jpg"), equalized_gray)
    cv2.imwrite(str(args.output_dir / "normalized_color.jpg"), normalized_color)

    print(f"Saved outputs to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
