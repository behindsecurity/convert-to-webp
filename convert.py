#!/usr/bin/env python3

import argparse
import sys
import os
from PIL import Image


def add_watermark(image: Image.Image, watermark_image_path: str, transparency: int) -> Image.Image:
    """Applies a resized watermark to the center of an image with adjustable transparency.

    Arguments:
        image (Image.Image): The PIL Image object of the base image.
        watermark_image_path (str): The path to the watermark image.
        transparency (int): The transparency level of the watermark (0 to 255; 0 is fully transparent, 255 is fully opaque).
    
    Returns:
        Image.Image: The watermarked image.
    """
    watermark = Image.open(watermark_image_path)
    base_width, base_height = image.size

    # Convert the watermark image to RGBA if not already
    if watermark.mode != 'RGBA':
        watermark = watermark.convert("RGBA")

    # Resize watermark if it's larger than the base image
    watermark_width, watermark_height = watermark.size
    if watermark_width > base_width or watermark_height > base_height:
        scale = min(base_width / watermark_width, base_height / watermark_height)
        new_size = (int(watermark_width * scale), int(watermark_height * scale))
        watermark = watermark.resize(new_size, Image.ANTIALIAS)

    # Adjust the watermark transparency
    alpha = watermark.split()[3]  # Get the alpha channel
    alpha = alpha.point(lambda p: p * transparency / 255)
    watermark.putalpha(alpha)

    # Calculate the position for the watermark: centered
    watermark_width, watermark_height = watermark.size
    position = ((base_width - watermark_width) // 2, (base_height - watermark_height) // 2)

    # Create a transparent layer the size of the base image
    transparent = Image.new('RGBA', image.size, (0,0,0,0))
    # Paste the watermark in the center
    transparent.paste(watermark, position, watermark)
    # Blend with the base image
    watermarked_image = Image.alpha_composite(image.convert('RGBA'), transparent)
    return watermarked_image.convert('RGB')


def convert_to_webp(base_image: Image.Image, filename: str, dimensions: tuple, quality: int, prefix: str) -> str:
    """Converts and resizes a PIL Image object to webp, saving locally with specified quality and filename prefix.

    Arguments:
        base_image (Image.Image): The PIL Image object to convert.
        filename (str): Name of the original file to derive the new filename.
        dimensions (tuple): A tuple containing dimensions to resize the image to. Example: (500, 333)
        quality (int): Image quality for the output file.
        prefix (str): Prefix to add to the file name when saved.
    
    Returns:
        str: Newly saved file's filename
    """
    base_image.thumbnail(dimensions)
    
    # Splitting filename to remove extension and add prefix
    base_filename = os.path.splitext(os.path.basename(filename))[0]
    new_filename = f"./webp/{prefix}{base_filename}.webp"
    base_image.save(new_filename, format="webp", optimize=True, quality=quality, method=6)
    
    return new_filename


def main():
    parser = argparse.ArgumentParser(description='Convert images to WEBP format with watermarking, specified quality and filename prefix.')
    parser.add_argument('files', nargs='+', help='Files to convert')
    parser.add_argument('--quality', type=int, default=85, help='Quality of the output WEBP images')
    parser.add_argument('--prefix', type=str, default='', help='Prefix to add to the file name')
    parser.add_argument('--width', type=int, default=1024, help='Width to resize the image to')
    parser.add_argument('--height', type=int, default=1024, help='Height to resize the image to')
    parser.add_argument('--watermark', type=str, required=True, help='Path to the watermark image')
    parser.add_argument('--transparency', type=int, default=128, help='Transparency of the watermark (0 to 255)')
    args = parser.parse_args()

    if not os.path.isdir('./webp'):
        os.mkdir('./webp')

    for file in args.files:
        if file.endswith('.png') or file.endswith('.jpg'):
            original_image = Image.open(file)
            watermarked_image = add_watermark(original_image, args.watermark, args.transparency)
            new_filename = convert_to_webp(watermarked_image, file, (args.width, args.height), args.quality, args.prefix)
            print(f"Processed {file} -> {new_filename}")

    print('Conversion complete.')

if __name__ == '__main__':
    main()
