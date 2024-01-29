from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from .models import *

import webuiapi

"""
    同步请求
"""
class ModelList(APIView):
    def get(self, request):
        if "model_type" not in request.query_params.keys():
            return Response(data={"msg": "缺少 model_type 参数"}, status=status.HTTP_400_BAD_REQUEST)

        # 根据 model_type 返回不同模型数据
        match request.query_params["model_type"]:
            case "sd":
                s = SDCheckPointSerializer(instance=SDCheckPoint.objects.all(), many=True)
            case "embedding":
                s = EmbeddingSerializer(instance=Embedding.objects.all(), many=True)
            case "lora":
                s = LoraSerializer(instance=Lora.objects.all(), many=True)
            case "upscaler":
                s = UpscalerSerializer(instance=Upscaler.objects.all(), many=True)
            case "sampler":
                s = SamplerSerializer(instance=Sampler.objects.all(), many=True)
            case _:
                return Response(data={"msg": "模型类型错误"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=s.data, status=status.HTTP_200_OK)


"""
    内部请求
"""
class RenewList(APIView):
    def post(self, request):
        def clean_and_create(obj_cls, items):
            # 删除表中所有的数据
            obj_cls.objects.all().delete()
            # 保存数据
            if isinstance(items, list):
                for item in items:
                    # 创建模型并保存
                    sd = obj_cls(
                        **item
                    )
                    sd.save()
            elif isinstance(items, dict):
                if "loaded" in items.keys():
                    for item_name, item_value in items["loaded"].items():
                        # 创建模型并保存
                        sd = obj_cls(
                            name=item_name,
                            **item_value
                        )
                        sd.save()

        # 验证
        s = RenewSerializer(data=request.data)
        if not s.is_valid():
            return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)

        # 获取ThirdServer的第一个对象
        third_server = ThirdServer.objects.first()
        # 创建 api
        api = webuiapi.WebUIApi(
            host=third_server.domain,
            port=third_server.port,
        )

        # 进行请求
        match s.validated_data['renew_type']:
            case 'sd':
                clean_and_create(SDCheckPoint, api.get_sd_models())
            case 'embedding':
                clean_and_create(Embedding, api.get_embeddings())
            case 'lora':
                clean_and_create(Lora, api.get_loras())
            case 'upscaler':
                clean_and_create(Upscaler, api.get_upscalers())
            case 'sampler':
                clean_and_create(Sampler, api.get_samplers())
            case 'all':
                clean_and_create(SDCheckPoint, api.get_sd_models())
                clean_and_create(Embedding, api.get_embeddings())
                clean_and_create(Lora, api.get_loras())
                clean_and_create(Upscaler, api.get_upscalers())
                clean_and_create(Sampler, api.get_samplers())

            case _:
                return Response(data={"msg": "renew_type 参数错误"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={
            "msg": "更新成功"
        }, status=status.HTTP_200_OK)
