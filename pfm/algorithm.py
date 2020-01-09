# pylint: disable=C0103

import json
from pathlib import Path
from typing import Dict, List

import attr
import numpy as np

from .models import Point, Polygon, Space

__all__ = (
    "Segment",
    "PathPlan",
    "PotentialFieldMethod",
)


@attr.s(slots=True, frozen=True)
class Segment:
    p1: Point = attr.ib()
    p2: Point = attr.ib()

    def to_dict(self) -> Dict[str, float]:
        return {
            "x1": self.p1.x,
            "y1": self.p1.y,
            "x2": self.p2.x,
            "y2": self.p2.y,
        }


@attr.s(slots=True, frozen=True)
class PathPlan:
    segments: List[Segment] = attr.ib(factory=list)

    def push(self, segment: Segment) -> None:
        self.segments.append(segment)

    def to_json(self) -> str:
        data = [
            segment.to_dict() for segment in self.segments
        ]
        return json.dumps(data, indent=4)

    def dump(self, path: Path) -> None:
        text = self.to_json()
        path.write_text(text, encoding="utf-8")

    def __contains__(self, segment: Segment) -> bool:
        return segment in self.segments


@attr.s(slots=True, frozen=True)
class PotentialFieldMethod:
    step: float = attr.ib(default=2)
    kp: float = attr.ib(default=10.0)
    eta: float = attr.ib(default=200)
    r0: float = attr.ib(default=0.4)

    def attractive(self, point: Point, goal: Point) -> float:
        return 0.5 * self.kp * point.distance(goal)

    def repulsive(self, point: Point, polygons: List[Polygon]) -> float:
        for polygon in polygons:
            dist = polygon.distance(point)
            if dist > self.r0:
                continue
            if dist <= 0.1:
                dist = 0.1
            return 0.5 * self.eta * (1. / dist - 1. / self.r0) ** 2
        return 0

    def potential(self, point: Point, space: Space) -> float:
        u_att = self.attractive(point, space.finish)
        u_rep = self.repulsive(point, space.polygons)
        u = u_att + u_rep
        return u

    def neighbors(self, point: Point) -> List[Point]:
        return [
            point + Point(0, self.step),            # up
            point + Point(self.step, 0),            # right
            point + Point(0, -self.step),           # down
            point + Point(-self.step, 0),           # left
            point + Point(self.step, self.step),    # right up diag
            point + Point(self.step, -self.step),   # right down diag
            point + Point(-self.step, -self.step),  # left down diag
            point + Point(-self.step, self.step),   # lef up diag
        ]

    def select(self, points: List[Point], space: Space) -> Point:
        potentials = [self.potential(p, space) for p in points]
        i = int(np.argmin(potentials))
        return points[i]

    def solve(self, space: Space, acc: float = 0.1) -> PathPlan:
        plan = PathPlan()
        current = space.start
        while current.distance(space.finish) > acc:
            neighbors = self.neighbors(current)
            selected = self.select(neighbors, space)
            segment = Segment(current, selected)
            if segment in plan:
                break
            plan.push(segment)
            current = selected
        return plan
