import argparse
from pathlib import Path

import cv2


def main() -> None:
    parser = argparse.ArgumentParser(description="Enhance brightness and contrast.")
    parser.add_argument("input", type=Path, help="Input image path")
    parser.add_argument("--alpha", type=float, default=1.2, help="Contrast multiplier")
    parser.add_argument("--beta", type=int, default=30, help="Brightness offset")
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

    adjusted = cv2.convertScaleAbs(image, alpha=args.alpha, beta=args.beta)
    cv2.imwrite(str(args.output_dir / "brightness_contrast.jpg"), adjusted)

    print(f"Saved outputs to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
