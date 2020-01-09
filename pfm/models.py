# pylint: disable=C0103,W0613,R0201

from abc import ABC
from pathlib import Path
from typing import Dict, List

import attr
from marshmallow import EXCLUDE, Schema, fields, post_load
from shapely import geometry

__all__ = (
    "Point",
    "PointSchema",
    "Polygon",
    "PolygonSchema",
    "Space",
    "SpaceSchema",
)


class Point(geometry.Point):

    def __add__(self, other: geometry.Point) -> "Point":
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __sub__(self, other: geometry.Point) -> "Point":
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)

    def __mul__(self, other: float) -> "Point":
        x = self.x * other
        y = self.y * other
        return Point(x, y)

    def __truediv__(self, other: float) -> "Point":
        x = self.x / other
        y = self.y / other
        return Point(x, y)


class Polygon(geometry.Polygon, ABC):  # pylint: disable=W0223
    pass


@attr.s(slots=True, frozen=True)
class Space:
    start: Point = attr.ib()
    finish: Point = attr.ib()
    polygons: List[Polygon] = attr.ib()

    @classmethod
    def form_file(cls, path: Path) -> "Space":
        text = path.read_text()
        return SpaceSchema().loads(text)


class ExcludeSchema(Schema):

    class Meta:
        unknown = EXCLUDE


class PointSchema(ExcludeSchema):
    x = fields.Int(required=True)
    y = fields.Int(required=True)

    @post_load
    def release(self, data: Dict, **kwargs) -> Point:
        x = data.pop("x")
        y = data.pop("y")
        return Point(x, y)


class PolygonSchema(ExcludeSchema):
    vertices = fields.Nested(PointSchema, many=True, required=True)

    @post_load
    def release(self, data: Dict, **kwargs) -> Polygon:
        coords = []
        for point in data.pop("vertices"):
            coords.append((point.x, point.y))
        return Polygon(coords)


class SpaceSchema(ExcludeSchema):
    start = fields.Nested(PointSchema, required=True)
    finish = fields.Nested(PointSchema, required=True)
    polygons = fields.Nested(PolygonSchema, many=True, required=True)

    @post_load
    def release(self, data: Dict, **kwargs) -> Space:
        return Space(**data)
