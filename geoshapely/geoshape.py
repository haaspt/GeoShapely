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
    """The base class for all GeoShape classes.

    Contains CRS handling properties and methods that are merged with Shapely geoms
    to create the various child classes (GeoPoint, GeoPolygon, etc.)

    All GeoShapes are simple Shapely geometries with the ability to store CRS
    information and perform CRS conversions on themselves.
    """

    def __init__(self, crs: Optional[Any]) -> None:
        self._crs = self._parse_crs(crs)

    def _parse_crs(self, crs: Optional[Any]) -> Optional[pyproj.CRS]:
        """Parse and return a pyproj.CRS, or None, from any input.

        If anything other than a GeoShape, pyproj.CRS, or None are passed in, the value
        will be passed to `pyproj.CRS.from_user_input()`. That method is capable of
        parsing a wide variety of CRS representations, including str and int types.
        See pyproj docs for further details.

        Parameters
        ----------
        crs:
            An optional CRS representation. Can be a pyproj.CRS, any instance
            of a GeoShape, any value parsable by pyproj.CRS.from_user_input,
            or None.

        Returns
        -------
        A pyproj.CRS or None
        """
        if crs is None:
            return crs
        elif isinstance(crs, GeoBaseGeometry):
            # Users can pass in a GeoShape
            return crs.crs
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
        """Assign a CRS to a GeoShape instance.

        No transformation/re-projection takes place. To convert from one CRS to another,
        see `.to_crs()`.

        Typically, this is only desired on shapes that have a CRS equal to None.
        Attempting  to set the CRS of an object that already has a CRS will result
        in a ValueError being thrown by default. This can be overridden by setting
        `allow_override` to True.

        By default a new object is returned, but inplace setting is possible as well.

        Parameters
        ----------
        crs:
            The CRS value to assign to the GeoShape.
        inplace:
            If True the shape is modified inplace, if False a copy is created.
            (Default: False)
        allow_override:
            If True users can override the current CRS value associated with a shape.
            No transformation of the underlying geometry is carried out.
            If False then a ValueError is raised if a user attempts to assign a CRS
            to a shape that already has one.
            (Default: False)

        Returns
        -------
        Either a new instance of the GeoShape with the new CRS set, or the original
        instance with the new CRS, depending on if `inplace` was set True or not.

        Raises
        ------
        ValueError:
            If allow_override is False and the object already has a CRS different from
            the one passed into this function.
        """
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
        """Transfrom the GeoShape from one CRS to another.

        Given a CRS value, the shape will be converted using Shapely's `transform`
        operation in combination with pyproj's `Transformer` class.

        A new instance of the shape is returned, reprojected to the desired CRS.

        Note that by default, `to_crs()` creates a new pyproj.Transformer each time
        it's called. This can be slow when mass-converting a large number of objects.
        Users can create their own Transformer once and then pass it into this method
        to optimize the process. Also consider using GeoPandas for bulk geometry and
        conversion handling.

        Parameters
        ----------
        crs:
            A CRS value to transfrom the shape to. Can be any value parsable by any
            GeoShape class.
            Note that `.set_crs()` can be used to simply set the CRS on a GeoShape
            that doesn't already have one.
        transformer: (Optional)
            A pyproj.Transfromer instance, pre-created to optimize transformation of
            multiple GeoShapes.

        Returns
        -------
        A new instance of the original object, transformed to the new CRS.

        Raises
        ------
        ValueError:
            If a transformer is passed in but its source/target CRS params do not match
            the current or desired CRSes.
        """
        crs = self._parse_crs(crs)
        if transformer:
            if transformer.source_crs != self.crs:
                raise ValueError(
                    "Incompatible pyproj.Transformer."
                    f"Transfromer has source CRS of {transformer.source_crs} but \
                    geom has crs of {self.crs}."
                )
            if transformer.target_crs != crs:
                raise ValueError(
                    "Incompatible pyproj.Transformer."
                    f"Transfromer has target CRS of {transformer.target_crs} but \
                    desired target CRS is {self.crs}."
                )
        if self.crs is None:
            return self.set_crs(crs)
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
