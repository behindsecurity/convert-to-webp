#!/usr/bin/env python3

import argparse
import os
from PIL import Image, ImageDraw, ImageFont

def add_image_watermark(image: Image.Image, watermark_path: str, transparency: int) -> Image.Image:
    """Apply an image watermark with adjustable transparency, centered."""
    watermark = Image.open(watermark_path)
    if watermark.mode != 'RGBA':
        watermark = watermark.convert("RGBA")

    base_w, base_h = image.size
    wm_w, wm_h = watermark.size

    if wm_w > base_w or wm_h > base_h:
        scale = min(base_w / wm_w, base_h / wm_h)
        watermark = watermark.resize((int(wm_w * scale), int(wm_h * scale)), Image.LANCZOS)
        wm_w, wm_h = watermark.size

    alpha = watermark.split()[3].point(lambda p: p * transparency / 255)
    watermark.putalpha(alpha)

    pos = ((base_w - wm_w) // 2, (base_h - wm_h) // 2)
    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    layer.paste(watermark, pos, watermark)
    return Image.alpha_composite(image.convert('RGBA'), layer).convert('RGB')


def add_text_watermark(
    image: Image.Image,
    text: str,
    font_path: str,
    font_size: int,
    font_color: str,
    transparency: int
) -> Image.Image:
    """Draw a text watermark with customizable font, color, size, and transparency, centered."""
    base = image.convert('RGBA')
    txt_layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)

    # load font (fallback to default if not found)
    try:
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
    except IOError:
        try:
            font = ImageFont.truetype("./fonts/dejavu-sans.bold.ttf", font_size)
        except IOError:
            # Fallback to the default bitmap font if TTF not found
            font = ImageFont.load_default()

    # parse color (hex "#rrggbb" or "r,g,b")
    if ',' in font_color:
        r, g, b = map(int, font_color.split(','))
    else:
        c = font_color.lstrip('#')
        r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)

    fill = (r, g, b, transparency)

    # measure text size: prefer textbbox, fallback to font.getsize
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except AttributeError:
        text_w, text_h = font.getsize(text)

    base_w, base_h = base.size
    pos = ((base_w - text_w) // 2, (base_h - text_h) // 2)

    draw.text(pos, text, font=font, fill=fill)
    return Image.alpha_composite(base, txt_layer).convert('RGB')


def convert_to_webp(base_image: Image.Image, filename: str, dims: tuple, quality: int, prefix: str):
    """Convert & resize to WebP, report per-file savings, and return sizes for overall summary."""
    orig_size = os.path.getsize(filename)
    base_image.thumbnail(dims)
    name = os.path.splitext(os.path.basename(filename))[0]
    out_path = f"./webp/{prefix}{name}.webp"
    base_image.save(out_path, format="webp", optimize=True, quality=quality, method=6)
    new_size = os.path.getsize(out_path)

    saved = orig_size - new_size
    saved_mb = saved / (1024 * 1024)
    pct = (saved / orig_size) * 100 if orig_size else 0

    print(f"Processed {filename} -> {out_path}")
    print(f" → Saved {saved} bytes ({saved_mb:.2f} MB), {pct:.1f}% smaller")

    return orig_size, new_size


def main():
    parser = argparse.ArgumentParser(
        description="Convert images to WebP, optionally watermarking with image and/or text, and report savings."
    )
    parser.add_argument('files', nargs='+', help="Input files (PNG, JPG, JPEG)")
    parser.add_argument('--quality', type=int, default=85, help="Output WebP quality (0-100)")
    parser.add_argument('--prefix',  type=str,   default='', help="Prefix for output filenames")
    parser.add_argument('--width',   type=int,   default=1024, help="Max width for resizing")
    parser.add_argument('--height',  type=int,   default=1024, help="Max height for resizing")

    # image watermark options
    parser.add_argument('--watermark',     type=str, help="Path to image watermark (PNG with transparency recommended)")
    parser.add_argument('--transparency',  type=int, default=100,
                        help="Image watermark transparency (0=transparent…255=opaque)")

    # text watermark options
    parser.add_argument('--text',           type=str, help="Text to use as watermark")
    parser.add_argument('--font-path',      type=str, help="Path to .ttf font file (default system font)")
    parser.add_argument('--font-size',      type=int, default=36, help="Font size for text watermark")
    parser.add_argument('--font-color',     type=str, default="#FFFFFF",
                        help="Font color as hex (#rrggbb) or 'r,g,b'")
    parser.add_argument('--text-transparency', type=int, default=100,
                        help="Text watermark transparency (0=transparent…255=opaque)")

    args = parser.parse_args()
    os.makedirs('./webp', exist_ok=True)

    total_orig = total_new = 0
    count = 0

    for filepath in args.files:
        if not filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Skipping {filepath}: unsupported format")
            continue

        img = Image.open(filepath)
        if args.watermark:
            img = add_image_watermark(img, args.watermark, args.transparency)
        if args.text:
            img = add_text_watermark(
                img,
                args.text,
                args.font_path,
                args.font_size,
                args.font_color,
                args.text_transparency
            )

        orig_size, new_size = convert_to_webp(
            img,
            filepath,
            (args.width, args.height),
            args.quality,
            args.prefix
        )

        total_orig += orig_size
        total_new  += new_size
        count += 1

    if count:
        total_saved = total_orig - total_new
        total_mb = total_saved / (1024 * 1024)
        total_pct = (total_saved / total_orig) * 100 if total_orig else 0
        print("\n=== Overall Savings ===")
        print(f"Processed {count} images")
        print(f"Total saved: {total_saved} bytes ({total_mb:.2f} MB), {total_pct:.1f}% smaller overall")
    else:
        print("No images processed.")

if __name__ == '__main__':
    main()
