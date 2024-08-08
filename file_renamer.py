# pip install pillow

import os

from PIL import Image
from PIL.ExifTags import TAGS
import datetime
import subprocess


def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image.getexif()
        if not exif_data:
            return None
        exif = {}
        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            exif[decoded] = value
        return exif
    except Exception as e:
        print(f'Error retrieving EXIF data for {image_path}: {e}')
        return None


def get_creation_date_from_exif(exif_data):
    date_str = exif_data.get("DateTimeOriginal")
    if date_str:
        # Format: "YYYY:MM:DD HH:MM:SS"
        try:
            return datetime.datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        except ValueError:
            return None
    return None


def get_creation_date_from_xattr(file_path):
    try:
        result = subprocess.run(['mdls', '-raw', '-name', 'kMDItemContentCreationDate', file_path], capture_output=True,
                                text=True)
        date_str = result.stdout.strip()
        if date_str:
            # Format: "YYYY-MM-DD HH:MM:SS Z"
            try:
                return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %z')
            except ValueError:
                return None
    except Exception as e:
        print(f'Error retrieving xattr data for {file_path}: {e}')
    return None


def rename_images(folder_path):
    for filename in os.listdir(folder_path):
        # if filename.lower().endswith(('.dng')):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.heic', '.mp4', '.mov')):
            image_path = os.path.join(folder_path, filename)
            exif_data = get_exif_data(image_path)
            creation_date = None
            if exif_data:
                creation_date = get_creation_date_from_exif(exif_data)
            if not creation_date:
                creation_date = get_creation_date_from_xattr(image_path)

            if creation_date:
                new_filename = creation_date.strftime('%Y%m%d_%H%M%S') + os.path.splitext(filename)[1]
                new_file_path = os.path.join(folder_path, new_filename)
                os.rename(image_path, new_file_path)
                print(f'Renamed {filename} to {new_filename}')
            else:
                print(f'No creation date found for {filename}')
        else:
            print(f'Skipping unsupported file type: {filename}')


if __name__ == "__main__":
    folder_path = ''
    rename_images(folder_path)

