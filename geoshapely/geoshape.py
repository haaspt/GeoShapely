from __future__ import annotations

from copy import deepcopy
from typing import Any, Optional, TypeVar, Union

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


GeoShapeType = TypeVar("GeoShapeType", bound="GeoBaseGeometry")


class GeoBaseGeometry:
    def __init__(self, crs: Optional[Union[pyproj.CRS, str]]) -> None:
        self._crs = self._parse_crs(crs)

    def _parse_crs(self, crs: Any) -> Optional[pyproj.CRS]:
        if crs is None:
            return crs
        elif isinstance(crs, pyproj.CRS):
            return crs
        else:
            # Attempt to generate CRS from other input
            return pyproj.CRS.from_user_input(crs)

    @property
    def crs(self) -> Optional[pyproj.CRS]:
        return self._crs

    def set_crs(
        self: GeoShapeType, crs: Any, inplace: bool = False, allow_override: bool = False
    ) -> GeoShapeType:
        crs = self._parse_crs(crs)
        if self.crs is not None and not allow_override and self.crs != crs:
            raise ValueError(
                "Geometry already has a CRS that does not match the passed CRS."
                "Specify 'allow_override=True' to allow replacing the existing "
                "CRS without doing any transformation. Use `.to_crs()` to transform the "
                "geometry instead."
            )
        if not inplace:
            result = deepcopy(self)
        else:
            result = self
        result._crs = crs
        return result


class GeoPoint(GeoBaseGeometry, Point):
    def __init__(self, *args, crs: Optional[Union[pyproj.CRS, str]] = None, **kwargs) -> None:
        GeoBaseGeometry.__init__(self, crs=crs)
        Point.__init__(self, *args, **kwargs)
