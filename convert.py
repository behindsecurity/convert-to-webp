#!/usr/bin/env python3

import os
import sys
import argparse
from PIL import Image

def convert_to_webp(filename:str, dimensions: tuple, quality:int, prefix:str) -> str:
    """Uses PIL library to convert image stream to webp, saving locally with specified quality and filename prefix.

    Arguments:
        filename:str - Name of the file to save.
        dimensions:tuple - A tuple containing dimensions to resize the image to. Example: (500, 333)
        quality:int - Image quality for the output file.
        prefix:str - Prefix to add to the file name when saved.
    
    Return:str 
        Newly saved file's filename
    """
    image = Image.open(filename)
    image.thumbnail(dimensions)
    image = image.convert("RGB")

    # Splitting filename to remove extension and add prefix
    base_filename = os.path.splitext(os.path.basename(filename))[0]
    new_filename = f"./webp/{prefix}{base_filename}.webp"
    image.save(new_filename, format="webp", optimize=True, quality=quality, method=6)
    return new_filename


def main():
    parser = argparse.ArgumentParser(description='Convert images to WEBP format with specified quality and filename prefix.')
    parser.add_argument('files', nargs='+', help='Files to convert')
    parser.add_argument('--quality', type=int, default=70, help='Quality of the output WEBP images')
    parser.add_argument('--prefix', type=str, default='', help='Prefix to add to the file name')
    parser.add_argument('--width', type=int, default=1024, help='Width to resize the image to')
    parser.add_argument('--height', type=int, default=1024, help='Height to resize the image to')
    args = parser.parse_args()

    if not os.path.isdir('./webp'):
        os.mkdir('./webp')

    original_files = []
    new_filenames = []

    for file in args.files:
        if file.endswith('.png') or file.endswith('.jpg'):
            original_files.append( (file, os.path.getsize(f'./{file}')) )
            new_filename = convert_to_webp(file, (args.width, args.height), args.quality, args.prefix)
            new_filenames.append(new_filename)

    if not original_files:
        print('[~] No valid image files specified. Please provide .png or .jpg files.')
        sys.exit()

    old_size = sum(size for _, size in original_files)
    new_sizes = [os.path.getsize(f'./{filename}') for filename in new_filenames]
    new_size = sum(new_sizes)

    difference_percentage = round((abs(new_size - old_size) / old_size) * 100.0, 2) if old_size > 0 else 0
    message = 'choosing quality over performance' if args.quality >= 60 else 'choosing performance over quality'
    file_quantity = len(original_files)

    print(f"""
        [{file_quantity} File{'s' if file_quantity > 1 else ''}] {', '.join(os.path.basename(filename) for filename, _ in original_files)}
        [Quality] {args.quality}% ({message})
        [Difference] {difference_percentage}% (higher is better - {new_size} bytes over {old_size} bytes)
        """)

if __name__ == '__main__':
    main()
