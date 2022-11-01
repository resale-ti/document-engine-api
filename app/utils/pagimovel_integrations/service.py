#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import requests


class PagimovelIntegration(object):
    """
    Classe responsável por criar a integração com o PGI-integrations.
    """

    def __init__(self):
        """
        Responsável por criar os objetos da classe.
        """
        self.base_url = os.environ.get("PAGIMOVEL_INTEGRATIONS_URL")
        self.headers = {
            "x-api-key": os.environ.get("PAGIMOVEL_INTEGRATIONS_API_KEY")
        }

    def get(self, endpoint: str) -> dict:
        """
        Obtem os dados do PGI-integration baseado no endpoint recebido.
        @param endpoint: str com o endpoint.
        @return: dict com os dados solicitados.
        """
        url = self.base_url + endpoint

        r = requests.get(url, headers=self.headers)
        response = r.json()
        return response

    def post(self, endpoint: str, data: dict) -> dict:
        """
        irá enviar dados para o PGI-integration baseado no endpoint recebido.
        @param endpoint: str com o endpoint.
        @param data: dict com os dados que serão enviados.
        @return: Se sucesso, returno um dict com os dados. Se não, str do erro.
        """
        url = self.base_url + endpoint

        try:
            body = json.dumps(data)

            r = requests.post(url, data=body)

            response = r.json()
        except Exception as e:
            response = str(e)

        return response

    def __get_data(self, carteira_id: str, imovel_id: str, path: str) -> dict:
        """
        Obtem o endpoint que será usado na requisição.
        @param carteira_id:
        @param imovel_id:
        @param path: caminho para montar o endpoint.
        @return: dict da resposta que obteve no def get().
        """
        endpoint = "/property/{0}/{1}/{2}".format(carteira_id, imovel_id, path)

        integration_response = self.get(endpoint)
        return integration_response


    def get_values(self, carteira_id: str, imovel_id: str) -> dict:
        """
        Obtem os valores com base no ID da carteira e o ID  do imóvel.
        @param carteira_id: str com o ID da carteira.
        @param imovel_id: str com o ID do imóvel.
        @return: dict com os valores obtidos.
        """
        response_data = self.__get_data(carteira_id, imovel_id, "values")

        return {
            "valor_venda": response_data.get("valor_venda"),
            "valor_venda_campanha": response_data.get("valor_venda_campanha"),
            "valor_avaliacao": response_data.get("valor_avaliacao")
        }
