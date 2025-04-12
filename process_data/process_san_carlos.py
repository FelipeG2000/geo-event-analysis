import os
import glob

from process_data.process_images_tools import GeoImageProcessor, calculate_index, scale_to_8bit, BASEPATH, NDWI_DIR, NDVI_DIR



BASEPATH_LANDSAT8 = f"{BASEPATH}/san_carlos/landsat8/bands/"
BASEPATH_SENTINEL2 = f"{BASEPATH}/san_carlos/sentinel2/bands/"



def get_ndwi_san_carlos_sentinel2():
    """
    Processes all Sentinel-2 images in the given directories to compute NDWI and save results.
    """
    os.makedirs(NDWI_DIR, exist_ok=True)

    band3_files = sorted(glob.glob(os.path.join(BASEPATH_SENTINEL2 + 'B3', "*.tif")))
    band8_files = sorted(glob.glob(os.path.join(BASEPATH_SENTINEL2 + 'B8', "*.tif")))

    for b3_path, b8_path in zip(band3_files, band8_files):
        filename = os.path.basename(b3_path)
        output_filename = filename.replace("mean", "ndwi")
        output_path = os.path.join(NDWI_DIR, output_filename)

        geo_b3 = GeoImageProcessor(b3_path)
        geo_b8 = GeoImageProcessor(b8_path)

        ndwi = calculate_index(geo_b3.data, geo_b8.data)
        geo_b3.data = scale_to_8bit(ndwi)
        geo_b3.save(output_path)

        print(f"Processed: {output_filename}")


def get_ndvi_san_carlos_sentinel2():
    """
    Processes all Sentinel-2 images in the given directories to compute NDVI and save results.
    """
    os.makedirs(NDVI_DIR, exist_ok=True)

    band4_files = sorted(glob.glob(os.path.join(BASEPATH_SENTINEL2 + "B4", "*.tif")))
    band8_files = sorted(glob.glob(os.path.join(BASEPATH_SENTINEL2 + "B8", "*.tif")))

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
    get_ndvi_san_carlos_sentinel2()

