import json
import os
import requests


class WuzuService(object):

    def __init__(self, type_vault):
        self.wuzu_url = os.environ.get("WUZU_URL") if type_vault == 'wuzu' else os.environ.get("PAGIMOVEL_MP_URL")
        self.api_key =  os.environ.get("WUZU_API_KEY") if type_vault == 'wuzu' else os.environ.get("PAGIMOVEL_MP_API_KEY")
        
        self.headers = {"Content-Type": "application/json",
                        "x-api-key": self.api_key}

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



