import os
import random
import shutil
import cv2

def has_class(label_path):
    # Load label image
    label_image = cv2.imread(label_path, cv2.IMREAD_GRAYSCALE)

    # Check if any non-black pixels are present
    return not (label_image == 0).all()


def sample_dataset(input_dir, output_dir, sample_size_per_class):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over each class
    for class_name in ['nutrient_deficiency', 'drydown', 'weed_cluster']:
        # Initialize counters for the current class
        sampled_count = 0
        class_count = 0

        # Get list of image files from the RGB folder
        rgb_files = os.listdir(os.path.join(input_dir, 'images', 'rgb'))

        # Shuffle the list of image files
        random.shuffle(rgb_files)

        # Iterate over each image
        for img_name in rgb_files:
            img_base_name = os.path.splitext(img_name)[0]

            # Check if the corresponding label exists and if it contains the specified class
            label_path = os.path.join(input_dir, 'labels', class_name, img_base_name + '.png')
            if os.path.exists(label_path) and has_class(label_path):
                # Copy the RGB image
                shutil.copyfile(os.path.join(input_dir, 'images', 'rgb', img_name),
                                os.path.join(output_dir, 'rgb', img_name))

                # Copy the label
                shutil.copyfile(label_path,
                                os.path.join(output_dir, 'labels', class_name, img_base_name + '.png'))

                # Increment counters
                sampled_count += 1
                class_count += 1

            # Check if the desired sample size for the current class has been reached
            if sampled_count >= sample_size_per_class:
                break

        print(f"Sampled {class_count} images with {class_name} labels to {output_dir}")



input_dir = '/Users/raybaldwin/Downloads/Agriculture-Vision-2021/train'
output_dir = '/Users/raybaldwin/V4A/supervised/final_final'
sample_size_per_class = 1000  # Adjust as needed

sample_dataset(input_dir, output_dir, sample_size_per_class)