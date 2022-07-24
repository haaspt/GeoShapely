import pyproj
import pytest
from pyproj.exceptions import CRSError
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry

from geoshapely.geoshape import GeoBaseGeometry, GeoLinearRing, GeoLineString, GeoPoint, GeoPolygon


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

    #  Test `.set_crs`
    test_geopoint = GeoPoint(test_coords, crs=None)
    set_geopoint = test_geopoint.set_crs(test_crs)
    assert set_geopoint.crs == test_crs
    # Confirm copy was returned
    assert set_geopoint.crs != test_geopoint.crs
    alt_crs = pyproj.CRS.from_string("epsg:3857")
    with pytest.raises(ValueError):
        set_geopoint.set_crs(alt_crs)
    set_geopoint.set_crs(alt_crs, inplace=True, allow_override=True)
    assert set_geopoint.crs == alt_crs

    # Test type checking
    with pytest.raises(CRSError):
        GeoPoint(test_coords, crs=2)

    with pytest.raises(CRSError):
        GeoPoint(test_coords, crs="invalid")

    # Test inheritance
    assert isinstance(test_geopoint, GeoBaseGeometry)
    assert isinstance(test_geopoint, Point)
    assert isinstance(test_geopoint, BaseGeometry)


def test_geolinestring():
    test_coords = [[0, 0], [1, 0], [1, 1]]
    test_crs_string = "epsg:4326"
    test_crs = pyproj.CRS.from_string(test_crs_string)
    geoline = GeoLineString(test_coords, crs=test_crs)
    assert geoline.length == 2


def test_geopolygon():
    test_coords = ((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0))
    test_crs_string = "epsg:4326"
    test_crs = pyproj.CRS.from_string(test_crs_string)
    geopoly = GeoPolygon(test_coords, crs=test_crs)
    assert geopoly.area == 1.0


def test_geolinearring():
    test_coords = ((0, 0), (0, 1), (1, 1), (1, 0))
    test_crs_string = "epsg:4326"
    test_crs = pyproj.CRS.from_string(test_crs_string)
    georing = GeoLinearRing(test_coords, crs=test_crs)
    assert georing.is_closed
    assert georing.length == 4.0
