import os
from datetime import datetime
from collections import defaultdict

import cv2
import numpy as np

from process_data.process_images_tools import GeoImageProcessor

NDVI_DIR = "/home/felipe/MiDrive/GEE_Exports/san_carlos/sentinel2/processed/indices/ndvi"
NDBI_DIR = "/home/felipe/MiDrive/GEE_Exports/san_carlos/sentinel2/processed/indices/ndbi"
SENTINEL1_VH_PATH = "/home/felipe/MiDrive/GEE_Exports/san_carlos/sentinel1/descending/VH/VH_despeckled"


def preprocesar_imagen(imagen):
    imagen = imagen.astype(np.float32)
    imagen = cv2.medianBlur(imagen, 3)
    min_val, max_val = np.min(imagen), np.max(imagen)
    if max_val - min_val < 1e-5:
        imagen = np.zeros_like(imagen)
    else:
        imagen = (imagen - min_val) / (max_val - min_val)
        imagen = imagen ** 1.5  # realce de contraste
        imagen = (imagen * 255).clip(0, 255).astype(np.uint8)
    return imagen


# Extrae año y mes del filename (penúltimo campo con formato YYYY-MM-DD)
def extract_year_month(filename):
    try:
        parts = filename.split('_')
        date_str = parts[-2]  # e.g., '2018-05-01'
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.year, date.month
    except:
        return None, None

# Indexar imágenes Sentinel-1 por (año, mes)
vh_files = sorted(os.listdir(SENTINEL1_VH_PATH))
vh_by_month = defaultdict(list)

for vh in vh_files:
    year, month = extract_year_month(vh)
    if year and month:
        vh_by_month[(year, month)].append(vh)

# Construir pares
pairs = []
ndvi_files = sorted(os.listdir(NDVI_DIR))
ndbi_files = sorted(os.listdir(NDBI_DIR))

for ndvi_file, ndbi_file in zip(ndvi_files, ndbi_files):
    year, month = extract_year_month(ndvi_file)
    if (year, month) and (year, month) in vh_by_month:
        vh_candidates = vh_by_month[(year, month)]
        if vh_candidates:
            best_vh = vh_candidates[0]
            pairs.append({
                "ndvi": ndvi_file,
                "ndbi": ndbi_file,
                "vh": best_vh
            })

print(f"Total de pares encontrados: {pairs}")


def multi_satellite_imagery():
    for pair in pairs:
        print(f"Voy en esta imagen {pair['ndbi'].split('.')[0][-21:]}")
        ndbi_image = GeoImageProcessor(f"{NDBI_DIR}/{pair['ndbi']}")
        ndvi_image = GeoImageProcessor(f"{NDVI_DIR}/{pair['ndvi']}")
        vh_image = GeoImageProcessor(f"{SENTINEL1_VH_PATH}/{pair['vh']}")

        target_size = (ndvi_image.data.shape[1], ndvi_image.data.shape[0])  # (width, height)

        ndvi_data = preprocesar_imagen(ndvi_image.data)
        ndbi_data = preprocesar_imagen(cv2.resize(ndbi_image.data, target_size))
        vh_data   = preprocesar_imagen(cv2.resize(vh_image.data, target_size)) # Escala la Sentinel-1

        ndbi_data = cv2.resize(ndbi_data, target_size)
        vh_data = cv2.resize(vh_data, target_size)

        # Asegura dtype uint8
        ndvi_data = ndvi_data.astype(np.uint8)
        ndbi_data = ndbi_data.astype(np.uint8)
        vh_data = vh_data.astype(np.uint8)

        # Combina como RGB
        indices = cv2.merge([ndbi_data, ndvi_data, vh_data])

        # Guarda y muestra
        cv2.imwrite(
            f'multi_satellite_imagery_alto_contraste_con_SAR/multi_satellite_fusion_{pair["ndbi"].split(".")[0][-21:]}.png', indices)


multi_satellite_imagery()