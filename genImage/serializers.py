from rest_framework import serializers
from .models import *

class SDCheckPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = SDCheckPoint
        fields = ('model_name', 'show_name', 'intro', 'cover')
        ordering = ('model_name',)


class LoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lora
        fields = ('name', 'show_name', 'intro', 'cover')
        ordering = ('name',)


class EmbeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Embedding
        fields = ('name', 'intro')
        ordering = ('name',)


class UpscalerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upscaler
        fields = ('name', )
        ordering = ('name',)


class SamplerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sampler
        fields = ('name', )
        ordering = ('name',)


class RenewSerializer(serializers.Serializer):
    # 只是进行简单的验证
    renew_type = serializers.ChoiceField(choices=['sd', 'lora', 'embedding', 'upscaler', 'sampler', 'all'])

