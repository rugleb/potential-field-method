# pylint: disable=C0103,W0613,R0201

from pathlib import Path
from typing import Dict, List

import attr
from marshmallow import EXCLUDE, Schema, fields, post_load

__all__ = (
    "Point",
    "PointSchema",
    "Polygon",
    "PolygonSchema",
    "Space",
    "SpaceSchema",
)


@attr.s(slots=True, frozen=True)
class Point:
    x: int = attr.ib()
    y: int = attr.ib()


@attr.s(slots=True, frozen=True)
class Polygon(Point):
    vertices: List[Point] = attr.ib()


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


class PointSchemaMixin:
    x = fields.Int(required=True)
    y = fields.Int(required=True)


class PointSchema(PointSchemaMixin, ExcludeSchema):

    @post_load
    def release(self, data: Dict, **kwargs) -> Point:
        return Point(**data)


class PolygonSchema(PointSchemaMixin, ExcludeSchema):
    vertices = fields.Nested(PointSchema, many=True, required=True)

    @post_load
    def release(self, data: Dict, **kwargs) -> Polygon:
        return Polygon(**data)


class SpaceSchema(ExcludeSchema):
    start = fields.Nested(PointSchema, required=True)
    finish = fields.Nested(PointSchema, required=True)
    polygons = fields.Nested(PolygonSchema, many=True, required=True)

    @post_load
    def release(self, data: Dict, **kwargs) -> Space:
        return Space(**data)
