import os
import glob

from process_data.process_images_tools import (GeoImageProcessor, calculate_index, scale_to_8bit, BASEPATH, NDWI_DIR,
                                               NDVI_DIR, NDBI_DIR, OUTPUT_VH_DESPECKLED, TILE_SIZE, filter_large_image,
                                               OUTPUT_VV_DESPECKLED)


BASEPATH_LANDSAT8 = f"{BASEPATH}/cocorna/landsat8/bands/"
BASEPATH_SENTINEL2 = f"{BASEPATH}/cocorna/sentinel2/bands/"
SENTINEL1_ASCENDING_VV_PATH = "/home/felipe/MiDrive/GEE_Exports/cocorna/sentinel1/ascending/VV"
SENTINEL1_ASCENDING_VH_PATH = "/home/felipe/MiDrive/GEE_Exports/cocorna/sentinel1/ascending/VH"
SENTINEL1_VV_PATH = "/home/felipe/MiDrive/GEE_Exports/cocorna/sentinel1/descending/VV"
SENTINEL1_VH_PATH = "/home/felipe/MiDrive/GEE_Exports/cocorna/sentinel1/descending/VH"

def get_ndwi_cocorna_sentinel2():
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


def get_ndvi_cocorna_sentinel2():
    """
    Processes all Sentinel-2 images in the given directories to compute NDVI and save results.
    """
    os.makedirs(NDVI_DIR, exist_ok=True)

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

def get_ndbi_cocorna_sentinel2():
    """
    Processes all Sentinel-2 images in the given directories to compute NDBI and save results.
    """
    os.makedirs(NDBI_DIR, exist_ok=True)

    band11_files = sorted(glob.glob(os.path.join(BASEPATH_SENTINEL2 + "B11", "*.tif")))  # SWIR
    band8_files = sorted(glob.glob(os.path.join(BASEPATH_SENTINEL2 + "B8", "*.tif")))    # NIR

    for b11_path, b8_path in zip(band11_files, band8_files):
        filename = os.path.basename(b11_path)
        output_filename = filename.replace("mean", "ndbi")
        output_path = os.path.join(NDBI_DIR, output_filename)

        geo_b11 = GeoImageProcessor(b11_path)
        geo_b8 = GeoImageProcessor(b8_path)

        ndbi = calculate_index(geo_b11.data, geo_b8.data)  # (SWIR - NIR) / (SWIR + NIR)
        geo_b11.data = scale_to_8bit(ndbi)
        geo_b11.save(output_path)

        print(f"Processed Sentinel-2 NDBI: {output_filename}")


def get_ndvi_cocorna_landsat8():
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


def get_ndwi_cocorna_landsat8():
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


def get_ndbi_cocorna_landsat8():
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


def get_filtered_sentinel1_ascending_vh_cocorna():
    os.makedirs(OUTPUT_VH_DESPECKLED, exist_ok=True)
    image_paths = sorted(glob.glob(os.path.join(SENTINEL1_ASCENDING_VH_PATH, "*.tif")))
    count=0
    for image_path in image_paths:
        count += 1
        filename = os.path.basename(image_path)
        output_filename = filename.replace("first_find", "filtered")
        output_path = os.path.join(OUTPUT_VH_DESPECKLED, output_filename)
        image = GeoImageProcessor(image_path)

        h, w = image.data.shape

        if h > TILE_SIZE or w > TILE_SIZE:
            image.data = filter_large_image(image.data)
            print(f"cuenta = {count}")
        image.save(output_path)

        print(f"✅ Processed: {output_filename}")


def get_filtered_sentinel1_ascending_vv_cocorna():
    os.makedirs(OUTPUT_VV_DESPECKLED, exist_ok=True)
    image_paths = sorted(glob.glob(os.path.join(SENTINEL1_ASCENDING_VV_PATH, "*.tif")))
    count=0
    for image_path in image_paths:
        count += 1
        filename = os.path.basename(image_path)
        output_filename = filename.replace("first_find", "filtered")
        output_path = os.path.join(OUTPUT_VV_DESPECKLED, output_filename)
        image = GeoImageProcessor(image_path)

        h, w = image.data.shape

        if h > TILE_SIZE or w > TILE_SIZE:
            image.data = filter_large_image(image.data)
            print(f"cuenta = {count}")
        image.save(output_path)

        print(f"✅ Processed: {output_filename}")


def get_filtered_sentinel1_descending_vh_cocorna():
    os.makedirs(OUTPUT_VH_DESPECKLED, exist_ok=True)
    image_paths = sorted(glob.glob(os.path.join(SENTINEL1_VH_PATH, "*.tif")))
    count=0
    for image_path in image_paths:
        count += 1
        filename = os.path.basename(image_path)
        output_filename = filename.replace("first_find", "filtered")
        output_path = os.path.join(OUTPUT_VH_DESPECKLED, output_filename)
        image = GeoImageProcessor(image_path)

        h, w = image.data.shape

        if h > TILE_SIZE or w > TILE_SIZE:
            image.data = filter_large_image(image.data)
            print(f"cuenta = {count}")
        image.save(output_path)

        print(f"✅ Processed: {output_filename}")


def get_filtered_sentinel1_descending_vv_cocorna():
    os.makedirs(OUTPUT_VV_DESPECKLED, exist_ok=True)
    image_paths = sorted(glob.glob(os.path.join(SENTINEL1_VV_PATH, "*.tif")))
    count=0
    for image_path in image_paths:
        count += 1
        filename = os.path.basename(image_path)
        output_filename = filename.replace("first_find", "filtered")
        output_path = os.path.join(OUTPUT_VV_DESPECKLED, output_filename)
        image = GeoImageProcessor(image_path)

        h, w = image.data.shape

        if h > TILE_SIZE or w > TILE_SIZE:
            image.data = filter_large_image(image.data)
            print(f"cuenta = {count}")
        image.save(output_path)

        print(f"✅ Processed: {output_filename}")

if __name__ == "__main__":
    get_filtered_sentinel1_descending_vv_cocorna()
