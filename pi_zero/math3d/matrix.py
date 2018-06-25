from .vector import *
from .constant import Constant

import math
import sys


class _Mat:
    def __init__(self, *args):
        self._init_zero()
        if args != ():
            if isinstance(args[0], list):
                self._init_matrix(args[0])
            elif isinstance(args[0], self._matrix_types):
                if len(self) == len(args[0]):
                    self._matrix = args[0].matrix
                else:
                    raise TypeError('Requires ' + str(type(self)) + ' for copy')
            else:
                self._init_matrix(list(args))
            if isinstance(args[0], self._scalar_types):
                if args[0] == 1 and len(args) == 1:
                    self._init_identity()

    def _init_zero(self):
        self._matrix = []
        for i in range(self.width):
            self._matrix.append(self._type())

    def _init_identity(self):
        if self.width == self.height:
            self._matrix = []
            for i in range(self.width):
                self._matrix.append(self._type([1 if i == j else 0 for j in range(self.height)]))
        else:
            raise TypeError('Requires ' + str(type(self)) + ' with same width and height')

    def _init_matrix(self, mat):
        if self._is_vectors_list(mat) and len(mat) <= self.width:
            self._init_vectors_list(mat)
        elif self._is_scalars_list(mat) and len(mat) <= self._size:
            self._init_scalars_list(mat)
        else:
            raise TypeError('Requires ' + str(list) + ' of ' +
                            str(self.width) + ' ' + str(self._type) + ' or ' +
                            str(self._size) + ' ' + str(self._scalar_types))

    def _is_vectors_list(self, mat):
        if not isinstance(mat, list):
            return False
        for element in mat:
            if type(element) != self._type:
                return False
        return True

    def _init_vectors_list(self, mat):
        for i, vec in enumerate(mat):
            self[i] = vec

    def _is_scalars_list(self, mat):
        if not isinstance(mat, list):
            return False
        for element in mat:
            if not isinstance(element, self._scalar_types):
                return False
        return True

    def _init_scalars_list(self, mat):
        while len(mat) < self._size:
            mat.append(0)
        for i in range(self.width):
            for j in range(self.height):
                self[i][j] = mat[i * self.height + j]

    def __repr__(self):
        stride = 0
        for vec in self:
            for scalar in vec:
                if len(str(scalar)) > stride:
                    stride = len(str(scalar))
        str_out = ''
        for i in range(self.height):
            str_out += '| '
            for j in range(self.width):
                str_out += str('{:>' + str(stride) + '}').format(str(self[j][i])) + ' '
            str_out += '|\n'
        return str_out

    def __str__(self):
        str_out = '['
        for i, vec in enumerate(self):
            str_out += str(vec)
            if i + 1 < self.width:
                str_out += ', '
        str_out += ']'
        return str_out

    def __len__(self):
        return self._size

    def __iter__(self):
        self._iter_vector = iter(self._matrix)
        return self._iter_vector

    def __next__(self):
        return next(self._iter_vector)

    def __reversed__(self):
        self._iter_vector = reversed(self._matrix)
        return self._iter_vector

    def __contains__(self, item):
        if isinstance(item, self._scalar_types):
            return item in self.flat
        elif isinstance(item, self._vector_types):
            return item in self._matrix
        else:
            return False

    def __eq__(self, other):
        if type(other) == type(self):
            for i, vec in enumerate(self):
                if vec != other[i]:
                    return False
        else:
            return False
        return True

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        if type(other) == type(self):
            result = type(self)()
            for i, vec in enumerate(self):
                result[i] = vec + other[i]
            return result
        else:
            raise TypeError('Requires ' + str(type(self)))

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, self._scalar_types):
            result = [scalar for vec in [u * other for u in self] for scalar in vec]
            return type(self)(result)
        elif type(other) == type(self):
            result = [sum(x * y for x, y in zip(col, row)) for col in other.list for row in zip(*self.list)]
            return type(self)(result)
        elif type(other) == self._type:
            mat = type(self)(other)
            result = [sum(x * y for x, y in zip(col, row)) for col in mat.list for row in zip(*self.list)]
            return self._type(result)
        else:
            raise TypeError('Requires ' + str(self._scalar_types) + ' or ' + str(type(self)))

    def __rmul__(self, other):
        if isinstance(other, self._scalar_types):
            return self * other
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def __truediv__(self, other):
        if isinstance(other, self._scalar_types):
            result = [scalar for vec in [u / other for u in self] for scalar in vec]
            return type(self)(result)
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def __floordiv__(self, other):
        if isinstance(other, self._scalar_types):
            result = [scalar for vec in [u // other for u in self] for scalar in vec]
            return type(self)(result)
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def __mod__(self, other):
        if isinstance(other, self._scalar_types):
            result = [scalar for vec in [u % other for u in self] for scalar in vec]
            return type(self)(result)
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def __neg__(self):
        result = type(self)()
        for i, vec in enumerate(self):
            result[i] = -vec
        return result

    def __pos__(self):
        return self

    def _det(self, mat, n):
        result = 0
        width = len(mat)
        if width == 1:
            result = n * mat[0][0]
        else:
            sign = -1
            for i in range(width):
                tmp_mat = []
                for j in range(1, width):
                    tmp_vec = []
                    for k in range(width):
                        if k != i:
                            tmp_vec.append(mat[j][k])
                    tmp_mat.append(tmp_vec)
                sign *= -1
                result += n * self._det(tmp_mat, sign * mat[0][i])
        return result

    def __abs__(self):
        return self._det(self.list, 1)

    def __invert__(self):
        determinant = abs(self)
        if determinant != 0:
            result = type(self)()
            if type(self) == Mat2:
                result[0][0] = self[1][1]
                result[0][1] = - self[0][1]
                result[1][0] = - self[1][0]
                result[1][1] = self[0][0]
            elif type(self) == Mat3:
                result[0][0] = self[1][1] * self[2][2] - self[2][1] * self[1][2]
                result[0][1] = self[2][1] * self[0][2] - self[0][1] * self[2][2]
                result[0][2] = self[0][1] * self[1][2] - self[1][1] * self[0][2]
                result[1][0] = self[2][0] * self[1][2] - self[1][0] * self[2][2]
                result[1][1] = self[0][0] * self[2][2] - self[2][0] * self[0][2]
                result[1][2] = self[1][0] * self[0][2] - self[0][0] * self[1][2]
                result[2][0] = self[1][0] * self[2][1] - self[2][0] * self[1][1]
                result[2][1] = self[2][0] * self[0][1] - self[0][0] * self[2][1]
                result[2][2] = self[0][0] * self[1][1] - self[1][0] * self[0][1]
            elif type(self) == Mat4:
                coef = [
                    self[2][2] * self[3][3] - self[3][2] * self[2][3],
                    self[1][2] * self[3][3] - self[3][2] * self[1][3],
                    self[1][2] * self[2][3] - self[2][2] * self[1][3],

                    self[2][1] * self[3][3] - self[3][1] * self[2][3],
                    self[1][1] * self[3][3] - self[3][1] * self[1][3],
                    self[1][1] * self[2][3] - self[2][1] * self[1][3],

                    self[2][1] * self[3][2] - self[3][1] * self[2][2],
                    self[1][1] * self[3][2] - self[3][1] * self[1][2],
                    self[1][1] * self[2][2] - self[2][1] * self[1][2],

                    self[2][0] * self[3][3] - self[3][0] * self[2][3],
                    self[1][0] * self[3][3] - self[3][0] * self[1][3],
                    self[1][0] * self[2][3] - self[2][0] * self[1][3],

                    self[2][0] * self[3][2] - self[3][0] * self[2][2],
                    self[1][0] * self[3][2] - self[3][0] * self[1][2],
                    self[1][0] * self[2][2] - self[2][0] * self[1][2],

                    self[2][0] * self[3][1] - self[3][0] * self[2][1],
                    self[1][0] * self[3][1] - self[3][0] * self[1][1],
                    self[1][0] * self[2][1] - self[2][0] * self[1][1]
                ]

                fac = [
                    Vec4(coef[0], coef[0], coef[1], coef[2]),
                    Vec4(coef[3], coef[3], coef[4], coef[5]),
                    Vec4(coef[6], coef[6], coef[7], coef[8]),
                    Vec4(coef[9], coef[9], coef[10], coef[11]),
                    Vec4(coef[12], coef[12], coef[13], coef[14]),
                    Vec4(coef[15], coef[15], coef[16], coef[17])
                ]

                vec = [
                    Vec4(self[1][0], self[0][0], self[0][0], self[0][0]),
                    Vec4(self[1][1], self[0][1], self[0][1], self[0][1]),
                    Vec4(self[1][2], self[0][2], self[0][2], self[0][2]),
                    Vec4(self[1][3], self[0][3], self[0][3], self[0][3])
                ]

                inv = [
                    (vec[1] * fac[0]) - (vec[2] * fac[1]) + (vec[3] * fac[2]),
                    (vec[0] * fac[0]) - (vec[2] * fac[3]) + (vec[3] * fac[4]),
                    (vec[0] * fac[1]) - (vec[1] * fac[3]) + (vec[3] * fac[5]),
                    (vec[0] * fac[2]) - (vec[1] * fac[4]) + (vec[2] * fac[5])
                ]

                sign = [
                    Vec4(+1, -1, +1, -1),
                    Vec4(-1, +1, -1, +1)
                ]

                result[0] = inv[0] * sign[0]
                result[1] = inv[1] * sign[1]
                result[2] = inv[2] * sign[0]
                result[3] = inv[3] * sign[1]
            else:
                raise TypeError('Requires ' + str(self._matrix_types))
            result *= 1 / determinant
            return result
        else:
            raise TypeError('Requires ' + str(self._matrix_types) + ' with determinant != 0')

    def __getitem__(self, item):
        return self._matrix[item]

    def __setitem__(self, key, value):
        self._matrix[key] = value

    def transpose(self):
        result = type(self)([scalar for vec in list(zip(*self.list)) for scalar in vec])
        return result

    def is_diagonal(self):
        for i, vec in enumerate(self):
            for j, scalar in enumerate(vec):
                if i != j and scalar != 0:
                    return False
        return True

    def is_orthogonal(self):
        mat = type(self)(self)
        mat.transpose()
        if self * mat == type(self)(1):
            return True
        return False

    @property
    def list(self):
        return [[scalar for scalar in vector] for vector in self]

    @property
    def matrix(self):
        return [vec for vec in self]

    @property
    def flat(self):
        return [scalar for vec in self for scalar in vec]

    @property
    def _scalar_types(self):
        return ConstantMat.SCALAR_TYPES

    @property
    def _matrix_types(self):
        return ConstantMat.MATRIX_TYPES

    @property
    def _vector_types(self):
        return ConstantMat.VECTOR_TYPES

    @property
    def _type(self):
        return ConstantMat.TYPE.get(type(self))

    @property
    def width(self):
        return ConstantMat.MATRIX_WIDTH.get(type(self))

    @property
    def height(self):
        return ConstantMat.MATRIX_HEIGHT.get(type(self))

    @property
    def _size(self):
        return self.width * self.height

    _matrix = []


class Mat2(_Mat):
    @staticmethod
    def get_info():
        print("Mat2 isn't implemented yet")


class Mat3(Mat2):
    def shear_x_2d(self, s):
        if isinstance(s, self._scalar_types):
            result = Mat3(1)
            result[1][0] = s
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def shear_y_2d(self, s):
        if isinstance(s, self._scalar_types):
            result = Mat3(1)
            result[0][1] = s
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def reflect_2d(self, vec):
        if isinstance(vec, self._vector_types):
            result = Mat3(1)
            for i in range(2):
                for j in range(2):
                    result[i][j] -= 2 * vec[i] * vec[j]
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._vector_types))

    def proj_2d(self, vec):
        if isinstance(vec, self._vector_types):
            result = Mat3(1)
            for i in range(2):
                for j in range(2):
                    result[i][j] -= vec[i] * vec[j]
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._vector_types))


