import os
import glob

from process_data.process_images_tools import (GeoImageProcessor, calculate_index, scale_to_8bit, BASEPATH, NDWI_DIR,
                                               NDVI_DIR, NDBI_DIR)



BASEPATH_LANDSAT8 = f"{BASEPATH}/la_mosca/landsat8/bands/"
BASEPATH_SENTINEL2 = f"{BASEPATH}/la_mosca/sentinel2/bands/"



def get_ndwi_la_mosca():
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


def get_ndvi_la_mosca():
    """
    Processes all Sentinel-2 images in the given directories to compute NDVI and save results.
    """
    os.makedirs(NDWI_DIR, exist_ok=True)

    band4_files = sorted(glob.glob(os.path.join(BASEPATH_SENTINEL2 + 'B4', "*.tif")))
    band8_files = sorted(glob.glob(os.path.join(BASEPATH_SENTINEL2 + 'B8', "*.tif")))

    for b4_path, b8_path in zip(band4_files, band8_files):
        filename = os.path.basename(b4_path)
        output_filename = filename.replace("mean", "ndvi")
        output_path = os.path.join(NDWI_DIR, output_filename)

        geo_b4 = GeoImageProcessor(b4_path)
        geo_b8 = GeoImageProcessor(b8_path)

        ndvi = calculate_index(geo_b8.data, geo_b4.data)
        geo_b4.data = scale_to_8bit(ndvi)
        geo_b4.save(output_path)

        print(f"Processed: {output_filename}")


def get_ndvi_la_mosca_landsat8():
    """
    Processes all Landsat 8 images in the given directories to compute NDVI and save results.
    """
    os.makedirs(NDVI_DIR, exist_ok=True)

    band4_files = sorted(glob.glob(os.path.join(BASEPATH_LANDSAT8 + 'SR_B4', "*.tif")))
    band5_files = sorted(glob.glob(os.path.join(BASEPATH_LANDSAT8 + 'SR_B5', "*.tif")))

    for b4_path, b5_path in zip(band4_files, band5_files):
        filename = os.path.basename(b4_path)
        output_filename = filename.replace("mean", "ndvi")
        output_path = os.path.join(NDVI_DIR, output_filename)

        geo_b4 = GeoImageProcessor(b4_path)
        geo_b5 = GeoImageProcessor(b5_path)

        ndvi = calculate_index(geo_b5.data, geo_b4.data)  # (NIR - Red) / (NIR + Red)
        geo_b4.data = scale_to_8bit(ndvi)
        geo_b4.save(output_path)

        print(f"Processed Landsat 8 NDVI: {output_filename}")


def get_ndwi_la_mosca_landsat8():
    """
    Processes all Landsat 8 images in the given directories to compute NDWI and save results.
    """
    os.makedirs(NDVI_DIR, exist_ok=True)

    band3_files = sorted(glob.glob(os.path.join(BASEPATH_LANDSAT8 + 'SR_B3', "*.tif")))
    band5_files = sorted(glob.glob(os.path.join(BASEPATH_LANDSAT8 + 'SR_B5', "*.tif")))

    for b3_path, b5_path in zip(band3_files, band5_files):
        filename = os.path.basename(b3_path)
        output_filename = filename.replace("mean", "ndwi")
        output_path = os.path.join(NDWI_DIR, output_filename)

        geo_b3 = GeoImageProcessor(b3_path)
        geo_b5 = GeoImageProcessor(b5_path)

        ndwi = calculate_index(geo_b5.data, geo_b3.data)
        geo_b3.data = scale_to_8bit(ndwi)
        geo_b3.save(output_path)

        print(f"Processed Landsat 8 NDWI: {output_filename}")


def get_ndbi_la_mosca_landsat8():
    """
    Processes all Landsat 8 images in the given directories to compute NDBI and save results.
    """
    os.makedirs(NDBI_DIR, exist_ok=True)

    band6_files = sorted(glob.glob(os.path.join(BASEPATH_LANDSAT8 + 'SR_B6', "*.tif")))  # SWIR
    band5_files = sorted(glob.glob(os.path.join(BASEPATH_LANDSAT8 + 'SR_B5', "*.tif")))  # NIR

    for b6_path, b5_path in zip(band6_files, band5_files):
        filename = os.path.basename(b6_path)
        output_filename = filename.replace("mean", "ndbi")
        output_path = os.path.join(NDBI_DIR, output_filename)

        geo_b6 = GeoImageProcessor(b6_path)
        geo_b5 = GeoImageProcessor(b5_path)

        ndbi = calculate_index(geo_b6.data, geo_b5.data)  # (SWIR - NIR) / (SWIR + NIR)
        geo_b6.data = scale_to_8bit(ndbi)
        geo_b6.save(output_path)

        print(f"Processed Landsat 8 NDBI: {output_filename}")

if __name__ == "__main__":
    get_ndbi_la_mosca_landsat8()

