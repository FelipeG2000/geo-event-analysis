import os
import glob

from process_data.process_images_tools import GeoImageProcessor, calculate_index, scale_to_8bit, BASEPATH_LANDSAT8, BASEPATH_SENTINEL2



# Base path where Sentinel-2 images are stored
OUTPUT_DIR = "ndwi"
NDVI_DIR = "ndvi"

def get_ndwi_cocorna_sentinel2():
    """
    Processes all Sentinel-2 images in the given directories to compute NDWI and save results.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    band3_files = sorted(glob.glob(os.path.join(BASEPATH_SENTINEL2 + 'B3', "*.tif")))
    band8_files = sorted(glob.glob(os.path.join(BASEPATH_SENTINEL2 + 'B8', "*.tif")))

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


def get_ndvi_cocorna_sentinel2():
    """
    Processes all Sentinel-2 images in the given directories to compute NDVI and save results.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    band4_files = sorted(glob.glob(os.path.join(BASEPATH_SENTINEL2 + 'B4', "*.tif")))
    band8_files = sorted(glob.glob(os.path.join(BASEPATH_SENTINEL2 + 'B8', "*.tif")))

    for b4_path, b8_path in zip(band4_files, band8_files):
        filename = os.path.basename(b4_path)
        output_filename = filename.replace("mean", "ndvi")
        output_path = os.path.join(NDVI_DIR, output_filename)

        geo_b4 = GeoImageProcessor(b4_path)
        geo_b8 = GeoImageProcessor(b8_path)

        ndvi = calculate_index(geo_b8.data, geo_b4.data)
        geo_b4.data = scale_to_8bit(ndvi)
        geo_b4.save(output_path)

        print(f"Processed: {output_filename}")

if __name__ == "__main__":
    get_ndvi_cocorna_sentinel2
