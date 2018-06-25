from .vector import *
from .constant import Constant

import math


class _Polar:
    def __len__(self):
        return 3

    def __eq__(self, other):
        if isinstance(other, self._polar_types):
            return self.vector == other.vector
        elif isinstance(other, ConstantVec.VECTOR_TYPES):
            return self.vector == other
        return False

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, self._polar_types) or isinstance(other, ConstantVec.VECTOR_TYPES):
            return abs(self) < abs(other)
        return False

    def __le__(self, other):
        if isinstance(other, self._polar_types) or isinstance(other, ConstantVec.VECTOR_TYPES):
            return abs(self) <= abs(other)
        return False

    def __gt__(self, other):
        if isinstance(other, self._polar_types) or isinstance(other, ConstantVec.VECTOR_TYPES):
            return abs(self) > abs(other)
        return False

    def __ge__(self, other):
        if isinstance(other, self._polar_types) or isinstance(other, ConstantVec.VECTOR_TYPES):
            return abs(self) >= abs(other)
        return False

    def __add__(self, other):
        if isinstance(other, self._polar_types):
            return type(self)(self.vector + other.vector, True)
        elif isinstance(other, ConstantVec.VECTOR_TYPES):
            return type(self)(self.vector + other, True)
        else:
            raise TypeError('Requires ' + str(self._polar_types) + ' or ' + str(ConstantVec.VECTOR_TYPES))

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, self._polar_types):
            return type(self)(self.vector * other.vector, True)
        elif isinstance(other, ConstantVec.VECTOR_TYPES):
            return type(self)(self.vector * other, True)
        else:
            raise TypeError('Requires ' + str(self._polar_types) + ' or ' + str(ConstantVec.VECTOR_TYPES))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, ConstantVec.SCALAR_TYPES):
            return type(self)(self.vector / other, True)
        else:
            raise TypeError('Requires ' + str(ConstantVec.SCALAR_TYPES))

    def __floordiv__(self, other):
        if isinstance(other, ConstantVec.SCALAR_TYPES):
            return type(self)(self.vector // other, True)
        else:
            raise TypeError('Requires ' + str(ConstantVec.SCALAR_TYPES))

    def __mod__(self, other):
        if isinstance(other, ConstantVec.SCALAR_TYPES):
            return type(self)(self.vector % other, True)
        else:
            raise TypeError('Requires ' + str(ConstantVec.SCALAR_TYPES))

    def __neg__(self):
        if isinstance(self, CylindricCoordinate):
            return type(self)(Vec3(
                self.radius,
                self.azimuth + math.pi,
                - self.elevation
            ))
        elif isinstance(self, SphericalCoordinate):
            return type(self)(Vec3(
                self.radius,
                self.inclination + math.pi,
                self.azimuth + math.pi
            ))
        else:
            raise TypeError('Requires ' + str(self._polar_types))

    def __pos__(self):
        return self

    def __abs__(self):
        if isinstance(self, CylindricCoordinate):
            return math.sqrt(self.radius ** 2 + self.elevation ** 2)
        elif isinstance(self, SphericalCoordinate):
            return self.radius
        else:
            raise TypeError('Requires ' + str(self._polar_types))

    def __invert__(self):
        return type(self)(~self.vector, True)

    def __round__(self, n=None):
        return type(self)(round(self.vector, n), True)

    def __ceil__(self):
        return type(self)(math.ceil(self.vector), True)

    def __floor__(self):
        return type(self)(math.floor(self.vector), True)

    def __trunc__(self):
        return type(self)(math.trunc(self.vector), True)

    def normalize(self):
        return type(self)(self.vector.normalize(), True)

    def distance(self, other):
        return type(self)(self.vector.distance(other), True)

    def angle(self, other):
        if isinstance(other, self._polar_types):
            return self.vector.angle(other.vector)
        elif isinstance(other, ConstantVec.VECTOR_TYPES):
            return self.vector.angle(other)
        else:
            raise TypeError('Requires ' + str(self._polar_types) + ' or ' + str(ConstantVec.VECTOR_TYPES))

    @property
    def vector(self):
        if isinstance(self, CylindricCoordinate):
            return Vec3(
                self.radius * math.cos(self.azimuth),
                self.elevation,
                self.radius * math.sin(self.azimuth)
            )
        elif isinstance(self, SphericalCoordinate):
            return Vec3(
                self.radius * math.sin(self.inclination) * math.cos(self.azimuth),
                self.radius * math.cos(self.inclination),
                self.radius * math.sin(self.inclination) * math.sin(self.azimuth)
            )
        else:
            raise TypeError('Requires ' + str(self._polar_types))

    @property
    def _scalar_types(self):
        return ConstantPolar.SCALAR_TYPES

    @property
    def _polar_types(self):
        return ConstantPolar.POLAR_TYPES


class CylindricCoordinate(_Polar):
    def __init__(self, other, convert=False):
        if isinstance(other, Vec3):
            if convert:
                self.radius = math.sqrt(other.x ** 2 + other.z ** 2)
                if other.x == 0 and other.z == 0:
                    self.azimuth = 0
                elif other.x >= 0:
                    self.azimuth = math.asin(other.z / self.radius)
                elif other.x > 0:
                    self.azimuth = math.atan(other.z / other.x)
                elif other.x < 0:
                    self.azimuth = - math.asin(other.z / self.radius) + math.pi
                else:
                    raise NameError('Should never happen')
                self.elevation = other.y
            else:
                self.radius = other.x
                self.azimuth = other.y
                self.elevation = other.z
        else:
            raise TypeError('Requires ' + str(Vec3))

    def __repr__(self):
        return (
            'radius = ' + str(self.radius) +
            ', azimuth = ' + str(self.azimuth) +
            ', elevation = ' + str(self.elevation)
        )

    def __str__(self):
        return str([self.radius, self.azimuth, self.elevation])

    def __getitem__(self, item):
        if item == 0:
            return self.radius
        elif item == 1:
            return self.azimuth
        elif item == 2:
            return self.elevation
        else:
            raise TypeError('Requires ' + str(int) + ' between 0 and 2')

    def __setitem__(self, key, value):
        if key == 0:
            self.radius = value
        elif key == 1:
            self.azimuth = value
        elif key == 2:
            self.elevation = value
        else:
            raise TypeError('Requires ' + str(int) + ' between 0 and 2')

    def __delitem__(self, key):
        if key == 0:
            del self._radius
        elif key == 1:
            del self._azimuth
        elif key == 2:
            del self._elevation
        else:
            raise TypeError('Requires ' + str(int) + ' between 0 and 2')

    @property
    def spherical(self):
        return SphericalCoordinate(Vec3(
            math.sqrt(self.radius ** 2 + self.elevation ** 2),
            math.atan(self.radius / self.elevation),
            self.azimuth
        ))

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if isinstance(value, self._scalar_types):
            self._radius = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    @property
    def azimuth(self):
        return self._azimuth

    @azimuth.setter
    def azimuth(self, value):
        if isinstance(value, self._scalar_types):
            self._azimuth = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    @property
    def elevation(self):
        return self._elevation

    @elevation.setter
    def elevation(self, value):
        if isinstance(value, self._scalar_types):
            self._elevation = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    _radius = 0
    _azimuth = 0
    _elevation = 0


class SphericalCoordinate(_Polar):
    def __init__(self, other, convert=False):
        if isinstance(other, Vec3):
            if convert:
                self.radius = abs(other)
                self.inclination = math.acos(other.y / self.radius)
                self.azimuth = math.atan(other.z / other.x)
            else:
                self.radius = other.x
                self.inclination = other.y
                self.azimuth = other.z
        else:
            raise TypeError('Requires ' + str(Vec3))

    def __repr__(self):
        return (
            'radius = ' + str(self.radius) +
            ', inclination = ' + str(self.inclination) +
            ', azimuth = ' + str(self.azimuth)
        )

    def __str__(self):
        return str([self.radius, self.inclination, self.azimuth])

    def __getitem__(self, item):
        if item == 0:
            return self.radius
        elif item == 1:
            return self.inclination
        elif item == 2:
            return self.azimuth
        else:
            raise TypeError('Requires ' + str(int) + ' between 0 and 2')

    def __setitem__(self, key, value):
        if key == 0:
            self.radius = value
        elif key == 1:
            self.inclination = value
        elif key == 2:
            self.azimuth = value
        else:
            raise TypeError('Requires ' + str(int) + ' between 0 and 2')

    def __delitem__(self, key):
        if key == 0:
            del self._radius
        elif key == 1:
            del self._inclination
        elif key == 2:
            del self._azimuth
        else:
            raise TypeError('Requires ' + str(int) + ' between 0 and 2')

    @property
    def cylindric(self):
        return CylindricCoordinate(Vec3(
            self.radius * math.sin(self.inclination),
            self.azimuth,
            self.radius * math.cos(self.inclination)
        ))

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if isinstance(value, self._scalar_types):
            self._radius = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    @property
    def inclination(self):
        return self._inclination

    @inclination.setter
    def inclination(self, value):
        if isinstance(value, self._scalar_types):
            self._inclination = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    @property
    def azimuth(self):
        return self._azimuth

    @azimuth.setter
    def azimuth(self, value):
        if isinstance(value, self._scalar_types):
            self._azimuth = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    _radius = 0
    _inclination = 0
    _azimuth = 0


class ConstantPolar(Constant):
    SCALAR_TYPES = int, float
    POLAR_TYPES = _Polar, CylindricCoordinate, SphericalCoordinate
