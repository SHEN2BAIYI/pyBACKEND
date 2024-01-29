import webuiapi
from genImage.models import *


def choose_suit_server_by_sdmodel(model_name):
    """
    选择合适的服务器
    """
    # 获取所有的服务器
    servers = list(ThirdServer.objects.all())
    for server in servers:
        if not server.is_alive:
            continue

        if server.checkpoint is None:
            # 没有记录负载模型，进行请求
            api = webuiapi.WebUIApi(
                host=server.domain,
                port=server.port,
            )
            # 获取负载模型
            sd_model = api.util_get_current_model()
            # 更新负载模型
            server.checkpoint = SDCheckPoint.objects.get(title=sd_model)
            server.save()

        if server.checkpoint.model_name == model_name and server.user_num == 0:
            # 如果模型名称相同，并且没有人使用，那么就选择这个服务器
            return server

    return None




