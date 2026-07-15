import PIL.Image
from pathlib import Path

# ascii characters used to build the output text
ASCII_CHARS = list("@$B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

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

def main(new_width = 100):
    # open image from user-input
    path = input("Enter the pathname to an image:\n")
    try:
        image = PIL.Image.open(path)
    except:
        print(path, "is not a valid pathname to an image.")
        return

    # convert image to ASCII
    new_image_data = pixels_to_ascii(grayify(resize_image(image, new_width)))

    # format
    pixel_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i+new_width)] for i in range(0, pixel_count, new_width))

    # print result
    print(ascii_image)

    # save result to "ascii_image.txt"
    output_folder = Path("outputs")
    output_folder.mkdir(exist_ok=True)

    image_name = Path(path).stem
    output_path = output_folder / f"{image_name}_ascii.txt"

    with open(output_path, "w") as f:
        f.write(ascii_image)

    print(f"Saved ASCII image to {output_path}")

main(150)