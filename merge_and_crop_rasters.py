"""
This script merges two raster files (GeoTIFF) in WGS84 format
and crops the result to a specified bounding box.
It uses rasterio for merging and cropping.
"""

import rasterio
from rasterio.merge import merge
from rasterio.windows import from_bounds as window_from_bounds
from rasterio.windows import transform as window_transform

# === Configuration ===
raster_path1 = "aa1.tif"
raster_path2 = "aa2.tif"
output_path = "merged_cropped_raster.tif"

# Bounding box in WGS84 (west, south, east, north)
west, south, east, north = 38.639904, 8.8331149, 38.9080529, 9.0985761 # Addis Ababa

# === Load and merge the rasters ===
src1 = rasterio.open(raster_path1)
src2 = rasterio.open(raster_path2)
mosaic, out_transform = merge([src1, src2])

# === Create crop window based on bounding box ===
window = window_from_bounds(west, south, east, north, out_transform)
window = window.round_offsets().round_lengths()

# === Crop the merged raster ===
cropped = mosaic[:, window.row_off:window.row_off + window.height,
                 window.col_off:window.col_off + window.width]

# === Compute transform for the cropped window ===
cropped_transform = window_transform(window, out_transform)

# === Update metadata for the cropped raster ===
out_meta = src1.meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": cropped.shape[1],
    "width": cropped.shape[2],
    "transform": cropped_transform,
    "count": cropped.shape[0]
})


# === Save the cropped raster ===
with rasterio.open(output_path, "w", **out_meta) as dest:
    dest.write(cropped)

# === Clean up ===
src1.close()
src2.close()