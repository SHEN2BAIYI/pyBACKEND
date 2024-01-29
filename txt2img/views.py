from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from pyBACKEND.utils import choose_suit_server_by_sdmodel
from pyBACKEND.txserver import tx_server
from .serializers import *
from .tasks import add

from kombu import Exchange

import webuiapi
import requests

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyBACKEND.settings')

"""
    同步请求
"""
class Txt2Img(APIView):
    def post(self, request):
        # 验证
        s = Txt2ImgSerializer(data=request.data)
        if not s.is_valid():
            return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)

        # 选择合适的第三方服务器
        server = choose_suit_server_by_sdmodel(s.validated_data["model"])

        if server:
            # 向第三方服务器发送请求
            api = webuiapi.WebUIApi(
                host=server.domain,
                port=server.port,
            )
            s.validated_data.pop("model")
            try:
                res = api.txt2img(**s.validated_data)
            except requests.exceptions.ProxyError:
                return Response(data={"msg": "网络错误，请稍后重试。"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            files_url = []
            # 上传图片到腾讯云
            if not tx_server.server:
                print("创建腾讯云对象")
                tx_server.create_tx_server()
            for image in res.images:
                file_url = tx_server.upload_file(image)
                if not file_url:
                    return Response(data={"msg": "网络错误，请稍后重试。"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                files_url.append(file_url)

            return Response(data=files_url, status=status.HTTP_200_OK)


@api_view(['GET'])
def my_test(request):
    result = add.apply_async(args=[1, 2], queue='feed')
    return Response(data={"msg": result.get()}, status=status.HTTP_200_OK)


