#!/usr/bin/env python3

import argparse
import os
from PIL import Image

def add_watermark(image: Image.Image, watermark_image_path: str, transparency: int) -> Image.Image:
    """Applies a resized watermark to the center of an image with adjustable transparency."""
    watermark = Image.open(watermark_image_path)
    base_width, base_height = image.size

    if watermark.mode != 'RGBA':
        watermark = watermark.convert("RGBA")

    w_w, w_h = watermark.size
    if w_w > base_width or w_h > base_height:
        scale = min(base_width / w_w, base_height / w_h)
        watermark = watermark.resize((int(w_w * scale), int(w_h * scale)), Image.LANCZOS)

    # adjust transparency
    alpha = watermark.split()[3].point(lambda p: p * transparency / 255)
    watermark.putalpha(alpha)

    # center position
    wm_w, wm_h = watermark.size
    position = ((base_width - wm_w) // 2, (base_height - wm_h) // 2)

    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    layer.paste(watermark, position, watermark)
    composite = Image.alpha_composite(image.convert('RGBA'), layer)
    return composite.convert('RGB')


def convert_to_webp(base_image: Image.Image, filename: str, dimensions: tuple, quality: int, prefix: str):
    """Converts/resizes to WebP, reports per-file savings, and returns sizes for overall tally."""
    # 1) original size
    orig_size = os.path.getsize(filename)

    # 2) resize & save
    base_image.thumbnail(dimensions)
    base_name = os.path.splitext(os.path.basename(filename))[0]
    out_path = f"./webp/{prefix}{base_name}.webp"
    base_image.save(out_path, format="webp", optimize=True, quality=quality, method=6)

    # 3) new size
    new_size = os.path.getsize(out_path)

    # 4) compute & print per-file savings
    saved = orig_size - new_size
    saved_mb = saved / (1024 * 1024)
    pct = (saved / orig_size) * 100 if orig_size > 0 else 0
    print(f"Processed {filename} -> {out_path}")
    print(f" → Saved {saved} bytes ({saved_mb:.2f} MB), {pct:.1f}% smaller")

    return out_path, orig_size, new_size


def main():
    parser = argparse.ArgumentParser(
        description='Convert images to WebP with optional watermarking, quality, prefix, and report total savings.'
    )
    parser.add_argument('files', nargs='+', help='Files to convert (PNG, JPG, JPEG)')
    parser.add_argument('--quality', type=int, default=85, help='Output WebP quality (0–100)')
    parser.add_argument('--prefix', type=str, default='', help='Filename prefix for output files')
    parser.add_argument('--width', type=int, default=1024, help='Max width to resize to')
    parser.add_argument('--height', type=int, default=1024, help='Max height to resize to')
    parser.add_argument('--watermark', type=str, help='Path to watermark image')
    parser.add_argument('--transparency', type=int, default=100, help='Watermark transparency (0–255)')
    args = parser.parse_args()

    os.makedirs('./webp', exist_ok=True)

    total_orig = 0
    total_new = 0
    processed_count = 0

    for file in args.files:
        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Skipping {file}: unsupported extension")
            continue

        img = Image.open(file)
        if args.watermark:
            img = add_watermark(img, args.watermark, args.transparency)

        _, orig_size, new_size = convert_to_webp(
            img,
            file,
            (args.width, args.height),
            args.quality,
            args.prefix
        )

        total_orig += orig_size
        total_new += new_size
        processed_count += 1

    if processed_count > 0:
        total_saved = total_orig - total_new
        total_saved_mb = total_saved / (1024 * 1024)
        total_pct = (total_saved / total_orig) * 100 if total_orig > 0 else 0
        print("\n=== Overall Savings ===")
        print(f"Processed {processed_count} images")
        print(f"Total saved: {total_saved} bytes ({total_saved_mb:.2f} MB), {total_pct:.1f}% reduction overall")
    else:
        print("No images were processed.")

if __name__ == '__main__':
    main()
