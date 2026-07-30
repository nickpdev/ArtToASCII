# ArtToASCII

ArtToASCII is a Python command-line application that converts images into ASCII art. It supports both plain text ASCII output and colored ASCII PNG output, with optional AI-powered background removal and adjustable detail levels.

The user provides an image path, chooses whether to remove the background, chooses whether the result should be colored or plain text, selects a detail level, and the program saves the output into organized folders.

## Features

- Convert images into plain text ASCII art
- Convert images into colored ASCII PNG images
- Optional AI-powered background removal using `rembg`
- Preserve phone/camera orientation using EXIF metadata
- Choose from three detail levels:
  - `low`
  - `normal`
  - `high`
- Save outputs into organized folders by output type and detail level
- Use descriptive filenames that include:
  - original image name
  - output type
  - detail level
  - `no_bg` when background removal is used

## Tech Stack

- Python
- Pillow
- rembg
- onnxruntime

## Demo / Usage Flow

When the program runs, it guides the user through a simple command-line flow:

```text
Enter the pathname to an image:
images/example-image.jpg

Do you want to remove the background? yes/no:
yes

Do you want the ASCII image to be colored? yes/no:
yes

Choose detail level: low/normal/high:
high
```

The program then processes the image and saves the result into the appropriate output folder.

## Installation

These instructions are for macOS/Linux.

### 1. Clone the Repository

```bash
git clone https://github.com/nickpdev/ArtToASCII.git
cd ArtToASCII
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Program

```bash
python main.py
```

## Project Structure

A typical project structure looks like this:

```text
ArtToASCII/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── images/
│   └── example-image.jpg
└── outputs/
    ├── text/
    │   ├── low/
    │   ├── normal/
    │   └── high/
    └── color/
        ├── low/
        ├── normal/
        └── high/
```

The `images/` folder can be used to store local test images.

The `outputs/` folder is created automatically when the program saves generated ASCII files.

## Output Organization

Generated files are organized by output type and detail level:

```text
outputs/
├── text/
│   ├── low/
│   ├── normal/
│   └── high/
└── color/
    ├── low/
    ├── normal/
    └── high/
```

Plain text ASCII files are saved in the `outputs/text/` folders.

Colored ASCII PNG files are saved in the `outputs/color/` folders.

## Example Output Files

```text
outputs/text/high/example-image_ascii_high.txt
outputs/text/high/example-image_ascii_high_no_bg.txt

outputs/color/high/example-image_ascii_color_high.png
outputs/color/high/example-image_ascii_color_high_no_bg.png
```

The `_no_bg` suffix is added when background removal is enabled.

## Detail Levels

The program supports three detail levels:

| Detail Level | Description |
|---|---|
| `low` | Smaller output with fewer ASCII characters |
| `normal` | Balanced default output size |
| `high` | Larger output with more detail |

Higher detail levels create larger outputs and may take longer to process.

## Dependencies

This project uses:

- `Pillow` for image processing, resizing, grayscale conversion, drawing text, and saving image files
- `rembg` for AI-powered background removal
- `onnxruntime` as the backend used by `rembg`

All dependencies are listed in `requirements.txt`.

Install them with:

```bash
python -m pip install -r requirements.txt
```

## Notes

Background removal may take longer the first time it is used because `rembg` may need to download or load its model.

Background removal quality can vary depending on the image. It generally works best when the main subject is clearly separated from the background.

Input images and generated outputs can be ignored by Git so the repository stays clean and lightweight.

## Recommended `.gitignore`

```gitignore
.venv/
__pycache__/
*.pyc
.DS_Store
images/
outputs/
```

This keeps virtual environments, Python cache files, local input images, and generated outputs out of version control.

## Future Improvements

Potential future improvements include:

- Improve background-removal cleanup by tuning transparency/alpha pixels
- Improve ASCII contrast settings for different detail levels
- Add more output customization options