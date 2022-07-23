from typing import Any, Optional, Union

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
    def __init__(self, crs: Optional[Union[pyproj.CRS, str]]) -> None:
        self._crs = self._init_crs(crs)

    def _init_crs(self, crs: Any) -> Optional[pyproj.CRS]:
        if crs is None:
            return crs
        elif isinstance(crs, pyproj.CRS):
            return crs
        elif isinstance(crs, str):
            # Attempt to generate CRS from string
            return pyproj.CRS.from_string(crs)
        else:
            raise TypeError(f"crs must be a pyproj.CRS or valid CRS string, got {type(crs)}.")

    @property
    def crs(self) -> Optional[pyproj.CRS]:
        return self._crs


class GeoPoint(GeoBaseGeometry, Point):
    def __init__(self, *args, crs: Optional[Union[pyproj.CRS, str]] = None, **kwargs) -> None:
        GeoBaseGeometry.__init__(self, crs=crs)
        Point.__init__(self, *args, **kwargs)

    def test_method(self) -> None:
        return self.crs
