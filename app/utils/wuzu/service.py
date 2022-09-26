import json
import os
import requests


class WuzuService(object):

    def __init__(self, *args, **kwargs):
        self.wuzu_url = os.environ.get("WUZU_URL")
        self.headers = {"Content-Type": "application/json",
                        "Authorization": "Token " + os.environ.get("WUZU_API_KEY")
                        }

    def call_wuzu(self, enpoint, data, method="post") -> [dict, str]:
        """
        Envia para o carteiras-admin os dados que serão salvos no BD e/ou S3.
        @param enpoint: endpoint da opração que será realizada.
        @param data: dados que serão salvos.
        @return: Em caso de sucesso, retornará um dict com os dados. Se não, uma mensagem de erro.
        """
        url = self.base_url + enpoint
        try:
            body = json.dumps(data)

            caller = getattr(requests, method)

            r = caller(url, data=body, headers=self.headers)

            response = r.json()
        except Exception as e:
            response = str(e)

        return response



