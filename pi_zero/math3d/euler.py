from .matrix import *
from .constant import Constant

import math


class EulerAngle:
    def __init__(self, yaw, pitch, roll):
        if (
            isinstance(yaw, self._scalar_types) and
            isinstance(pitch, self._scalar_types) and
            isinstance(roll, self._scalar_types)
        ):
            self._yaw = yaw
            self._pitch = pitch
            self._roll = roll
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    def __repr__(self):
        return (
            'yaw = ' + str(self._yaw) +
            ', pitch = ' + str(self._pitch) +
            ', roll = ' + str(self._roll)
        )

    def __str__(self):
        return str([self._yaw, self._pitch, self._roll])

    def __len__(self):
        return 3

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (
                self.yaw == other.yaw and
                self.pitch == other.pitch and
                self.roll == other.roll
            )
        return False

    def __ne__(self, other):
        return not self == other

    def __getitem__(self, item):
        if item == 0:
            return self.yaw
        elif item == 1:
            return self.pitch
        elif item == 2:
            return self.roll
        else:
            raise TypeError('Requires ' + str(int) + ' between 0 and 2')

    def __setitem__(self, key, value):
        if key == 0:
            self.yaw = value
        elif key == 1:
            self.pitch = value
        elif key == 2:
            self.roll = value
        else:
            raise TypeError('Requires ' + str(int) + ' between 0 and 2')

    def __delitem__(self, key):
        if key == 0:
            del self._yaw
        elif key == 1:
            del self._pitch
        elif key == 2:
            del self._roll
        else:
            raise TypeError('Requires ' + str(int) + ' between 0 and 2')

    def get_rotation(self):
        cos_yaw = math.cos(self.yaw)
        sin_yaw = math.sin(self.yaw)
        cos_pitch = math.cos(self.pitch)
        sin_pitch = math.sin(self.pitch)
        cos_roll = math.cos(self.roll)
        sin_roll = math.sin(self.roll)
        result = Mat4(1)
        result[0][0] = cos_yaw * cos_roll + sin_yaw * sin_pitch * sin_roll
        result[0][1] = sin_roll * cos_pitch
        result[0][2] = - sin_yaw * cos_roll + cos_yaw * sin_pitch * sin_roll
        result[1][0] = - cos_yaw * sin_roll + sin_yaw * sin_pitch * cos_roll
        result[1][1] = cos_roll * cos_pitch
        result[1][2] = sin_roll * sin_yaw + cos_yaw * sin_pitch * cos_roll
        result[2][0] = sin_yaw * cos_pitch
        result[2][1] = - sin_pitch
        result[2][2] = cos_yaw * cos_pitch
        return result

    def get_front(self):
        return Vec3(
            math.cos(self.yaw) * math.cos(self.pitch),
            math.sin(self.pitch),
            math.sin(self.yaw) * math.cos(self.pitch)
        ).normalize()

    @staticmethod
    def get_rotation_x(angle_x):
        cos_x = math.cos(angle_x)
        sin_x = math.sin(angle_x)
        result = Mat4(1)
        result[1][1] = cos_x
        result[2][1] = sin_x
        result[1][2] = - sin_x
        result[2][2] = cos_x
        return result

    @staticmethod
    def get_rotation_y(angle_y):
        cos_y = math.cos(angle_y)
        sin_y = math.sin(angle_y)
        result = Mat4(1)
        result[0][0] = cos_y
        result[2][0] = - sin_y
        result[0][2] = sin_y
        result[2][2] = cos_y
        return result

    @staticmethod
    def get_rotation_z(angle_z):
        cos_z = math.cos(angle_z)
        sin_z = math.sin(angle_z)
        result = Mat4(1)
        result[0][0] = cos_z
        result[1][0] = sin_z
        result[0][1] = - sin_z
        result[1][1] = cos_z
        return result

    @staticmethod
    def get_rotation_xy(angle_x, angle_y):
        return EulerAngle.get_rotation_x(angle_x) * EulerAngle.get_rotation_y(angle_y)

    @staticmethod
    def get_rotation_yx(angle_y, angle_x):
        return EulerAngle.get_rotation_y(angle_y) * EulerAngle.get_rotation_x(angle_x)

    @staticmethod
    def get_rotation_xz(angle_x, angle_z):
        return EulerAngle.get_rotation_x(angle_x) * EulerAngle.get_rotation_z(angle_z)

    @staticmethod
    def get_rotation_zx(angle_z, angle_x):
        return EulerAngle.get_rotation_z(angle_z) * EulerAngle.get_rotation_x(angle_x)

    @staticmethod
    def get_rotation_yz(angle_y, angle_z):
        return EulerAngle.get_rotation_y(angle_y) * EulerAngle.get_rotation_z(angle_z)

    @staticmethod
    def get_rotation_zy(angle_z, angle_y):
        return EulerAngle.get_rotation_z(angle_z) * EulerAngle.get_rotation_y(angle_y)

    @staticmethod
    def orientate_2d(angle):
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        return Mat2(
            cos_angle, sin_angle,
            - sin_angle, cos_angle
        )

    @staticmethod
    def orientate_3d(angle):
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        result = Mat3(1)
        result[0][0] = cos_angle
        result[0][1] = sin_angle
        result[1][0] = - sin_angle
        result[1][1] = cos_angle
        return result

    @property
    def yaw(self):
        return self._yaw

    @yaw.setter
    def yaw(self, value):
        if isinstance(value, self._scalar_types):
            self._yaw = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    @property
    def pitch(self):
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        if isinstance(value, self._scalar_types):
            self._pitch = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    @property
    def roll(self):
        return self._roll

    @roll.setter
    def roll(self, value):
        if isinstance(value, self._scalar_types):
            self._roll = value
        else:
            raise TypeError('Requires ' + str(self._scalar_types))

    @property
    def _scalar_types(self):
        return ConstantEuler.SCALAR_TYPES

    _yaw = 0
    _pitch = 0
    _roll = 0


class ConstantEuler(Constant):
    SCALAR_TYPES = int, float


def to_radian(angle):
    return angle * math.pi / 180


def to_degree(angle):
    return angle * 180 / math.pi

