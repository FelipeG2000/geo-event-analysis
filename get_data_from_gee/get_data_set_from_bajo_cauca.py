from utils import *
from config.ee_init import ee



ROI_BAJO_CAUCA = ee.Geometry.Rectangle(-74.746023, 8.037527, -74.8303614, 8.113206)

def get_sentinel1_descending_data_set_from_bajo_cauca():
    """
    Retrieves and exports mean Landsat images of the Bajo Cauca region for multiple date ranges.

    - Defines a region of interest (ROI) based on predefined coordinates.
    - Extracts sentinel 1 imagery for each date range from 2017 to 2024.
    - Filters imagery for descending orbit mode.
    - Computes the mean image for each period.
    - Exports each band separately to Google Drive (organized by filename).

    The exported files follow this naming convention:
    - File name: `bajo_cauca_first_{start_date}_{end_date}`
    """

    dates = generate_date_ranges(2017, 2025, 'monthly')

    collection_sentinel1_path = 'COPERNICUS/S1_GRD'

    for date in dates:
        sentinel1_collection_bajo_cauca = (
            get_satellite_collection(ee_client=ee, collection_id=collection_sentinel1_path,
                                     start=date[0], end=date[1], roi=ROI_BAJO_CAUCA)
            .filter(ee.Filter.eq('instrumentMode', 'IW'))
            .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
        )

        first_image = sentinel1_collection_bajo_cauca.first()

        if first_image.getInfo():
            image = first_image.clip(ROI_BAJO_CAUCA).reproject(crs='EPSG:4326', scale=10)
            bands = image.bandNames().getInfo()
            if "VV" in bands:
                print(f"Processing band VV for bajo cauca image ({date[0]} - {date[1]})")
                description = f"First image Bajo Cauca {date[0]} to {date[1]} using VV band"
                task = ee.batch.Export.image.toDrive(
                    image=image.select("VV").visualize(**{'min': -25, 'max': 5}),
                    description=description,
                    folder="temporal_folder_for_VV_images_of_bajo_cauca",
                    fileNamePrefix=f"bajo_cauca_first_find_{date[0]}_{date[1]}",
                    region=ROI_BAJO_CAUCA.bounds().getInfo()['coordinates'],
                    scale=10,
                    crs='EPSG:4326',
                    maxPixels=1e13
                )
                task.start()
                monitor_task(task)
        else:
            print(f"No Sentinel-1 images found for bajo cauca in date range {date[0]} - {date[1]}")


if __name__ == '__main__':
    get_sentinel1_descending_data_set_from_bajo_cauca()
