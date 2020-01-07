import unittest
from typing import Any

from marshmallow import ValidationError

from project import (
    Point,
    PointSchema,
    Polygon,
    PolygonSchema,
    Space,
    SpaceSchema,
    settings,
)


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
                "x": ["Not a valid number."],
                "y": ["Not a valid number."],
            }
            self.assertDictEqual(messages, e.messages)


class PolygonSchemaTestCase(SchemaTestCase):
    schema = PolygonSchema()

    def test_with_valid_data(self) -> None:
        x, y = 10, 20

        data = {
            "x": x,
            "y": y,
            "vertices": [
                {
                    "x": x,
                    "y": y,
                },
            ],
        }

        polygon = self.schema.load(data)
        self.assertIsInstance(polygon, Polygon)

        self.assertEqual(x, polygon.x)
        self.assertEqual(y, polygon.y)

        vertices = [
            Point(x, y),
        ]
        self.assertEqual(polygon.vertices, vertices)

        self.assertDictEqual(data, self.schema.dump(polygon))

    def test_with_empty_data(self) -> None:
        data = {}

        try:
            self.schema.load(data)
        except ValidationError as e:
            self.assertDictEmpty(e.valid_data)

            messages = {
                "x": ["Missing data for required field."],
                "y": ["Missing data for required field."],
                "vertices": ["Missing data for required field."],
            }
            self.assertDictEqual(messages, e.messages)

    def test_with_invalid_data(self) -> None:
        data = {
            "x": type,
            "y": type,
            "vertices": {},
        }

        try:
            self.schema.load(data)
        except ValidationError as e:
            self.assertDictEmpty(e.valid_data)

            messages = {
                "x": ["Not a valid number."],
                "y": ["Not a valid number."],
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
