#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import requests


class CarteirasIntegration(object):

    def __init__(self):
        self.base_url = os.environ.get("CARTEIRAS_URL")

    def post(self, url, data):
        url = self.base_url + url

        try:
            body = json.dumps(data)

            r = requests.post(url=url, data=body)

            response = r.json()
        except Exception as e:
            response = str(e)

        return response

    def get_condicoes_pagamentos(self, property_id):
        url = f"/integration/generate_condicoes_pagamento/{property_id}"

        data = {
            "condicoes_pagamento": property_id
        }

        r = self.post(url=url, data=data)

        return r.get("condicoes_pagamento")
