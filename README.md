# Image Renamer Script

This Python script renames image files in a specified folder based on their creation dates extracted from EXIF metadata
or extended file attributes. It supports a variety of image formats as well as some video formats.

## Prerequisites

- Python 3.x
- [Pillow](https://python-pillow.org/) library for handling image files

## Installation

To install the required Pillow library, use pip:

```bash
pip install pillow
```

### Usage

Set the Folder Path: Update the folder_path variable in the script to point to the directory containing your images.

```python
folder_path = '/path/to/your/folder'
```

### Run the Script: Execute the script to rename the image files.

```bash
python file_renamer.py
```

The script currently supports the following file types:

	•	Images: .png, .jpg, .jpeg, .tiff, .bmp, .gif, .heic
	•	Videos: .mp4, .mov

How It Works

	1.	Extract EXIF Data: The script attempts to extract EXIF data from the images to get the creation date.
	2.	Fallback to Extended Attributes: If EXIF data is unavailable or does not contain the creation date, the script retrieves the creation date from the extended file attributes.
	3.	Rename Files: Files are renamed to the format YYYYMMDD_HHMMSS.ext based on the extracted creation date.