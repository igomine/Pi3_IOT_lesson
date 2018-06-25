from .vector import *
from .euler import *
from .constant import Constant

import sys
import math


class Quat:

    def __init__(self, *args):
        quat = []
        if not isinstance(args, list):
            quat = list(args)
        if isinstance(quat, list):
            if len(quat) == 1:
                if isinstance(quat[0], Vec4):
                    self.w = quat[0].w
                    self.vec = Vec3(quat[0].x, quat[0].y, quat[0].z)
                elif isinstance(quat[0], EulerAngle):
                    cos_yaw = math.cos(quat[0].yaw / 2)
                    sin_yaw = math.sin(quat[0].yaw / 2)
                    cos_pitch = math.cos(quat[0].pitch / 2)
                    sin_pitch = math.sin(quat[0].pitch / 2)
                    cos_roll = math.cos(quat[0].roll / 2)
                    sin_roll = math.sin(quat[0].roll / 2)
                    self.w = cos_yaw * cos_pitch * cos_roll + sin_yaw * sin_pitch * sin_roll
                    self.vec = Vec3(
                        cos_yaw * sin_pitch * cos_roll + sin_yaw * cos_pitch * sin_roll,
                        sin_yaw * cos_pitch * cos_roll - cos_yaw * sin_pitch * sin_roll,
                        cos_yaw * cos_pitch * sin_roll - sin_yaw * sin_pitch * cos_roll
                    )
                elif isinstance(quat[0], self._scalar_types):
                    self.w = quat[0]
                    self.vec = Vec3()
                else:
                    raise TypeError('Requires ' + str(Vec4))
            elif len(quat) == 2:
                if isinstance(quat[0], self._scalar_types) and isinstance(quat[1], self._vector_types):
                    self.w = quat[0]
                    self.vec = quat[1]
                else:
                    raise TypeError('Requires ' + str(self._scalar_types) + ' and ' + str(self._vector_types))
            elif len(quat) == 4:
                if (
                    isinstance(quat[0], self._scalar_types) and
                    isinstance(quat[1], self._scalar_types) and
                    isinstance(quat[2], self._scalar_types) and
                    isinstance(quat[3], self._scalar_types)
                ):
                    self.w = quat[0]
                    self.x = quat[1]
                    self.y = quat[2]
                    self.z = quat[3]
                else:
                    raise TypeError('Requires 4 ' + str(self._scalar_types))
            else:
                self.w = 1
                self.vec = Vec3()
        else:
            raise NameError('Should never happen')

    def __repr__(self):
        return str(self.list)

    def __str__(self):
        return repr(self)

    def __len__(self):
        return 4

    def __eq__(self, other):
        if type(self) == type(other):
            return self.w == other.w and self.vec == other.vec
        return True

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if type(self) == type(other):
            return abs(self) < abs(other)
        return False

    def __le__(self, other):
        if type(self) == type(other):
            return abs(self) <= abs(other)
        return False

    def __gt__(self, other):
        if type(self) == type(other):
            return abs(self) > abs(other)
        return False

    def __ge__(self, other):
        if type(self) == type(other):
            return abs(self) >= abs(other)
        return False

    def __add__(self, other):
        if type(self) == type(other):
            return type(self)(
                self.w + other.w,
                self.vec + other.vec
            )
        else:
            raise TypeError('Requires ' + str(type(self)))

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if type(self) == type(other):
            return type(self)(
                self.w * other.w - self.vec.dot(other.vec),
                self.w * other.vec +
                other.w * self.vec +
                self.vec.cross(other.vec)
            )
        elif isinstance(other, self._scalar_types):
            return type(self)(
                self.w * other,
                self.vec * other
            )
        else:
            raise TypeError('Requires ' + str(type(self)) + ' or ' + str(self._scalar_types))

    def __rmul__(self, other):
        if type(self) == type(other):
            raise NameError('Product quaternion is not commutative')
        elif isinstance(other, self._scalar_types):
            return self * other
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def __truediv__(self, other):
        if type(self) == type(other):
            return self * ~other
        elif isinstance(other, self._scalar_types):
            return type(self)(
                self.w / other,
                self.vec / other
            )
        else:
            raise TypeError('Requires ' + str(type(self)) + ' or ' + str(self._scalar_types))

    def __floordiv__(self, other):
        if type(self) == type(other):
            return self / other
        elif isinstance(other, self._scalar_types):
            return type(self)(
                self.w // other,
                self.vec // other
            )
        else:
            raise TypeError('Requires ' + str(type(self)) + ' or ' + str(self._scalar_types))

    def __mod__(self, other):
        if isinstance(other, self._scalar_types):
            return type(self)(
                self.w % other,
                self.vec % other
            )
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def __neg__(self):
        return type(self)(
            - self.w,
            - self.vec
        )

    def __pos__(self):
        return self

    def __abs__(self):
        return (self.w ** 2 + abs(self.vec) ** 2) ** (1/2)

    def __invert__(self):
        return self.conjugate() * (1 / abs(self))

    def __pow__(self, power, modulo=None):
        log = power * self.log()
        return log.exp()

    def exp(self):
        norm = abs(self.vec)
        vec = self.vec
        if norm > sys.float_info.epsilon:
            vec = vec / norm
        return Quat(
            math.exp(self.w) * math.cos(norm),
            math.exp(self.w) * math.sin(norm) * self.vec
        )

    def log(self):
        quat_norm = abs(self)
        if quat_norm < sys.float_info.epsilon:
            return Quat(- float('inf'), float('nan') * self.vec)
        vec_norm = abs(self.vec)
        if vec_norm < sys.float_info.epsilon:
            return Quat(math.log(quat_norm), Vec3(0))
        return Quat(math.log(quat_norm), math.acos(self.w / quat_norm) * self.vec.normalize())

    def angle(self):
        return math.acos(self.w) * 2

    def unit_vector(self):
        return self.vec.normalize()

    def rotate(self, angle, axis):
        if isinstance(angle, self._scalar_types) and isinstance(axis, self._vector_types):
            return self * Quat(
                math.cos(angle / 2),
                axis.normalize() * math.sin(angle / 2)
            )
        else:
            raise TypeError('Requires ' + str(self._scalar_types) + ' and ' + str(self._vector_types))

    def axis(self):
        if 1 - self.w ** 2 <= 0:
            return Vec3(0, 0, 1)
        tmp = 1 / math.sqrt(1 - self.w ** 2)
        return Vec3(self.x * tmp, self.y * tmp, self.z * tmp)

    def yaw(self):
        theta = - 2 * (self.x * self.z - self.w * self.y)
        theta = 1 if theta > 1 else theta
        theta = -1 if theta < -1 else theta
        return math.asin(theta)

    def pitch(self):
        return math.atan2(
            2 * (self.y * self.z + self.w * self.x),
            self.w ** 2 - self.x ** 2 - self.y ** 2 + self.z ** 2
        )

    def roll(self):
        return math.atan2(
            2 * (self.y * self.x + self.w * self.z),
            self.w ** 2 - self.x ** 2 - self.y ** 2 + self.z ** 2
        )

    def euler(self):
        return EulerAngle(
            self.yaw(),
            self.pitch(),
            self.roll()
        )

    def normalize(self):
        norm = abs(self)
        if norm == 0:
            return self
        else:
            return self / norm

    def conjugate(self):
        return type(self)(
            self.w,
            - self.vec
        )

    def dot(self, other):
        if type(self) == type(other):
            return self.w * other.w + self.vec.dot(other.vec)
        else:
            raise TypeError('Requires ' + str(type(self)))

    def lerp(self, other, factor):
        if type(self) == type(other) and isinstance(factor, self._scalar_types):
            k = 1 if factor > 1 else factor
            k = 0 if factor < 0 else factor
            return self * (1 - k) + other * k
        else:
            raise TypeError('Requires ' + str(type(self)) + ' and ' + str(self._scalar_types))

    def slerp(self, other, factor):
        if type(self) == type(other) and isinstance(factor, self._scalar_types):
            k = 1 if factor > 1 else factor
            k = 0 if factor < 0 else factor
            return ((other * ~self) ** factor) * self
        else:
            raise TypeError('Requires ' + str(type(self)) + ' and ' + str(self._scalar_types))

    def nlerp(self, other, factor):
        if type(self) == type(other) and isinstance(factor, self._scalar_types):
            k = 1 if factor > 1 else factor
            k = 0 if factor < 0 else factor
            tmp = (1 - factor) * self + factor * other
            return tmp / abs(tmp)
        else:
            raise TypeError('Requires ' + str(type(self)) + ' and ' + str(self._scalar_types))

    @property
    def x(self):
        return self.vec.x

    @x.setter
    def x(self, value):
        if isinstance(value, self._scalar_types):
            self._vec.x = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    @property
    def y(self):
        return self.vec.y

    @y.setter
    def y(self, value):
        if isinstance(value, self._scalar_types):
            self._vec.y = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    @property
    def z(self):
        return self.vec.z

    @z.setter
    def z(self, value):
        if isinstance(value, self._scalar_types):
            self._vec.z = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        if isinstance(value, self._scalar_types):
            self._w = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    @property
    def _scalar_types(self):
        return ConstantQuat.SCALAR_TYPES

    @property
    def _vector_types(self):
        return ConstantQuat.VECTOR_TYPES

    @property
    def list(self):
        return [
            self._w,
            self.vec.x,
            self.vec.y,
            self.vec.z
        ]

    @property
    def vec(self):
        return self._vec

    @vec.setter
    def vec(self, value):
        if isinstance(value, self._vector_types):
            if type(value) == Vec2:
                self._vec = Vec3(value.x, value.y, 0)
            else:
                self._vec = Vec3(value.list)
        else:
            raise TypeError('Requires ' + str(self._vector_types))

    _w = 1
    _vec = Vec3(0)


class ConstantQuat(Constant):
    SCALAR_TYPES = int, float
    VECTOR_TYPES = Vec2, Vec3, Vec4
