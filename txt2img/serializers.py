from rest_framework import serializers
from genImage.models import *
from .validators import DecimalValidator


# txt2img
class Txt2ImgSerializer(serializers.Serializer):
    model = serializers.ChoiceField(choices=[x.model_name for x in SDCheckPoint.objects.all()])
    prompt = serializers.CharField(max_length=1000)
    negative_prompt = serializers.CharField(max_length=1000)
    seed = serializers.IntegerField(min_value=-1, max_value=10000000000, required=False)
    cfg_scale = serializers.DecimalField(min_value=1, max_value=30, decimal_places=1, max_digits=3,
                                         validators=[DecimalValidator(0.5)], required=False)

    batch_size = serializers.IntegerField(min_value=1, max_value=6, required=False)
    n_iter = serializers.IntegerField(min_value=1, max_value=6, required=False)
    width = serializers.IntegerField(min_value=64, max_value=2048)
    height = serializers.IntegerField(min_value=64, max_value=2048)

    override_settings = serializers.JSONField(required=False)
    override_settings_restore_afterwards = serializers.BooleanField(required=False)
    alwayson_script = serializers.JSONField(required=False)

    # face restore and tilling
    restore_faces = serializers.BooleanField(required=False)
    tilling = serializers.BooleanField(required=False)

    # 差异种子
    sub_seed = serializers.IntegerField(min_value=0, max_value=10000000000, required=False)
    sub_seed_strength = serializers.DecimalField(min_value=0, max_value=1, required=False,
                                                 decimal_places=2, max_digits=3)
    seed_resize_from_h = serializers.IntegerField(min_value=0, max_value=2048, required=False)
    seed_resize_from_w = serializers.IntegerField(min_value=0, max_value=2048, required=False)

    # 采样器
    sampler_name = serializers.ChoiceField(choices=[x.name for x in Sampler.objects.all()], required=False)
    steps = serializers.IntegerField(min_value=1, max_value=150, required=False)

    # 通用设置
    do_not_save_samples = serializers.BooleanField(required=False, default=True)
    do_not_save_grid = serializers.BooleanField(required=False, default=True)
    eta = serializers.DecimalField(min_value=0, max_value=1, required=False, decimal_places=2, max_digits=3)
    disable_extra_network = serializers.BooleanField(required=False)

    # 高清修复
    enable_hr = serializers.BooleanField(required=False)
    denoising_strength = serializers.DecimalField(min_value=0, max_value=1, required=False,
                                                  decimal_places=2, max_digits=3)
    # hr_scale = serializers.DecimalField(min_value=1, max_value=4, required=False,
    #                                     decimal_places=2, max_digits=3, validators=[DecimalValidator(0.05)])
    hr_scale = serializers.FloatField(min_value=1, max_value=4, required=False)
    hr_upscaler = serializers.ChoiceField(choices=[x.name for x in Upscaler.objects.all()], required=False)
    hr_second_pass_steps = serializers.IntegerField(min_value=0, max_value=150, required=False)
    hr_resize_x = serializers.IntegerField(min_value=0, max_value=2048, required=False)
    hr_resize_y = serializers.IntegerField(min_value=0, max_value=2048, required=False)

    # refiner
    refiner_checkpoint = serializers.ChoiceField(choices=[x.model_name for x in SDCheckPoint.objects.all()],
                                                 required=False)
    refiner_switch_at = serializers.DecimalField(min_value=0.01, max_value=1,
                                                 required=False, decimal_places=2, max_digits=3)

