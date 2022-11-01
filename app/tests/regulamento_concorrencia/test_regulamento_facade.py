import unittest
from api.contract.regulamento_concorrencia.regulamento_facade import RegulamentoConcorrenciaFacade
from app.tests.regulamento_concorrencia.mocks.objects_mock import *

class RegulamentoFacadeTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs) -> None:
        super(RegulamentoFacadeTestCase, self).__init__(*args, **kwargs)
        self.facade_obj = RegulamentoConcorrenciaFacade(
            wallet=WALLET_MOCK,
            payment_methods=PAYMENT_METHODS_MOCK,
            properties=PROPERTY_MOCK,
            regulamento_dates=REGULAMENTO_DATES_MOCK,
            qualificacao=QUALIFICACAO_MOCK
        )

    # ---------------------------------- BASE DATA --------------------------------------------------- #
    def test_regulamento_facade_get_base_data_keys(self):
        default_base_data_keys = ['regulamento', 'N_REGULAMENTO', 'TAXA_SERVICO',
                                  'QUALIFICACAO_VENDEDORES', 'PORTAL_VENDEDOR',
                                  'TAXA_INTERMEDIACAO', 'DATA_ATUAL']

        base_data = self.facade_obj._get_base_data()
        for bd_key in base_data.keys():
            self.assertTrue(bd_key in default_base_data_keys)

    # ---------------------------------- PAYMENT METHODS --------------------------------------------- #
    def test_regulamento_facade_get_payment_methods_keys(self):
        default_payment_methods = ['CONDICAO_VISTA', 'CONDICOES_PAGAMENTO_VISTA',
                                   'CONDICAO_PARCELADO', 'CONDICOES_PAGAMENTO_PARCELADO']

        payment_methods = self.facade_obj._get_payment_methods()
        for pm_key in payment_methods.keys():
            self.assertTrue(pm_key in default_payment_methods)

    def test_regulamento_facade_get_payment_desc_vista(self):
        for method in self.facade_obj.payment_methods:
            if method.get("tipo_condicao") == "vista":
                desc_vista = self.facade_obj._get_payment_desc_vista(
                    method=method)
                self.assertEqual(
                    desc_vista, '100% do pagamento na emissão do CCV (Contrato de Compra e Venda)')

    def test_regulamento_facade_get_payment_desc_parcelado(self):
        for method in self.facade_obj.payment_methods:
            if method.get("tipo_condicao") == "parcelado":
                desc_parcelado = self.facade_obj._get_payment_desc_parcelado(
                    method=method)
                self.assertEqual(
                    desc_parcelado, '30% de entrada e saldo em até 3 parcelas')

    # ---------------------------------- DATAS CONCORRENCIA --------------------------------------------- #

    def test_regulamento_facade_get_datas_concorrencia_keys(self):
        default_datas_concorrencia = ['DATA_INICIO', 'HORA_INICIO',
                                      'DATA_FIM', 'HORA_FIM']

        datas_concorrencia = self.facade_obj._get_datas_concorrencia()
        for dc_key in datas_concorrencia.keys():
            self.assertTrue(dc_key in default_datas_concorrencia)

    def test_regulamento_facade_get_datas_concorrencia_return_object_str(self):
        datas_concorrencia = self.facade_obj._get_datas_concorrencia()
        for dc_values in datas_concorrencia.values():
            self.assertEqual(dc_values.__class__, str)

    def test_regulamento_facade_get_datas_concorrencia_correct_format(self):
        data_format = "%d/%m/%Y"
        hora_format = "%H:%M"

        datas_concorrencia = self.facade_obj._get_datas_concorrencia()
        for dc_key, dc_value in datas_concorrencia.items():
            if dc_key in ["DATA_INICIO", "DATA_FIM"]:
                self.assertIsInstance(datetime.datetime.strptime(
                    dc_value, data_format), datetime.datetime)

            if dc_key in ["HORA_INICIO", "HORA_FIM"]:
                self.assertIsInstance(datetime.datetime.strptime(
                    dc_value, hora_format), datetime.datetime)

    # ---------------------------------- IMOVEIS --------------------------------------------- #
    def test_regulamento_facade_get_imoveis_data_keys(self):
        default_imoveis_data_keys = ["LOTE", "ID_BANCO", "DESCRICAO_LEGAL",
                                     "CONSIDERACOES_IMPORTANTES", "LANCE_MINIMO"]

        imoveis_data = self.facade_obj._get_imoveis_data()

        for id_key in imoveis_data.get("imoveis")[0].keys():
            self.assertTrue(id_key in default_imoveis_data_keys)


if __name__ == '__main__':
    unittest.main()
