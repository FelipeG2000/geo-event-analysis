from utils import *
import time
import ee

ee.Authenticate()
ee.Initialize(project="investigation-project-pipe")


POINTS_SAN_CARLOS = [[-75.0174891, 6.2002711],
                    [-74.9691066, 6.2007604],
                    [-74.9686103, 6.1675056],
                    [-75.0172356, 6.1670877]]
ROI_SAN_CARLOS = generate_roi_from_points(ee, POINTS_SAN_CARLOS)

def get_landsat_data_set_from_san_carlos():
    dates = generate_date_ranges(2015, 2025)

    collection_landsta_path = 'LANDSAT/LC08/C02/T1_L2'
    for date in dates:

        landsat_collection_san_carlos = get_satellite_collection(ee_client=ee,
                                                               collection_id=collection_landsta_path,
                                                               start=date[0],
                                                               end=date[1],
                                                               roi=ROI_SAN_CARLOS)
        image = landsat_collection_san_carlos.map(mask_landsat_8sr).mean().clip(ROI_SAN_CARLOS).reproject(crs='EPSG:4326',
                                                                                                      scale=30)
        for band in image.bandNames().getInfo():
            print(f"processing the follow band {band} of san carlos image in this dates {date[0]}-{date[1]}")
            description = f"Mean image of San carlos captured between {date[0]} and {date[1]}, using the {band} band."
            task = ee.batch.Export.image.toDrive(
                image=image.select(band),
                description=description,
                folder=band,
                fileNamePrefix=f"San_carlos_mean_{date[0]}_{date[1]}",
                region=ROI_SAN_CARLOS.bounds().getInfo()['coordinates'],
                scale=30,
                crs='EPSG:4326',
                maxPixels=1e13
            )
            task.start()
            while task.active():
                status = task.status()
                state = status.get('state')

                if state == "FAILED":
                    print(f"Error: {status.get('error_message')}")
                    break
                elif state == "CANCELLED":
                    print("The export task was cancelled.")
                    break

                time.sleep(1)


def get_landsat_visualisation_data_set_from_san_carlos():
    """
    Retrieves and exports mean Landsat images of the La Mosca region for multiple date ranges.

    - Defines a region of interest (ROI) based on predefined coordinates.
    - Extracts Landsat 8 imagery for each date range from 2015 to 2024.
    - Computes the mean image for each period.
    - Exports each band separately to Google Drive (organized by filename).

    The exported files follow this naming convention:
    - File name: `san_carlos_mean_{start_date}_{end_date}`
    """

    dates = generate_date_ranges(2019, 2025)

    collection_landsta_path = 'LANDSAT/LC08/C02/T1_L2'

    for date in dates:

        landsat_collection_san_carlos = get_satellite_collection(ee_client=ee,
                                                               collection_id=collection_landsta_path,
                                                               start=date[0],
                                                               end=date[1],
                                                               roi=ROI_SAN_CARLOS)
        image = landsat_collection_san_carlos.map(mask_landsat_8sr).mean().clip(ROI_SAN_CARLOS).reproject(crs='EPSG:4326',
                                                                                                      scale=30)
        for band in filter_landsat8_sr_st_bands(image.bandNames().getInfo()):
            print(f"processing the follow band {band} of san carlos image in this dates {date[0]}-{date[1]}")
            description = f"Mean image of San Carlos captured between {date[0]} and {date[1]}, using the {band} band."
            visualization = get_landsat8_visualization_params(band)
            task = ee.batch.Export.image.toDrive(
                image=image.select(band).visualize(**visualization),
                description=description,
                folder=f'{band}',
                fileNamePrefix=f"san_carlos_mean_{date[0]}_{date[1]}",
                region=ROI_SAN_CARLOS.bounds().getInfo()['coordinates'],
                scale=30,
                crs='EPSG:4326',
                maxPixels=1e13
            )
            task.start()
            while task.active():
                status = task.status()
                state = status.get('state')

                if state == "FAILED":
                    print(f"Error: {status.get('error_message')}")
                    break
                elif state == "CANCELLED":
                    print("The export task was cancelled.")
                    break

                time.sleep(1)


if __name__ == '__main__':
    get_landsat_visualisation_data_set_from_san_carlos()