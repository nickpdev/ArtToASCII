import PIL.Image
from pathlib import Path

# ascii characters used to build the output text
ASCII_CHARS = list("@#%&8BMW*+=-:. ")

# resize image according to a new width
def resize_image(image, new_width = 150):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.45)
    resized_image = image.resize((new_width, new_height))
    return(resized_image)

# convert each pixel to grayscale
def grayify(image):
    grayscale_image = image.convert("L")
    return(grayscale_image)

# convert pixels to a string of ASCII characters
def pixels_to_ascii(image):
    pixels = image.get_flattened_data()
    characters = "".join(
        ASCII_CHARS[pixel * (len(ASCII_CHARS) - 1) // 255]
        for pixel in pixels
    )
    return characters

def pixels_to_colored_ascii(image):
    rgb_image = image.convert("RGB")
    grayscale_image = grayify(image)

    rgb_pixels = list(rgb_image.get_flattened_data())
    grayscale_pixels = list(grayscale_image.get_flattened_data())

    colored_chars = []

    for gray_pixel, rgb_pixel in zip(grayscale_pixels, rgb_pixels):
        r, g, b = rgb_pixel

        char = ASCII_CHARS[gray_pixel * (len(ASCII_CHARS) - 1) // 255]

        colored_char = f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        colored_chars.append(colored_char)

    return colored_chars

def main(new_width = 150):
    # open image from user-input
    path = input("Enter the pathname to an image:\n")
    print("Processing image...")

    try:
        image = PIL.Image.open(path)
    except:
        print(path, "is not a valid pathname to an image.")
        return

    color_choice = input("\nDo you want the ASCII image to be colored? yes/no:\n").lower()

    # resize image once
    resized_image = resize_image(image, new_width)

    if color_choice == "yes" or color_choice == "y":
        # convert image to colored ASCII
        new_image_data = pixels_to_colored_ascii(resized_image)

        # format colored ASCII
        pixel_count = len(new_image_data)
        ascii_image = "\n".join(
            "".join(new_image_data[i:i + new_width])
            for i in range(0, pixel_count, new_width)
        )

        file_suffix = "ascii_color"

    else:
        # convert image to normal ASCII
        new_image_data = pixels_to_ascii(grayify(resized_image))

        # format normal ASCII
        pixel_count = len(new_image_data)
        ascii_image = "\n".join(
            new_image_data[i:i + new_width]
            for i in range(0, pixel_count, new_width)
        )

        file_suffix = "ascii"

    # print result
    print(ascii_image)

    # save results to outputs folder
    output_folder = Path("outputs")
    output_folder.mkdir(exist_ok=True)

    image_name = Path(path).stem
    output_path = output_folder / f"{image_name}_{file_suffix}.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ascii_image)

    print(f"Saved ASCII image to {output_path}")

main(150)