class Mat4(Mat3):
    def shear_x_3d(self, s, t):
        if isinstance(s, self._scalar_types):
            result = Mat4(1)
            result[0][1] = s
            result[0][2] = t
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def shear_y_3d(self, s, t):
        if isinstance(s, self._scalar_types):
            result = Mat4(1)
            result[1][0] = s
            result[1][2] = t
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def shear_z_3d(self, s, t):
        if isinstance(s, self._scalar_types):
            result = Mat4(1)
            result[2][0] = s
            result[2][1] = t
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def reflect_3d(self, vec):
        if isinstance(vec, self._vector_types):
            result = Mat4(1)
            for i in range(3):
                for j in range(3):
                    result[i][j] -= 2 * vec[i] * vec[j]
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._vector_types))

    def proj_3d(self, vec):
        if isinstance(vec, self._vector_types):
            result = Mat4(1)
            for i in range(3):
                for j in range(3):
                    result[i][j] -= vec[i] * vec[j]
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._vector_types))

    def translate(self, vec):
        if isinstance(vec, self._vector_types):
            vec = Vec4(vec.list)
            vec.w = 1
            result = Mat4(1)
            result[3] = vec
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._vector_types))

    def rotate(self, angle, vec):
        if isinstance(vec, self._vector_types):
            axis = Vec4(vec.list)
            axis.w = 1
            axis = axis.normalize()
            result = Mat4(1)
            cosinus = math.cos(angle)
            sinus = math.sin(angle)
            result[0][0] = cosinus + axis.x ** 2.0 * (1.0 - cosinus)
            result[0][1] = axis.y * axis.x * (1.0 - cosinus) + axis.z * sinus
            result[0][2] = axis.z * axis.x * (1.0 - cosinus) - axis.y * sinus
            result[1][0] = axis.x * axis.y * (1.0 - cosinus) - axis.z * sinus
            result[1][1] = cosinus + axis.y ** 2.0 * (1.0 - cosinus)
            result[1][2] = axis.z * axis.y * (1.0 - cosinus) + axis.x * sinus
            result[2][0] = axis.x * axis.z * (1.0 - cosinus) + axis.y * sinus
            result[2][1] = axis.y * axis.z * (1.0 - cosinus) - axis.x * sinus
            result[2][2] = cosinus + axis.z ** 2.0 * (1.0 - cosinus)
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._vector_types))

    def scale(self, vec):
        if isinstance(vec, self._vector_types):
            vec = Vec4(vec.list)
            vec.w = 1
            result = Mat4(1)
            for i in range(len(vec)):
                result[i][i] *= vec[i]
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._vector_types))

    def ortho(self, left, right, bottom, top, near=-1, far=-1):
        if (
            isinstance(left, self._scalar_types) and
            isinstance(right, self._scalar_types) and
            isinstance(bottom, self._scalar_types) and
            isinstance(top, self._scalar_types) and
            isinstance(near, self._scalar_types) and
            isinstance(far, self._scalar_types)
        ):
            result = Mat4(1)
            result[0][0] = 2 / (right - left)
            result[1][1] = 2 / (top - bottom)
            result[3][0] = - (right + left) / (right - left)
            result[3][1] = - (top + bottom) / (top - bottom)
            if near < 0 or far < 0:
                result[2][2] = -1
            else:
                result[2][2] = - 2 / (far - near)
                result[3][2] = - (far + near) / (far - near)
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def perspective(self, fov, aspect, near, far):
        if (
            isinstance(fov, self._scalar_types) and
            isinstance(aspect, self._scalar_types) and
            isinstance(near, self._scalar_types) and
            isinstance(far, self._scalar_types) and
            aspect - sys.float_info.epsilon > 0
        ):
            half_fov = math.tan(fov / 2)
            result = Mat4(1)
            result[0][0] = 1 / (aspect * half_fov)
            result[1][1] = 1 / half_fov
            result[2][3] = - 1
            result[2][2] = - (far + near) / (far - near)
            result[3][2] = - (2 * far * near) / (far - near)
            result = self * result
            return result
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    @staticmethod
    def look_at(eye, center, up):
        if (
            isinstance(eye, Vec3) and
            isinstance(center, Vec3) and
            isinstance(up, Vec3)
        ):
            f = (center - eye).normalize()
            s = f.cross(up).normalize()
            u = s.cross(f)
            result = Mat4(1)
            result[0][0] = s.x
            result[1][0] = s.y
            result[2][0] = s.z
            result[0][1] = u.x
            result[1][1] = u.y
            result[2][1] = u.z
            result[0][2] = - f.x
            result[1][2] = - f.y
            result[2][2] = - f.z
            result[3][0] = - eye.dot(s)
            result[3][1] = - eye.dot(u)
            result[3][2] = eye.dot(f)
            return result


class ConstantMat(Constant):
    SCALAR_TYPES = int, float
    MATRIX_TYPES = Mat2, Mat3, Mat4
    VECTOR_TYPES = Vec2, Vec3, Vec4
    TYPE = {
        _Mat: None,
        Mat2: Vec2,
        Mat3: Vec3,
        Mat4: Vec4
    }
    MATRIX_WIDTH = {
        _Mat: 0,
        Mat2: 2,
        Mat3: 3,
        Mat4: 4
    }
    MATRIX_HEIGHT = {
        _Mat: 0,
        Mat2: 2,
        Mat3: 3,
        Mat4: 4
    }
