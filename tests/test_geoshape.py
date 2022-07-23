import pyproj
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry

from geoshapely.geoshape import GeoBaseGeometry, GeoPoint


def test_geopoint():
    test_coords = (-1, 1)
    test_crs = pyproj.CRS.from_string("epsg:4326")

    test_geopoint = GeoPoint(test_coords, crs=test_crs)
    assert (test_geopoint.x, test_geopoint.y) == test_coords
    assert test_geopoint.crs == test_crs

    test_coords = (-1, 0, 1)
    test_geopoint = GeoPoint(*test_coords, crs=test_crs)
    assert test_geopoint.coords[0] == test_coords
    assert test_geopoint.crs == test_crs

    test_geopoint = GeoPoint(test_coords)
    assert test_geopoint.coords[0] == test_coords
    assert test_geopoint.crs is None

    test_geopoint = GeoPoint(*test_coords)
    assert test_geopoint.coords[0] == test_coords
    assert test_geopoint.crs is None

    assert isinstance(test_geopoint, GeoBaseGeometry)
    assert isinstance(test_geopoint, Point)
    assert isinstance(test_geopoint, BaseGeometry)
