import pyproj
import pytest
from shapely.geometry import LinearRing, LineString, Point, Polygon
from shapely.geometry.base import BaseGeometry

from geoshapely import ops
from geoshapely.geoshape import GeoLinearRing, GeoLineString, GeoPoint, GeoPolygon


def test_make_geoshape_from_geom():
    crs = pyproj.CRS.from_string("epsg:4326")

    # Test supported types
    point = Point(1, 1)
    geopoint = ops.make_geoshape_from_geom(point, crs)
    assert isinstance(geopoint, GeoPoint)
    assert geopoint.crs == crs

    linestring = LineString([[0, 0], [1, 0], [1, 1]])
    geolinestring = ops.make_geoshape_from_geom(linestring, crs)
    assert isinstance(geolinestring, GeoLineString)
    assert geolinestring.crs == crs

    polygon = Polygon(((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0)))
    geopolygon = ops.make_geoshape_from_geom(polygon, crs)
    assert isinstance(geopolygon, GeoPolygon)
    assert geopolygon.crs == crs

    linearring = LinearRing(((0, 0), (0, 1), (1, 1), (1, 0)))
    geolinearring = ops.make_geoshape_from_geom(linearring, crs)
    assert isinstance(geolinearring, GeoLinearRing)
    assert geolinearring.crs == crs

    # TODO add multigeoms

    # Test incompatible and unsupported types
    class NotAGeom:
        pass

    incompat_class = NotAGeom()
    with pytest.raises(TypeError):
        ops.make_geoshape_from_geom(incompat_class, crs)

    class WeirdShape(BaseGeometry):
        pass

    weird_shape = WeirdShape()
    with pytest.raises(TypeError):
        ops.make_geoshape_from_geom(weird_shape, crs)

    # Test that geoshapes can be passed in
    ops.make_geoshape_from_geom(geopoint, crs)
