import argparse
from pathlib import Path

import cv2


def main() -> None:
    parser = argparse.ArgumentParser(description="Resize, crop, and rotate an image.")
    parser.add_argument("input", type=Path, help="Input image path")
    parser.add_argument("--width", type=int, default=640, help="Resize width")
    parser.add_argument("--height", type=int, default=480, help="Resize height")
    parser.add_argument("--angle", type=float, default=30.0, help="Rotation angle in degrees")
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

    resized = cv2.resize(image, (args.width, args.height), interpolation=cv2.INTER_AREA)

    h, w = resized.shape[:2]
    crop = resized[h // 4 : (3 * h) // 4, w // 4 : (3 * w) // 4]

    center = (w // 2, h // 2)
    rot_mat = cv2.getRotationMatrix2D(center, args.angle, 1.0)
    rotated = cv2.warpAffine(resized, rot_mat, (w, h))

    cv2.imwrite(str(args.output_dir / "resized.jpg"), resized)
    cv2.imwrite(str(args.output_dir / "cropped.jpg"), crop)
    cv2.imwrite(str(args.output_dir / "rotated.jpg"), rotated)

    print(f"Saved outputs to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
