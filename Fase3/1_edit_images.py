import argparse
from pathlib import Path

import cv2


def main() -> None:
    parser = argparse.ArgumentParser(description="Basic image editing pipeline.")
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
    resized = cv2.resize(image, (800, 600), interpolation=cv2.INTER_AREA)
    flipped = cv2.flip(image, 1)

    cv2.imwrite(str(args.output_dir / "gray.jpg"), gray)
    cv2.imwrite(str(args.output_dir / "resized.jpg"), resized)
    cv2.imwrite(str(args.output_dir / "flipped.jpg"), flipped)
    print(f"Saved outputs to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
