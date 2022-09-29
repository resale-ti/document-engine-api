import json
import os
import requests


class WuzuService(object):

    def __init__(self, *args, **kwargs):
        self.wuzu_url = os.environ.get("WUZU_URL")
        self.headers = {"Content-Type": "application/json",
                        "x-api-key": os.environ.get("WUZU_API_KEY")}

    def call_wuzu(self, endpoint, data, method="post"):
        """
        Envia para o carteiras-admin os dados que serão salvos no BD e/ou S3.
        @param enpoint: endpoint da opração que será realizada.
        @param data: dados que serão salvos.
        @return: Em caso de sucesso, retornará um dict com os dados. Se não, uma mensagem de erro.
        """
        url = self.wuzu_url + endpoint
        try:
            body = json.dumps(data)

            r = requests.post(url, data=body, headers=self.headers)

            response = r.json()
        except Exception as e:
            response = str(e)

        return response



