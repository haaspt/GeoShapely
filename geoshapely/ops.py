from copy import deepcopy
from typing import Any, Optional

from shapely.geometry import LinearRing, LineString, Point, Polygon
from shapely.geometry.base import BaseGeometry

from .geoshape import GeoBaseGeometry, GeoLinearRing, GeoLineString, GeoPoint, GeoPolygon


def make_geoshape_from_geom(
    shapely_geom: BaseGeometry, crs: Optional[Any] = None
) -> GeoBaseGeometry:
    """Create a GeoShape instance of a Shapely geometry.

    This convenience function takes in an instance of any Shapely geom and returns
    its GeoShape equivalent. e.g.:
        Point -> GeoPoint
        Polygon -> GeoPolygon

    Optionally, a CRS can be specified, which will be associated with the new GeoShape.

    Parameters
    ----------
    shapely_geom:
        An instance of any Shapely geometry that derives from BaseGeometry.
        If a GeoShape is passed in, a copy is returned, converted to the specified
        CRS, if one was set.
    crs: (Optional)
        A CRS to be associated with the new GeoShape.
        See `pyproj.CRS.from_user_input()` for information on allowable types.

    Returns
    -------
    A new instance of the Geo-equivalent of the Shapely geom passed in

    Raises
    ------
    TypeError:
        If `shapely_geom` is not derived from BaseGeometry or if no equivalent GeoShape
        can be identified.
    """
    if not isinstance(shapely_geom, BaseGeometry):
        raise TypeError(
            f"`shapely_geom` must be an instance of Shapely geometry \
            derived from `BaseGeometry`, cannot convert value of type {type(shapely_geom)}"
        )
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
    else:
        return TypeError(
            f"No suitable Geo-equivalent exists for value of type {type(shapely_geom)}"
        )
    return result
