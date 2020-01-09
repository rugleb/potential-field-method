import unittest
from typing import Any

from marshmallow import ValidationError
from shapely.geometry import Point, Polygon

from project import (
    Point,
    PointSchema,
    Polygon,
    PolygonSchema,
    Space,
    SpaceSchema,
    settings,
)


class PointTestCase(unittest.TestCase):

    def test_sum_method(self) -> None:
        p1 = Point(10, 20)
        p2 = Point(20, 30)

        p3 = p1 + p2
        self.assertEqual(p1.x + p2.x, p3.x)
        self.assertEqual(p1.y + p2.y, p3.y)

    def test_sub_method(self) -> None:
        p1 = Point(10, 30)
        p2 = Point(20, 30)

        p3 = p1 - p2
        self.assertEqual(p1.x - p2.x, p3.x)
        self.assertEqual(p1.y - p2.y, p3.y)

    def test_mul_method(self) -> None:
        p1 = Point(5, 5)
        scalar = 10

        p2 = p1 * scalar
        self.assertEqual(p1.x * scalar, p2.x)
        self.assertEqual(p1.y * scalar, p2.y)

    def test_div_method(self) -> None:
        p1 = Point(5, 5)
        scalar = 10

        p2 = p1 / scalar
        self.assertEqual(p1.x / scalar, p2.x)
        self.assertEqual(p1.y / scalar, p2.y)


class SchemaTestCase(unittest.TestCase):

    def assertDictEmpty(self, data: Any) -> None:
        self.assertDictEqual({}, data)


class PointSchemaTestCase(SchemaTestCase):
    schema = PointSchema()

    def test_with_valid_data(self) -> None:
        x, y = 10, 20

        data = {
            "x": x,
            "y": y,
        }

        point = self.schema.load(data)
        self.assertIsInstance(point, Point)

        self.assertEqual(x, point.x)
        self.assertEqual(y, point.y)

        self.assertDictEqual(data, self.schema.dump(point))

    def test_with_empty_data(self) -> None:
        data = {}

        try:
            PointSchema().load(data)
        except ValidationError as e:
            self.assertDictEmpty(e.valid_data)

            messages = {
                "x": ["Missing data for required field."],
                "y": ["Missing data for required field."],
            }
            self.assertDictEqual(messages, e.messages)

    def test_with_invalid_data(self) -> None:
        data = {
            "x": type,
            "y": type,
        }

        try:
            PointSchema().load(data)
        except ValidationError as e:
            self.assertDictEmpty(e.valid_data)

            messages = {
                "x": ["Not a valid integer."],
                "y": ["Not a valid integer."],
            }
            self.assertDictEqual(messages, e.messages)


class PolygonSchemaTestCase(SchemaTestCase):
    schema = PolygonSchema()

    def test_with_valid_data(self) -> None:
        x, y = 10, 20

        data = {
            "vertices": [
                {"x": x, "y": y},
                {"x": x, "y": y},
                {"x": x, "y": y},
            ],
        }

        polygon = self.schema.load(data)
        self.assertIsInstance(polygon, Polygon)

    def test_with_empty_data(self) -> None:
        data = {}

        try:
            self.schema.load(data)
        except ValidationError as e:
            self.assertDictEmpty(e.valid_data)

            messages = {
                "vertices": ["Missing data for required field."],
            }
            self.assertDictEqual(messages, e.messages)

    def test_with_invalid_data(self) -> None:
        data = {
            "vertices": {},
        }

        try:
            self.schema.load(data)
        except ValidationError as e:
            self.assertDictEmpty(e.valid_data)

            messages = {
                "vertices": ["Invalid type."],
            }
            self.assertDictEqual(messages, e.messages)


class SpaceSchemaTestCase(SchemaTestCase):
    schema = SpaceSchema()

    def test_from_path_method(self) -> None:
        path = settings.DATA_DIR.joinpath("discharged.json")
        self.assertTrue(path.is_file())

        space = Space.form_file(path)
        self.assertIsInstance(space, Space)

    def test_with_empty_data(self) -> None:
        data = {}

        try:
            self.schema.load(data)
        except ValidationError as e:
            self.assertDictEmpty(e.valid_data)

            messages = {
                "start": ["Missing data for required field."],
                "finish": ["Missing data for required field."],
                "polygons": ["Missing data for required field."],
            }
            self.assertDictEqual(messages, e.messages)


if __name__ == "__main__":
    unittest.main()
