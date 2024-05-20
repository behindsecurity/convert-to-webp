# Image Watermarking and WEBP Conversion Tool

This Python script provides a tool for adding watermarks to images and converting them to the WEBP format. It allows you to specify the transparency of the watermark, resize the watermark to fit the image, and adjust the dimensions and quality of the resulting WEBP images.

## Features

- **Watermarking**: Adds a watermark to the center of an image, resizing the watermark to ensure it fits within the image while maintaining its aspect ratio.
- **WEBP Conversion**: Converts images to the WEBP format, allowing for specification of image dimensions and quality.
- **Batch Processing**: Processes multiple images in one go, applying watermarks and converting them to WEBP format.

## Prerequisites

Before you can run this script, you need to have Python installed on your system along with the PIL library. If you do not have the PIL library installed, you can install it using pip:

```bash
pip3 install Pillow
```

## Usage

To use this script, you need to provide the paths to the images you want to process, as well as the path to the watermark image. You can also specify the quality, the dimensions for resizing, and the prefix for the output filenames.

### Command-Line Arguments

- `files`: List of image files to process. Each file should be a `.png` or `.jpg`.
- `--quality`: Quality of the output WEBP images (default is 85).
- `--prefix`: Prefix to add to the filename when saved.
- `--width`: Width to resize the image to (default is 1024).
- `--height`: Height to resize the image to (default is 1024).
- `--watermark`: Path to the watermark image (required).
- `--transparency`: Transparency of the watermark (0 to 255, where 0 is fully transparent and 255 is fully opaque; default is 128).

### Example Command

```bash
python3 convert.py image1.jpg image2.png --watermark /path/to/watermark.png --transparency 125 --quality 70 --width 800 --height 600 --prefix converted_
```

This command will process `image1.jpg` and `image2.png`, add the watermark from `/path/to/watermark.png`, and save the converted WEBP images with a quality of 90 and dimensions of 800x600 pixels. The output files will be prefixed with `converted_`.

## Output

The script will create a directory named `./webp` where it will save all the converted images. The names of the output files will be derived from the original filenames, prefixed as specified, and saved in WEBP format.
