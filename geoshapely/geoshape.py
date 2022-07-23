from typing import Optional

import pyproj
from shapely.geometry import (
    LinearRing,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)

SHAPELY_GEOMS = [
    Point,
    Polygon,
    LineString,
    LinearRing,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
]


class GeoBaseGeometry:
    def __init__(self, crs: Optional[pyproj.CRS]) -> None:
        self._crs = crs

    @property
    def crs(self) -> Optional[pyproj.CRS]:
        return self._crs


class GeoPoint(GeoBaseGeometry, Point):
    def __init__(self, *args, crs: Optional[pyproj.CRS] = None, **kwargs) -> None:
        GeoBaseGeometry.__init__(self, crs=crs)
        Point.__init__(self, *args, **kwargs)

    def test_method(self) -> None:
        return self.crs
