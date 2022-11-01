#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import requests


class Service(object):
    def __init__(self):
        self.base_url = os.environ.get('PAGIMOVEL_ADMIN_API_URL')
        self.headers = {"Content-Type": "application/json",
                        "Authorization": "Token " + os.environ.get('PAGIMOVEL_ADMIN_API_KEY')
                        }

    def post(self, enpoint, data) -> [dict, str]:
        """
        Envia para o carteiras-admin os dados que serão salvos no BD e/ou S3.
        @param enpoint: endpoint da opração que será realizada.
        @param data: dados que serão salvos.
        @return: Em caso de sucesso, retornará um dict com os dados. Se não, uma mensagem de erro.
        """
        url = self.base_url + enpoint
        try:
            body = json.dumps(data)

            r = requests.post(url, data=body, headers=self.headers)

            response = r.json()
        except Exception as e:
            response = str(e)

        return response


