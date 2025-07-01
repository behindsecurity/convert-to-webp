# convert-to-webp

A command-line tool to batch-convert images to WebP format with optional image and/or text watermarks.  
It automatically resizes, optimizes for quality, reports per-file and total byte/MB savings, and supports customization of fonts, colors, sizes and transparency.

---

## Features

- **Convert** JPEG/PNG to WebP with thumbnail resizing  
- **Optimize** output with adjustable quality (0–100) and `optimize`/`method=6` flags  
- **Image watermark**: supply a PNG (with alpha) and set transparency  
- **Text watermark**: customize text, TTF font, font size, font color, and transparency  
- **Reporting**: shows bytes and MB saved per file and overall, plus percent reduction  
- **Batch** processing: handle multiple files in one command  

---

## Requirements

- Python 3.6+  
- [Pillow](https://pypi.org/project/Pillow/)  

```bash
pip install --upgrade Pillow
````

---

## Installation

1. Clone this repository

```bash
git clone https://github.com/behindsecurity/convert-to-webp.git
cd convert-to-webp
```
2. Make the script executable (or invoke via `python3`)

```bash
chmod +x convert-to-webp.py
```

---

## Usage

```bash
./convert-to-webp.py [options] <file1> <file2> ... <fileN>
```

All converted files are written to the `./webp/` directory (created automatically).

### Common options

| Option | Type| Default| Description |
| --------------------- | ------ | --------- | ----------------------------------------------------------- |
| `--quality`  | int | 85  | WebP quality (0=lowest…100=highest) |
| `--prefix`| string | `''`| Prefix for output filenames|
| `--width` | int | 1024| Max width (px) for thumbnail  |
| `--height`| int | 1024| Max height (px) for thumbnail |
| `--watermark`| path| —| Path to image watermark (PNG with transparency recommended) |
| `--transparency`| int | 100 | Watermark image transparency (0=hidden…255=opaque) |
| `--text`  | string | —| Text to render as watermark|
| `--font-path`| path| —| Path to `.ttf` font file (falls back to default PIL font)|
| `--font-size`| int | 36  | Font size for text watermark  |
| `--font-color`  | string | `#FFFFFF` | Font color, either hex (`#rrggbb`) or `r,g,b`|
| `--text-transparency` | int | 100 | Text watermark transparency (0=hidden…255=opaque)  |

Run `./convert-to-webp.py --help` for full usage details.

---

## Examples

#### Basic conversion

```bash
./convert-to-webp.py photo1.jpg photo2.png
```

#### Set quality and resize dimensions

```bash
./convert-to-webp.py --quality 75 --width 800 --height 600 img/*.jpg
```

#### Add an image watermark

```bash
./convert-to-webp.py --watermark logo.png --transparency 128 pictures/*.png
```

#### Add a text watermark

```bash
./convert-to-webp.py \
  --text "© MyCompany" \
  --font-path /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf \
  --font-size 48 \
  --font-color "#FF0000" \
  --text-transparency 200 \
  assets/*.jpg
```

#### Combined image + text watermark with output prefix

```bash
./convert-to-webp.py \
  --prefix "webp_" \
  --watermark logo.png --transparency 80 \
  --text "behindsecurity.com" \
  --font-size 30 \
  --font-color 255,255,0 \
  --text-transparency 150 \
  photos/*
```

After running, you’ll see output like:

```
Processed photo1.jpg -> ./webp/webp_photo1.webp
 → Saved 1,024,512 bytes (0.98 MB), 45.3% smaller
Processed photo2.png -> ./webp/webp_photo2.webp
 → Saved786,432 bytes (0.75 MB), 38.1% smaller

=== Overall Savings ===
Processed 2 images
Total saved: 1,810,944 bytes (1.73 MB), 41.7% smaller overall
```

---

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to your branch (`git push origin feature-name`)
5. Open a Pull Request

---

## License

This project is licensed under the [MIT License](LICENSE).

