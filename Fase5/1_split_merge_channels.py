import argparse
from pathlib import Path

import cv2


def main() -> None:
    parser = argparse.ArgumentParser(description="Split and merge BGR channels.")
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

    b, g, r = cv2.split(image)
    merged_bgr = cv2.merge([b, g, r])
    merged_rgb_order = cv2.merge([r, g, b])
    merged_gbr_order = cv2.merge([g, b, r])

    cv2.imwrite(str(args.output_dir / "channel_b.png"), b)
    cv2.imwrite(str(args.output_dir / "channel_g.png"), g)
    cv2.imwrite(str(args.output_dir / "channel_r.png"), r)
    cv2.imwrite(str(args.output_dir / "merged_bgr.jpg"), merged_bgr)
    cv2.imwrite(str(args.output_dir / "merged_rgb_order.jpg"), merged_rgb_order)
    cv2.imwrite(str(args.output_dir / "merged_gbr_order.jpg"), merged_gbr_order)

    print(f"Saved outputs to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
