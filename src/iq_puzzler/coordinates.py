from __future__ import annotations
import numpy as np
from typing import NamedTuple


# Global constants
FLOAT_TOLERANCE = 1e-6  # Tolerance for floating point comparisons


class Location3D(NamedTuple):
    """A 3D location in the puzzle grid.

    The grid uses a coordinate system where:
    - Points in each layer are spaced XY_DIST apart in x and y directions
    - For odd z-layers (1, 3, 5, etc.), points are shifted by XY_DIST/2 in both x and y
    - In the z direction, layers are spaced Z_DIST apart
    """

    x: float
    y: float
    z: float

    def __eq__(self, other: object) -> bool:
        """Compare two locations with floating point precision."""
        if not isinstance(other, Location3D):
            return NotImplemented
        return (
            abs(self.x - other.x) < FLOAT_TOLERANCE
            and abs(self.y - other.y) < FLOAT_TOLERANCE
            and abs(self.z - other.z) < FLOAT_TOLERANCE
        )

    def __hash__(self) -> int:
        """Hash the location using rounded coordinates."""
        # Round to the same precision as our tolerance
        precision = int(-np.log10(FLOAT_TOLERANCE))
        return hash(
            (
                round(self.x, precision),
                round(self.y, precision),
                round(self.z, precision),
            )
        )


# Constants for coordinate transformations
XY_DIST = 1.0  # Base distance between points in the x-y plane
# Points in each layer are spaced XY_DIST apart
# For odd z-layers, points are shifted by XY_DIST/2 in both x and y

Z_DIST = 0.5 * np.sqrt(2 * XY_DIST * XY_DIST)  # Vertical distance between layers
# This is half the height of a regular tetrahedron with edge length XY_DIST
# This ensures that points in adjacent layers form equilateral triangles
