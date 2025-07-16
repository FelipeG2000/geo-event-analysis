import os
import glob

from process_data.process_images_tools import (GeoImageProcessor, calculate_index, scale_to_8bit, BASEPATH, NDWI_DIR,
                                               NDVI_DIR, NDBI_DIR, TILE_SIZE, filter_large_image, OUTPUT_VV_DESPECKLED,
                                               OUTPUT_VH_DESPECKLED)
import matplotlib.pyplot as plt
import cv2
import numpy as np

BASEPATH_LANDSAT8 = f"{BASEPATH}/la_mosca/landsat8/bands/"
BASEPATH_SENTINEL2 = f"{BASEPATH}/la_mosca/sentinel2/bands/"
NDVI_DIR = f"{BASEPATH}la_mosca/sentinel2/processed/indices/ndvi"
NDBI_DIR = f"{BASEPATH}la_mosca/sentinel2/processed/indices/ndbi"
NDWI_DIR = f"{BASEPATH}la_mosca/sentinel2/processed/indices/ndwi"
SENTINEL1_VV_PATH = "/home/felipe/MiDrive/GEE_Exports/la_mosca/sentinel1/descending/VV"
SENTINEL1_VH_PATH = "/home/felipe/MiDrive/GEE_Exports/la_mosca/sentinel1/descending/VH"
SENTINEL1_ASCENDING_VV_PATH = "/home/felipe/MiDrive/GEE_Exports/la_mosca/sentinel1/ascending/VV"
SENTINEL1_ASCENDING_VH_PATH = "/home/felipe/MiDrive/GEE_Exports/la_mosca/sentinel1/ascending/VH"

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


def get_ndbi_la_mosca_sentinel2():
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

        ndbi = calculate_index(geo_b6.data, geo_b5.data)
        geo_b6.data = scale_to_8bit(ndbi)
        geo_b6.save(output_path)

        print(f"Processed Landsat 8 NDBI: {output_filename}")


def get_filtered_sentinel1_descending_vv_la_mosca():
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


def get_filtered_sentinel1_ascending_vv_la_mosca():
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


def get_filtered_sentinel1_ascending_vh_la_mosca():
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


def get_filtered_sentinel1_descending_vh_la_mosca():
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


def experimento_interesante():
    ndvi = GeoImageProcessor(f"{NDVI_DIR}/la_mosca_ndvi_2018-10-01_2018-12-31.tif")
    ndbi = GeoImageProcessor(f"{NDWI_DIR}/la_mosca_ndbi_2018-10-01_2018-12-31.tif")
    vv = GeoImageProcessor("VV/la_mosca_filtered_2017-05-01_2017-05-31.tif")

    # Asegura que todos tengan el mismo tamaño -> usa ndvi como referencia
    target_size = (ndvi.data.shape[1], ndvi.data.shape[0])  # (width, height)

    ndvi_data = ndvi.data
    ndbi_data = ndbi.data
    vv_data = vv.data  # Escala la Sentinel-1

    # Si hace falta, reescala tamaños:
    ndbi_data = cv2.resize(ndbi_data, target_size)
    vv_data = cv2.resize(vv_data, target_size)

    # Asegura dtype uint8
    ndvi_data = ndvi_data.astype(np.uint8)
    ndbi_data = ndbi_data.astype(np.uint8)
    vv_data = vv_data.astype(np.uint8)

    # Combina como RGB
    indices = cv2.merge([ndbi_data, ndvi_data, vv_data])

    # Guarda y muestra
    cv2.imwrite('indices.png', indices)
    plt.imshow(indices)
    plt.show()

if __name__ == "__main__":
    get_filtered_sentinel1_ascending_vh_la_mosca()

