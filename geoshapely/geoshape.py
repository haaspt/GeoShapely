from copy import deepcopy
from typing import Any, Optional, TypeVar

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
from shapely.ops import transform

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
    def __init__(self, crs: Optional[Any]) -> None:
        self._crs = self._parse_crs(crs)

    def _parse_crs(self, crs: Any) -> Optional[pyproj.CRS]:
        if isinstance(crs, GeoShapeType):
            # Users can pass in a GeoShape
            return crs.crs
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

    def to_crs(
        self: GeoShapeType,
        crs: Any,
        transformer: Optional[pyproj.Transformer] = None,
    ) -> GeoShapeType:
        if transformer and transformer.source_crs != self.crs:
            raise ValueError(
                "Incompatible pyproj.Transformer."
                f"Transfromer has source crs of {transformer.source_crs} but \
                geom has crs of {self.crs}."
            )
        if self.crs is None:
            return self.set_crs(crs)
        crs = self._parse_crs(crs)
        if not transformer:
            transformer = pyproj.Transformer.from_crs(self._crs, crs)
        transform_func = transformer.transform
        result = deepcopy(self)
        result = transform(transform_func, result)
        result._crs = crs
        return result


class GeoPoint(GeoBaseGeometry, Point):
    def __init__(self, *args, crs: Optional[Any] = None, **kwargs) -> None:
        GeoBaseGeometry.__init__(self, crs=crs)
        Point.__init__(self, *args, **kwargs)


class GeoPolygon(GeoBaseGeometry, Polygon):
    def __init__(self, *args, crs: Optional[Any] = None, **kwargs) -> None:
        GeoBaseGeometry.__init__(self, crs=crs)
        Polygon.__init__(self, *args, **kwargs)


class GeoLineString(GeoBaseGeometry, LineString):
    def __init__(self, *args, crs: Optional[Any] = None, **kwargs) -> None:
        GeoBaseGeometry.__init__(self, crs=crs)
        LineString.__init__(self, *args, **kwargs)


class GeoLinearRing(GeoBaseGeometry, LinearRing):
    def __init__(self, *args, crs: Optional[Any] = None, **kwargs) -> None:
        GeoBaseGeometry.__init__(self, crs=crs)
        LinearRing.__init__(self, *args, **kwargs)


# TODO add multipolygons
