from .constant import Constant

import math


class _Vec:

    def __init__(self):
        self._list = [0 for i in range(self._size)]

    def _parse_args(self, args):
        vec = []
        if args != ():
            if isinstance(args[0], list):
                vec = args[0]
            elif isinstance(args[0], self._vector_types):
                if len(self) == len(args[0]):
                    vec = args[0].list
                else:
                    raise TypeError('Requires ' + str(type(self)) + ' for copy')
            else:
                vec = list(args)
        else:
            vec = [0]
        while len(vec) < len(self):
            vec.append(vec[0])
        return vec

    def __repr__(self):
        return str(self.list)

    def __str__(self):
        return repr(self)

    def __len__(self):
        return self._size

    def __iter__(self):
        self._iter_scalar = iter(self._list)
        return self._iter_scalar

    def __next__(self):
        return next(self._iter_scalar)

    def __reversed__(self):
        self._iter_scalar = reversed(self._list)
        return self._iter_scalar

    def __contains__(self, item):
        if isinstance(item, self._scalar_types):
            for scalar in self:
                if scalar == item:
                    return True
        else:
            return False

    def __eq__(self, other):
        if type(self) == type(other):
            for i, scalar in enumerate(self):
                if scalar != other[i]:
                    return False
        return True

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, self._vector_types):
            return abs(self) < abs(other)
        return False

    def __le__(self, other):
        if isinstance(other, self._vector_types):
            return abs(self) <= abs(other)
        return False

    def __gt__(self, other):
        if isinstance(other, self._vector_types):
            return abs(self) > abs(other)
        return False

    def __ge__(self, other):
        if isinstance(other, self._vector_types):
            return abs(self) >= abs(other)
        return False

    def __add__(self, other):
        if type(self) == type(other):
            result = type(self)()
            for i, scalar in enumerate(self):
                result[i] = scalar + other[i]
            return result
        else:
            raise TypeError('Requires ' + str(type(self)))

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, self._scalar_types):
            result = type(self)()
            for i, scalar in enumerate(self):
                result[i] = scalar * other
            return result
        elif isinstance(other, self._vector_types):
            result = type(self)()
            for i, scalar in enumerate(self):
                result[i] = scalar * other[i]
            return result
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, self._scalar_types):
            result = type(self)()
            for i, scalar in enumerate(self):
                result[i] = scalar / other
            return result
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def __floordiv__(self, other):
        if isinstance(other, self._scalar_types):
            result = type(self)()
            for i, scalar in enumerate(self):
                result[i] = scalar // other
            return result
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def __mod__(self, other):
        if isinstance(other, self._scalar_types):
            result = type(self)()
            for i, scalar in enumerate(self):
                result[i] = scalar % other
            return result
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def __neg__(self):
        result = type(self)()
        for i, scalar in enumerate(self):
            result[i] = -scalar
        return result

    def __pos__(self):
        return self

    def __abs__(self):
        result = 0
        for scalar in self:
            result += scalar ** 2
        return result ** (1/2)

    def __invert__(self):
        result = type(self)()
        for i, scalar in enumerate(self[::-1]):
            result[i] = scalar
        return result

    def __round__(self, n=None):
        result = type(self)()
        for i, scalar in enumerate(self):
            result[i] = round(scalar, n)
        return result

    def __ceil__(self):
        result = type(self)()
        for i, scalar in enumerate(self):
            result[i] = math.ceil(scalar)
        return result

    def __floor__(self):
        result = type(self)()
        for i, scalar in enumerate(self):
            result[i] = math.floor(scalar)
        return result

    def __trunc__(self):
        result = type(self)()
        for i, scalar in enumerate(self):
            result[i] = math.trunc(scalar)
        return result

    def normalize(self):
        norm = abs(self)
        if norm == 0:
            return self
        else:
            return self / norm

    def distance(self, other):
        if type(self) == type(other):
            return abs(self - other)
        else:
            raise TypeError('Requires ' + str(type(self)))

    def dot(self, other):
        if type(self) == type(other):
            result = 0
            for i, scalar in enumerate(self):
                result += scalar * other[i]
            return result
        else:
            raise TypeError('Requires ' + str(type(self)))

    def angle(self, other):
        if type(self) == type(other):
            return math.acos(self.dot(other) / (abs(self) * abs(other)))
        else:
            raise TypeError('Requires ' + str(type(self)))

    def __getitem__(self, item):
        return self._list[item]

    def __setitem__(self, key, value):
        self._list[key] = value

    def __delitem__(self, key):
        del self[key]

    @property
    def _scalar_types(self):
        return ConstantVec.SCALAR_TYPES

    @property
    def _vector_types(self):
        return ConstantVec.VECTOR_TYPES

    @property
    def _size(self):
        return ConstantVec.VECTOR_SIZE.get(type(self))

    @property
    def list(self):
        return self._list

    _list = []


class Vec2(_Vec):

    def __init__(self, *args):
        vec = self._parse_args(args)
        super().__init__()
        self.x = vec[0]
        self.y = vec[1]

    @property
    def x(self):
        return self._list[0]

    @x.setter
    def x(self, value):
        if isinstance(value, self._scalar_types):
            self._list[0] = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    @property
    def y(self):
        return self._list[1]

    @y.setter
    def y(self, value):
        if isinstance(value, self._scalar_types):
            self._list[1] = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))


class Vec3(Vec2):

    def __init__(self, *args):
        vec = self._parse_args(args)
        super().__init__(vec[0], vec[1])
        self.z = vec[2]

    def cross(self, other):
        if type(self) == Vec3 and type(other) == Vec3:
            return Vec3(self.y * other.z - self.z * other.y,
                        self.z * other.x - self.x * other.z,
                        self.x * other.y - self.y * other.x)
        else:
            raise TypeError('Requires ' + str(Vec3))

    @property
    def z(self):
        return self._list[2]

    @z.setter
    def z(self, value):
        if isinstance(value, self._scalar_types):
            self._list[2] = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))


class Vec4(Vec3):

    def __init__(self, *args):
        vec = self._parse_args(args)
        super().__init__(vec[0], vec[1], vec[2])
        self.w = vec[3]

    @property
    def w(self):
        return self._list[3]

    @w.setter
    def w(self, value):
        if isinstance(value, self._scalar_types):
            self._list[3] = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))


class ConstantVec(Constant):
    SCALAR_TYPES = int, float
    VECTOR_TYPES = Vec2, Vec3, Vec4
    VECTOR_SIZE = {
        _Vec: 0,
        Vec2: 2,
        Vec3: 3,
        Vec4: 4
    }
