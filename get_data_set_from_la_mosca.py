import time

from utils import *
import ee



ee.Authenticate()
ee.Initialize(project="investigation-project-pipe")


def get_landsat_data_set_from_la_mosca():
    """
    Retrieves and exports mean Landsat images of the La Mosca region for multiple date ranges.

    - Defines a region of interest (ROI) based on predefined coordinates.
    - Extracts Landsat 8 imagery for each date range from 2015 to 2024.
    - Computes the mean image for each period.
    - Exports each band separately to Google Drive (organized by filename).

    The exported files follow this naming convention:
    - File name: `la_mosca_mean_{start_date}_{end_date}`
    """

    dates = [(str(AAAA) + MM1, str(AAAA) + MM2) for AAAA in range(2024, 2025)
              for MM1, MM2 in zip(['-01-01', '-04-01', '-07-01', '-10-01'],
                                  ['-03-31', '-06-30', '-09-30', '-12-31'])]

    points_la_mosca = [[-75.3845077, 6.2052735],
                      [-75.3363690, 6.2052617],
                      [-75.3359859, 6.1513562],
                      [-75.3847079, 6.1515247]]

    roi_la_mosca = generate_roi_from_points(ee, points_la_mosca)

    collection_landsta_path = 'LANDSAT/LC08/C02/T1_L2'

    for date in dates:

        landsat_collection_la_mosca = get_satellite_collection(ee_client=ee,
                                                               collection_id=collection_landsta_path,
                                                               start=date[0],
                                                               end=date[1],
                                                               roi=roi_la_mosca)
        image = landsat_collection_la_mosca.map(mask_landsat_8sr).mean().clip(roi_la_mosca).reproject(crs='EPSG:4326',
                                                                                                      scale=30)
        for band in image.bandNames().getInfo():
            description = f"Mean image of La Mosca captured between {date[0]} and {date[1]}, using the {band} band."
            task = ee.batch.Export.image.toDrive(
                image=image.select(band),
                description=description,
                folder=band,
                fileNamePrefix=f"la_mosca_mean_{date[0]}_{date[1]}",
                region=roi_la_mosca.bounds().getInfo()['coordinates'],
                scale=30,
                crs='EPSG:4326',
                maxPixels=1e13
            )
            task.start()
            while task.active() and task.status().get('state') not in  ["FAILED", "CANCELLED"]:
                time.sleep(1)

if __name__ == '__main__':
    get_landsat_data_set_from_la_mosca()