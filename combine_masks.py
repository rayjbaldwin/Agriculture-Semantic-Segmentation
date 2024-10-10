import os
import numpy as np
from PIL import Image

# Paths to your RGB images and label folders
rgb_folder = "/Users/raybaldwin/V4A/supervised/final_final/rgb"
weed_cluster_folder = "/Users/raybaldwin/V4A/supervised/final_final/labels/weed_cluster"
nutrient_deficiency_folder = "/Users/raybaldwin/V4A/supervised/final_final/labels/nutrient_deficiency"
drydown_folder = "/Users/raybaldwin/V4A/supervised/final_final/labels/drydown"

# Output folder to save combined masks
output_folder = "/Users/raybaldwin/V4A/supervised/final_final/Combined_Masks"
os.makedirs(output_folder, exist_ok=True)

# Get list of RGB images
rgb_images = os.listdir(rgb_folder)

# Iterate over RGB images
for rgb_image in rgb_images:
    # Load RGB image
    rgb_image_path = os.path.join(rgb_folder, rgb_image)
    rgb = np.array(Image.open(rgb_image_path))

    # Initialize the combined mask with zeros
    combined_mask = np.zeros_like(rgb)

    # Load binary label files if they exist, otherwise consider them as blank
    if os.path.exists(os.path.join(weed_cluster_folder, rgb_image.replace('.jpg', '.png'))):
        weed_cluster = np.array(Image.open(os.path.join(weed_cluster_folder, rgb_image.replace('.jpg', '.png'))))
        combined_mask[weed_cluster > 0] = 3

    if os.path.exists(os.path.join(nutrient_deficiency_folder, rgb_image.replace('.jpg', '.png'))):
        nutrient_deficiency = np.array(Image.open(os.path.join(nutrient_deficiency_folder, rgb_image.replace('.jpg', '.png'))))
        combined_mask[nutrient_deficiency > 0] = 2

    if os.path.exists(os.path.join(drydown_folder, rgb_image.replace('.jpg', '.png'))):
        drydown = np.array(Image.open(os.path.join(drydown_folder, rgb_image.replace('.jpg', '.png'))))
        combined_mask[drydown > 0] = 1

    # Save combined mask
    combined_mask_image = Image.fromarray(combined_mask.astype(np.uint8))
    combined_mask_image.save(os.path.join(output_folder, rgb_image.replace('.jpg', '.png')))
