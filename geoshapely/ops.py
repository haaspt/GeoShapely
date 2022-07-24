from copy import deepcopy
from typing import Any, Optional

from shapely.geometry import LinearRing, LineString, Point, Polygon
from shapely.geometry.base import BaseGeometry

from .geoshape import GeoBaseGeometry, GeoLinearRing, GeoLineString, GeoPoint, GeoPolygon


def make_geoshape_from_geom(
    shapely_geom: BaseGeometry, crs: Optional[Any] = None
) -> GeoBaseGeometry:
    if isinstance(shapely_geom, GeoBaseGeometry):
        # Just create a copy if a GeoShape is passed it back
        result = deepcopy(shapely_geom)
        if result.crs:
            result = result.to_crs(crs=crs)
        else:
            result = shapely_geom.set_crs(crs)
    elif isinstance(shapely_geom, Point):
        result = GeoPoint(shapely_geom, crs=crs)
    elif isinstance(shapely_geom, LineString):
        result = GeoLineString(shapely_geom, crs=crs)
    elif isinstance(shapely_geom, Polygon):
        result = GeoPolygon(shapely_geom, crs=crs)
    elif isinstance(shapely_geom, LinearRing):
        result = GeoLinearRing(shapely_geom, crs=crs)
    # TODO add multigeoms
    return result
