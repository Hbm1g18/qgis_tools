# To call this script on a raster use py reclassify_table.py {input raster} {output directory} --num_intervals{amount}

import argparse
import os
import rasterio
from rasterio import Affine
import numpy as np

def reclassify_raster(input_path, output_path, num_intervals):
    # Open the raster file
    with rasterio.open(input_path) as src:
        # Read raster data
        raster_data = src.read(1)

        # Find the max and min values
        max_value = np.max(raster_data)
        min_value = np.min(raster_data)

        # Calculate the range and interval for reclassification
        value_range = max_value - min_value
        interval = value_range / num_intervals

        # Reclassify the raster into specified number of groups
        reclassified_data = np.digitize(raster_data, bins=np.arange(min_value, max_value, interval))

        # Update metadata for the output raster
        profile = src.profile
        profile.update(count=1)  # Update the number of bands to 1

        # Write the reclassified data to the output raster
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(reclassified_data, 1)

def main():
    parser = argparse.ArgumentParser(description='Reclassify a raster into specified intervals.')
    parser.add_argument('input_raster', help='Path to the input raster file')
    parser.add_argument('output_folder', help='Path to the output folder for the reclassified raster')
    parser.add_argument('--num_intervals', type=int, default=10, help='Number of intervals for reclassification')

    args = parser.parse_args()

    # Extract the filename without the extension
    input_filename = os.path.splitext(os.path.basename(args.input_raster))[0]

    # Construct the output path based on the input raster and output folder
    output_raster_path = os.path.join(args.output_folder, f'{input_filename}_reclassified.tif')

    reclassify_raster(args.input_raster, output_raster_path, args.num_intervals)

    print(f"{args.input_raster} reclassified to {args.num_intervals} bands and saved in {args.output_folder}")

if __name__ == "__main__":
    main()
