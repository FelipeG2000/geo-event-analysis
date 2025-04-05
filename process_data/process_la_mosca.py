import os
import glob

from process_data.process_images_tools import GeoImageProcessor, calculate_index, scale_to_8bit



# Base path where Sentinel-2 images are stored
BASEPATH_B3 = "/home/felipe/MiDrive/GEE_Exports/la_mosca/sentinel2/bands/B3"
BASEPATH_B8 = "/home/felipe/MiDrive/GEE_Exports/la_mosca/sentinel2/bands/B8"
OUTPUT_DIR = "ndwi"


def get_ndwi_la_mosca():
    """
    Processes all Sentinel-2 images in the given directories to compute NDWI and save results.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    band3_files = sorted(glob.glob(os.path.join(BASEPATH_B3, "*.tif")))
    band8_files = sorted(glob.glob(os.path.join(BASEPATH_B8, "*.tif")))

    for b3_path, b8_path in zip(band3_files, band8_files):
        filename = os.path.basename(b3_path)
        output_filename = filename.replace("mean", "ndwi")
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        geo_b3 = GeoImageProcessor(b3_path)
        geo_b8 = GeoImageProcessor(b8_path)

        ndwi = calculate_index(geo_b3.data, geo_b8.data)
        geo_b3.data = scale_to_8bit(ndwi)
        geo_b3.save(output_path)

        print(f"Processed: {output_filename}")


if __name__ == "__main__":
    get_ndwi_la_mosca()

