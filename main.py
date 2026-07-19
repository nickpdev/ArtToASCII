import PIL.Image
from PIL import ImageDraw, ImageFont, ImageOps
from pathlib import Path

# detailed character ramp for colored PNG output
COLOR_ASCII_CHARS = list("@$B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# cleaner character ramp for plain text output
TEXT_ASCII_CHARS = list("@#%*+=-:.    ")

# detail levels control the ASCII image width
DETAIL_LEVELS = {
    "low": 80,
    "normal": 150,
    "high": 250
}


# resize image according to a new width
def resize_image(image, new_width=150):
    width, height = image.size
    ratio = height / width

    # 0.45 helps correct terminal/text character height distortion
    new_height = int(new_width * ratio * 0.45)

    resized_image = image.resize((new_width, new_height))
    return resized_image


# resize image for colored PNG output while preserving the original aspect ratio
def resize_image_for_png(image, new_width=150, one_char_width=10, one_char_height=18):
    width, height = image.size
    ratio = height / width

    # adjusts the resized pixel height based on the final drawn character cell size
    new_height = int(new_width * ratio * (one_char_width / one_char_height))

    resized_image = image.resize((new_width, new_height))
    return resized_image


# apply phone/camera orientation metadata so vertical photos stay vertical
def fix_orientation(image):
    return ImageOps.exif_transpose(image)


# convert each pixel to grayscale
def grayify(image):
    grayscale_image = image.convert("L")
    return grayscale_image

# improve grayscale contrast before converting to plain ASCII
def enhance_grayscale(image):
    # stretches the brightness range, but ignores extreme dark/light outliers
    enhanced_image = ImageOps.autocontrast(image, cutoff=2)
    return enhanced_image


# convert pixels to a string of ASCII characters
def pixels_to_ascii(image, ascii_chars, white_threshold=245):
    pixels = image.get_flattened_data()

    # map each grayscale pixel value from 0-255 to a character in the selected ramp
    # very bright pixels become blank spaces to reduce noise
    characters = "".join(
        " " if pixel >= white_threshold else ascii_chars[pixel * (len(ascii_chars) - 1) // 255]
        for pixel in pixels
    )

    return characters


# create and save a colored ASCII image as a PNG
def save_colored_ascii_png(image, output_path, new_width=150):
    # size of each ASCII character cell in the final PNG
    one_char_width = 10
    one_char_height = 18
    font_size = 15

    # resize the image before converting it to ASCII
    resized_image = resize_image_for_png(image, new_width, one_char_width, one_char_height)

    # RGB image is used for the color of each character
    rgb_image = resized_image.convert("RGB")

    # grayscale image is used to choose which ASCII character to draw
    grayscale_image = grayify(resized_image)

    width, height = rgb_image.size

    # create a blank black image that the ASCII characters will be drawn onto
    output_image = PIL.Image.new(
        "RGB",
        (one_char_width * width, one_char_height * height),
        color=(0, 0, 0)
    )

    # drawing object used to place text onto the output image
    draw = ImageDraw.Draw(output_image)

    # try to use a monospace Mac font, otherwise fall back to Pillow's default font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", font_size)
    except:
        font = ImageFont.load_default()

    # load pixel access objects so we can read RGB and grayscale values by coordinate
    rgb_pixels = rgb_image.load()
    grayscale_pixels = grayscale_image.load()

    # loop through each pixel and draw an ASCII character with the original RGB color
    for y in range(height):
        for x in range(width):
            r, g, b = rgb_pixels[x, y]
            gray = grayscale_pixels[x, y]

            # choose ASCII character based on brightness
            char = COLOR_ASCII_CHARS[gray * (len(COLOR_ASCII_CHARS) - 1) // 255]

            # draw the character at the matching position in the output image
            draw.text(
                (x * one_char_width, y * one_char_height),
                char,
                font=font,
                fill=(r, g, b)
            )

    # save the final colored ASCII image
    output_image.save(output_path)


def main(new_width=150):
    # ask user for the image path
    path = input("Enter the pathname to an image:\n")

    # try to open the image
    try:
        image = PIL.Image.open(path)
        image = fix_orientation(image)
    except:
        print(path, "is not a valid pathname to an image.")
        return

    # ask whether to create a colored PNG or normal text ASCII
    color_choice = input("\nDo you want the ASCII image to be colored? yes/no:\n").lower()

    # ask user how detailed they want the output to be
    detail_choice = input("\nChoose detail level: low/normal/high:\n").lower()

    # use the selected detail level, or fall back to normal if the input is invalid
    if detail_choice not in DETAIL_LEVELS:
        print("Invalid detail level. Using normal.")
        detail_choice = "normal"

    new_width = DETAIL_LEVELS[detail_choice]

    # create the outputs folder if it does not already exist
    output_folder = Path("outputs")
    output_folder.mkdir(exist_ok=True)

    # use the original image filename for the output file
    image_name = Path(path).stem

    if color_choice == "yes" or color_choice == "y":
        # colored ASCII is saved as a PNG so the RGB colors display correctly
        output_path = output_folder / f"{image_name}_ascii_color_{detail_choice}.png"

        print("\nProcessing colored ASCII image...")
        save_colored_ascii_png(image, output_path, new_width)

        print(f"Saved colored ASCII image to {output_path}")

    else:
        # normal ASCII is saved as a plain text file
        resized_image = resize_image(image, new_width)

        grayscale_image = grayify(resized_image)
        grayscale_image = enhance_grayscale(grayscale_image)

        new_image_data = pixels_to_ascii(grayscale_image, TEXT_ASCII_CHARS, white_threshold=240)

        pixel_count = len(new_image_data)

        # split the long ASCII string into lines matching the image width
        ascii_image = "\n".join(
            new_image_data[i:i + new_width]
            for i in range(0, pixel_count, new_width)
        )

        print(ascii_image)

        output_path = output_folder / f"{image_name}_ascii_{detail_choice}.txt"

        # save the plain ASCII image
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ascii_image)

        print(f"Saved ASCII image to {output_path}")


main(150)