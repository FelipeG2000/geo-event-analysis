import os
import cv2
import numpy as np
from collections import defaultdict
from process_data.process_images_tools import GeoImageProcessor

# Paths
NDVI_DIR = "/home/felipe/MiDrive/GEE_Exports/cocorna/sentinel2/processed/indices/ndvi"
NDBI_DIR = "/home/felipe/MiDrive/GEE_Exports/cocorna/sentinel2/processed/indices/ndbi"
NDWI_DIR = "/home/felipe/MiDrive/GEE_Exports/cocorna/sentinel2/processed/indices/ndwi"
OUTPUT_DIR = "multi_satellite_imagery_indices"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def preprocesar_imagen(imagen):
    imagen = imagen.astype(np.float32)
    imagen = cv2.medianBlur(imagen, 3)

    min_val = np.min(imagen)
    max_val = np.max(imagen)
    if max_val - min_val < 1e-5:
        imagen = np.zeros_like(imagen)
    else:
        imagen = (imagen - min_val) / (max_val - min_val)
        imagen = imagen ** 1.5
        imagen = (imagen * 255).clip(0, 255).astype(np.uint8)

    return imagen

# Extrae fecha desde el nombre (último bloque antes del .tif)
def extract_date(filename):
    parts = filename.split("_")
    return parts[-2] if len(parts) >= 2 else None  # ejemplo: '2018-10-01'

# Indexar archivos por fecha
ndvi_by_date = {extract_date(f): f for f in os.listdir(NDVI_DIR) if f.endswith(".tif")}
ndbi_by_date = {extract_date(f): f for f in os.listdir(NDBI_DIR) if f.endswith(".tif")}
ndwi_by_date = {extract_date(f): f for f in os.listdir(NDWI_DIR) if f.endswith(".tif")}

# Buscar fechas comunes
common_dates = set(ndvi_by_date) & set(ndbi_by_date) & set(ndwi_by_date)
print(f"📅 Fechas comunes encontradas: {len(common_dates)}")

for date in sorted(common_dates):
    print(f"🛰️ Procesando fecha: {date}")

    ndvi = GeoImageProcessor(os.path.join(NDVI_DIR, ndvi_by_date[date]))
    ndbi = GeoImageProcessor(os.path.join(NDBI_DIR, ndbi_by_date[date]))
    ndwi = GeoImageProcessor(os.path.join(NDWI_DIR, ndwi_by_date[date]))

    target_size = (ndvi.data.shape[1], ndvi.data.shape[0])  # (width, height)

    # Resize y convertir a uint8
    ndvi_data = preprocesar_imagen(ndvi.data)
    ndbi_data = preprocesar_imagen(cv2.resize(ndbi.data, target_size))
    ndwi_data = preprocesar_imagen(cv2.resize(ndwi.data, target_size))

    # Fusionar como RGB
    fused = cv2.merge([ndbi_data, ndvi_data, ndwi_data])

    output_filename = f"fusion_{date}.png"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    cv2.imwrite(output_path, fused)

    print(f"✅ Guardado: {output_path}")
