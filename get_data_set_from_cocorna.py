from utils import *
import ee

ee.Authenticate()
ee.Initialize(project="investigation-project-pipe")


POINTS_COCORNA = [[-75.205, 6.108],
                  [-75.160, 6.108],
                  [-75.205, 6.062],
                  [-75.160, 6.062]]

ROI_COCORNA = generate_roi_from_points(ee, POINTS_COCORNA)


def get_landsat_data_set_from_cocorna():
    dates = [(str(AAAA) + MM1, str(AAAA) + MM2) for AAAA in range(2015, 2025)
             for MM1, MM2 in zip(['-01-01', '-04-01', '-07-01', '-10-01'],
                                 ['-03-31', '-06-30', '-09-30', '-12-31'])]

    collection_landsat_path = 'LANDSAT/LC08/C02/T1_L2'
    for date in dates:

        landsat_collection_cocorna = get_satellite_collection(ee_client=ee,
                                                               collection_id=collection_landsat_path,
                                                               start=date[0],
                                                               end=date[1],
                                                               roi=ROI_COCORNA)
        image = landsat_collection_cocorna.map(mask_landsat_8sr).mean().clip(ROI_COCORNA).reproject(crs='EPSG:4326',
                                                                                                      scale=30)
        for band in image.bandNames().getInfo():
            print(f"processing the follow band {band} of Cocorna image in this dates {date[0]}-{date[1]}")
            description = f"Mean image of Cocorna captured between {date[0]} and {date[1]}, using the {band} band."
            task = ee.batch.Export.image.toDrive(
                image=image.select(band),
                description=description,
                folder=band,
                fileNamePrefix=f"cocorna_mean_{date[0]}_{date[1]}",
                region=ROI_COCORNA.bounds().getInfo()['coordinates'],
                scale=30,
                crs='EPSG:4326',
                maxPixels=1e13
            )
            task.start()
            monitor_task(task)


def get_landsat_visualisation_data_set_from_cocorna():
    """
    Retrieves and exports mean visualized Landsat images of the Cocorna region for multiple date ranges.

    - Defines a region of interest (ROI) based on predefined coordinates.
    - Extracts Landsat 8 imagery for each date range from 2015 to 2024.
    - Computes the mean image for each period.
    - Exports each band separately to Google Drive (organized by filename).

    The exported files follow this naming convention:
    - File name: `cocorna_mean_{start_date}_{end_date}`
    """

    dates = generate_date_ranges(2023, 2025)

    collection_landsta_path = 'LANDSAT/LC08/C02/T1_L2'

    for date in dates:

        landsat_collection_cocorna = get_satellite_collection(ee_client=ee,
                                                               collection_id=collection_landsta_path,
                                                               start=date[0],
                                                               end=date[1],
                                                               roi=ROI_COCORNA)
        image = landsat_collection_cocorna.map(mask_landsat_8sr).mean().clip(ROI_COCORNA).reproject(crs='EPSG:4326',
                                                                                                      scale=30)
        for band in filter_landsat8_sr_st_bands(image.bandNames().getInfo()):
            print(f"processing the follow band {band} of Cocorna image in this dates {date[0]}-{date[1]}")
            description = f"Mean image of Cocorna captured between {date[0]} and {date[1]}, using the {band} band."
            visualization = get_landsat8_visualization_params(band)
            task = ee.batch.Export.image.toDrive(
                image=image.select(band).visualize(**visualization),
                description=description,
                folder=f'{band}',
                fileNamePrefix=f"cocorna_mean_{date[0]}_{date[1]}",
                region=ROI_COCORNA.bounds().getInfo()['coordinates'],
                scale=30,
                crs='EPSG:4326',
                maxPixels=1e13
            )
            task.start()
            monitor_task(task)


def get_sentinel2_data_set_from_cocorna():
    """
    Retrieves and exports mean Landsat images of the Cocorna region for multiple date ranges.

    - Defines a region of interest (ROI) based on predefined coordinates.
    - Extracts sentinel 2 imagery for each date range from 2018 to 2024.
    - Computes the mean image for each period.
    - Exports each band separately to Google Drive (organized by filename).

    The exported files follow this naming convention:
    - File name: `cocorna_mean_{start_date}_{end_date}`
    """

    dates = generate_date_ranges(2018, 2025)

    collection_sentinel2_path = "COPERNICUS/S2_SR_HARMONIZED"

    for date in dates:

        sentinel2_collection_cocorna = get_satellite_collection(ee_client=ee, collection_id=collection_sentinel2_path,
                                                                 start=date[0], end=date[1], roi=ROI_COCORNA)
        image = sentinel2_collection_cocorna.map(mask_sentinel2_sr).mean().clip(ROI_COCORNA).reproject(crs='EPSG:4326',
                                                                                                         scale=10)
        for band in image.bandNames().getInfo():
            print(f"processing the follow band {band} of Cocorna image in this dates {date[0]}-{date[1]}")
            description = f"Mean image cocorna {date[0]} to {date[1]} using {band} band"
            task = ee.batch.Export.image.toDrive(
                image=image.select(band),
                description=description,
                folder=band,
                fileNamePrefix=f"cocorna_mean_{date[0]}_{date[1]}",
                region=ROI_COCORNA.bounds().getInfo()['coordinates'],
                scale=10,
                crs='EPSG:4326',
                maxPixels=1e13
            )
            task.start()
            monitor_task(task)


if __name__ == '__main__':
    get_sentinel2_data_set_from_cocorna()