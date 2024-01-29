from django.contrib import admin

# Register your models here.
from .models import SDCheckPoint, ThirdServer, Embedding, Lora, Sampler, Upscaler

@admin.register(SDCheckPoint)
class SDAdmin(admin.ModelAdmin):
    list_display = ('title', 'intro', 'show_name')
    list_display_links = ('title', 'intro')
    list_filter = ('title',)
    search_fields = ('title',)
    list_per_page = 10
    ordering = ('id',)
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'model_name', 'hash', 'sha256',
                       'filename', 'config')
        }),
        ('附加信息', {
            'classes': ('collapse',),
            'fields': ('cover', 'show_name', 'intro')
        })
    )


@admin.register(ThirdServer)
class ThirdServerAdmin(admin.ModelAdmin):
    readonly_fields = ('created_time', 'updated_time')
    list_display = ('name', 'intro', 'domain', 'port', 'user_num', 'updated_time', 'expire_time',
                    'checkpoint_title', 'is_alive')
    list_display_links = ('name', 'intro')
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10
    ordering = ('-created_time',)
    fieldsets = [
        ('基本信息', {
            'fields': ('name', 'intro', 'user_num',
                       'domain', 'port', 'checkpoint')
        }),
        ('时间信息', {
            'fields': ('created_time', 'updated_time', 'expire_time', 'is_alive')
        }),
    ]

    @admin.display(description='负载模型')
    def checkpoint_title(self, obj):
        return obj.checkpoint.title if obj.checkpoint else ''


@admin.register(Embedding)
class EmbeddingAdmin(admin.ModelAdmin):
    list_display = ('name', 'sd_checkpoint_name', 'intro')
    list_display_links = ('name', 'intro')
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10
    ordering = ('id',)
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'intro', 'sd_checkpoint', 'sd_checkpoint_name')
        }),
        ('附加信息', {
            'classes': ('collapse',),
            'fields': ('step', 'shape', 'vectors')
        })
    )


@admin.register(Lora)
class LoraAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias', 'cover', 'intro')
    list_display_links = ('name', 'intro')
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10
    ordering = ('id',)
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'show_name', 'cover', 'intro')
        }),
        ('附加信息', {
            'classes': ('collapse',),
            'fields': ('alias', 'path', 'metadata')
        })
    )


@admin.register(Sampler)
class SamplerAdmin(admin.ModelAdmin):
    list_display = ('name', 'aliases')
    list_display_links = ('name', )
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10
    ordering = ('id',)
    fieldsets = (
        ('基本信息', {
            'fields': ('name', )
        }),
        ('附加信息', {
            'classes': ('collapse',),
            'fields': ('aliases', 'options')
        })
    )


@admin.register(Upscaler)
class UpscalerAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_name', 'scale')
    list_display_links = ('name', )
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10
    ordering = ('id',)
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'model_name', 'scale')
        }),
        ('附加信息', {
            'classes': ('collapse',),
            'fields': ('model_path', 'model_url')
        })
    )
