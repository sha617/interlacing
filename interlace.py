import argparse
from wand.image import Image
from wand.color import Color

def parse_arguments():
    parser = argparse.ArgumentParser(description="Interlace multiple images with specified PPI and slice size.")
    parser.add_argument("images", type=str, nargs='+', help="Paths to the image files (minimum of 2)")
    parser.add_argument("--ppi", type=int, default=300, help="Pixels per inch for the output image (default: 300)")
    parser.add_argument("--slice", type=int, default=10, help="Slice size in pixels (default: 10)")
    parser.add_argument("--horz", action="store_true", help="Use horizontal slicing instead of vertical")
    parser.add_argument("--output", type=str, default="interlaced_output.jpg", help="Output filename (default: interlaced_output.jpg)")
    return parser.parse_args()

def interlace_images(image_paths, output_path, ppi, slice_size, horizontal):
    # Number of images
    num_images = len(image_paths)
    if num_images < 2:
        raise ValueError("At least two images are required for interlacing.")

    # Open all images
    images = [Image(filename=img_path) for img_path in image_paths]

    # Ensure all images have the same dimensions
    min_width = min(img.width for img in images)
    min_height = min(img.height for img in images)

    # Crop all images to the smallest dimensions centered
    for img in images:
        img.crop(width=min_width, height=min_height, gravity='center')

    # Create a blank canvas for the output image
    with Image(width=min_width, height=min_height, background=Color('white')) as output_img:
        if horizontal:
            # Horizontal interlacing with specified slice size
            for y in range(0, min_height, num_images * slice_size):
                slices = []
                for i, img in enumerate(images):
                    height_slice = min(num_images * slice_size, min_height - y)
                    # Crop `X * S` height from each image
                    slice_part = img[y:y+height_slice, 0:min_width]
                    # Scale down to `S` pixels in height
                    slice_part.sample(min_width, slice_size)
                    slices.append(slice_part)
                # Append scaled slices one by one
                for i, slice_img in enumerate(slices):
                    output_img.composite(slice_img, left=0, top=y + i * slice_size)
        else:
            # Vertical interlacing with specified slice size
            for x in range(0, min_width, num_images * slice_size):
                slices = []
                for i, img in enumerate(images):
                    width_slice = min(num_images * slice_size, min_width - x)
                    # Crop `X * S` width from each image
                    slice_part = img[0:min_height, x:x+width_slice]
                    # Scale down to `S` pixels in width
                    slice_part.sample(slice_size, min_height)
                    slices.append(slice_part)
                # Append scaled slices one by one
                for i, slice_img in enumerate(slices):
                    output_img.composite(slice_img, left=x + i * slice_size, top=0)

        # Set the PPI of the output image
        output_img.resolution = (ppi, ppi)

        # Save the interlaced image
        output_img.save(filename=output_path)

def main():
    args = parse_arguments()
    interlace_images(args.images, args.output, args.ppi, args.slice, args.horz)

if __name__ == "__main__":
    main()

