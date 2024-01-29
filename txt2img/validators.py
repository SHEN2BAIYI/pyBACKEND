from rest_framework import serializers


class DecimalValidator:
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        # 判断是否能整除 base
        if value % self.base != 0:
            print(value, self.base, value % self.base)
            raise serializers.ValidationError(f"必须是 {self.base} 的整数倍")

    def set_context(self, serializer_field):
        pass
