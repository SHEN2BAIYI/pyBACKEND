from django.conf import settings
from django.db import models

from pyBACKEND.settings import STATICFILES_DIRS

import os

class ThirdServer(models.Model):
    name = models.CharField(max_length=40, verbose_name='第三方服务器名称', help_text='第三方服务器名称')
    intro = models.TextField(verbose_name='第三方服务器简介', help_text='第三方服务器简介', blank=True, null=True)

    # 状态类型
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    expire_time = models.DateTimeField(verbose_name='过期时间', help_text='过期时间')
    is_alive = models.BooleanField(default=True, verbose_name='是否可用', help_text='是否可用')

    # 域名和端口
    domain = models.CharField(max_length=40, verbose_name='域名', help_text='域名')
    port = models.IntegerField(verbose_name='端口', help_text='端口')

    # 一对多关系
    checkpoint = models.ForeignKey('SDCheckPoint', on_delete=models.SET_NULL,
                                   verbose_name='SD模型', help_text='SD模型', null=True)

    user_num = models.IntegerField(verbose_name='用户数量', help_text='用户数量', default=0, null=True)

    class Meta:
        verbose_name = '第三方服务器'
        verbose_name_plural = verbose_name
        ordering = ('-created_time',)

    def __str__(self):
        return self.name


class SDCheckPoint(models.Model):
    # api 请求
    title = models.CharField(max_length=50, verbose_name='SD模型全称', help_text='SD模型全称')
    model_name = models.CharField(max_length=40, verbose_name='SD模型名称', help_text='SD模型名称')
    hash = models.CharField(max_length=40, verbose_name='SD模型哈希值', help_text='SD模型哈希值')
    sha256 = models.CharField(max_length=100, verbose_name='SD模型SHA256值', help_text='SD模型SHA256值')
    filename = models.CharField(max_length=100, verbose_name='SD模型文件名', help_text='SD模型文件名', blank=True, null=True)
    config = models.JSONField(verbose_name='SD模型配置', help_text='SD模型配置', blank=True, null=True)

    intro = models.TextField(verbose_name='SD模型简介', help_text='SD模型简介', blank=True, null=True)
    cover = models.ImageField(upload_to=os.path.join(STATICFILES_DIRS[0], 'cover/SD/',),
                              verbose_name='封面图片', help_text='封面图片', blank=True, null=True)
    show_name = models.CharField(max_length=40, verbose_name='SD模型展示名称', help_text='SD模型展示名称', blank=True, null=True)

    class Meta:
        verbose_name = 'SD'
        verbose_name_plural = verbose_name
        ordering = ('id',)


class Lora(models.Model):
    # api 请求
    name = models.CharField(max_length=40, verbose_name='Lora模型名称', help_text='Lora模型名称')
    alias = models.CharField(max_length=40, verbose_name='Lora模型别名', help_text='Lora模型别名', blank=True, null=True)
    path = models.CharField(max_length=100, verbose_name='Lora模型路径', help_text='Lora模型路径', blank=True, null=True)
    metadata = models.JSONField(verbose_name='Lora模型元数据', help_text='Lora模型元数据', blank=True, null=True)

    intro = models.TextField(verbose_name='Lora模型简介', help_text='Lora模型简介', blank=True, null=True)
    cover = models.ImageField(upload_to=os.path.join(STATICFILES_DIRS[0], 'cover/Lora/',),
                              verbose_name='封面图片', help_text='封面图片', blank=True, null=True)
    show_name = models.CharField(max_length=40, verbose_name='Lora模型展示名称', help_text='Lora模型展示名称', blank=True, null=True)

    class Meta:
        verbose_name = 'Lora'
        verbose_name_plural = verbose_name
        ordering = ('id',)


class Embedding(models.Model):
    # api 请求
    name = models.CharField(max_length=40, verbose_name='Embedding模型名称', help_text='Embedding模型名称')
    step = models.IntegerField(verbose_name='Embedding模型步长', help_text='Embedding模型步长', null=True)
    sd_checkpoint = models.CharField(max_length=40, verbose_name='SD模型哈希值', help_text='SD模型哈希值', null=True)
    sd_checkpoint_name = models.CharField(max_length=40, verbose_name='SD模型名称', help_text='SD模型名称', null=True)
    shape = models.CharField(max_length=40, verbose_name='Embedding模型形状', help_text='Embedding模型形状', null=True)
    vectors = models.IntegerField(verbose_name='Embedding模型向量数', help_text='Embedding模型向量数', null=True)

    intro = models.TextField(verbose_name='Embedding模型简介', help_text='Embedding模型简介', blank=True, null=True)

    class Meta:
        verbose_name = 'Embedding'
        verbose_name_plural = verbose_name
        ordering = ('id',)


class Sampler(models.Model):
    # api 请求
    name = models.CharField(max_length=40, verbose_name='Sampler名称', help_text='Sampler名称')
    aliases = models.JSONField(verbose_name='Sampler别名', help_text='Sampler别名', blank=True, null=True)
    options = models.JSONField(verbose_name='Sampler选项', help_text='Sampler选项', blank=True, null=True)

    class Meta:
        verbose_name = 'Sampler'
        verbose_name_plural = verbose_name
        ordering = ('id',)


class Upscaler(models.Model):
    # api 请求
    name = models.CharField(max_length=40, verbose_name='Upscaler名称', help_text='Upscaler名称')
    model_name = models.CharField(max_length=40, verbose_name='Upscaler模型名称', help_text='Upscaler模型名称', null=True)
    model_path = models.CharField(max_length=100, verbose_name='Upscaler模型路径', help_text='Upscaler模型路径', null=True)
    model_url = models.CharField(max_length=100, verbose_name='Upscaler模型URL', help_text='Upscaler模型URL', null=True)
    scale = models.FloatField(verbose_name='Upscaler放大倍数', help_text='Upscaler放大倍数')

    class Meta:
        verbose_name = 'Upscaler'
        verbose_name_plural = verbose_name
        ordering = ('id',)
