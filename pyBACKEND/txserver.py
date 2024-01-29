from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from PIL import Image

import os
import io
import random
import string


# TX云密钥
SECRET_ID_TX = "AKIDIaqaBkCUbaR8NhHNpOWkZUsNEZuw2885"
SECRET_KEY_TX = "9GUXhojYN5vgS6qquBWtR0pprjgOCACj"
REGION_TX = "ap-nanjing"
SCHEME_TX = "https"
BUCKET_TX = "morefun-1302194859"


class TXServer:
    def __init__(self):
        self.server = None

    @staticmethod
    def gen_random_string():
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 20))
        return ran_str

    def create_tx_server(self):
        config = CosConfig(Region=REGION_TX, SecretId=SECRET_ID_TX,
                           SecretKey=SECRET_KEY_TX, Scheme=SCHEME_TX)

        self.server = CosS3Client(config)

    def upload_file(self, img: Image):
        # PIL 转 bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # 根据年月日时间创建文件名
        filename = '{}.png'.format(TXServer.gen_random_string())

        self.server.put_object(
            Bucket=BUCKET_TX,
            Body=img_byte_arr,
            Key=filename,
            StorageClass='STANDARD',
            EnableMD5=False
        )

        return '{}://{}.cos.{}.myqcloud.com/{}'.format(
            SCHEME_TX, BUCKET_TX, REGION_TX, filename
        )


tx_server = TXServer()
