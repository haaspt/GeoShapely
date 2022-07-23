import pyproj
import pytest
from pyproj.exceptions import CRSError
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry

from geoshapely.geoshape import GeoBaseGeometry, GeoPoint


def test_geopoint():
    test_coords = (-1, 1)
    test_crs_string = "epsg:4326"
    test_crs = pyproj.CRS.from_string(test_crs_string)

    test_geopoint = GeoPoint(test_coords, crs=test_crs)
    assert (test_geopoint.x, test_geopoint.y) == test_coords
    assert test_geopoint.crs == test_crs

    # Confirm 3D points and unpacking both work
    test_coords = (-1, 0, 1)
    test_geopoint = GeoPoint(*test_coords, crs=test_crs)
    assert test_geopoint.z == test_coords[2]
    assert test_geopoint.coords[0] == test_coords
    assert test_geopoint.crs == test_crs

    # Test setting null CRS
    test_geopoint = GeoPoint(test_coords)
    assert test_geopoint.coords[0] == test_coords
    assert test_geopoint.crs is None

    test_geopoint = GeoPoint(*test_coords)
    assert test_geopoint.coords[0] == test_coords
    assert test_geopoint.crs is None

    # Test setting CRS by string
    test_geopoint = GeoPoint(test_coords, crs=test_crs_string)
    assert test_geopoint.crs == test_crs

    # Test type checking
    with pytest.raises(TypeError):
        GeoPoint(test_coords, crs=2)

    with pytest.raises(CRSError):
        GeoPoint(test_coords, crs="invalid")

    # Test inheritance
    assert isinstance(test_geopoint, GeoBaseGeometry)
    assert isinstance(test_geopoint, Point)
    assert isinstance(test_geopoint, BaseGeometry)
