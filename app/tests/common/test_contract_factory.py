import unittest
import os

from api.contract.contract_factory import ContractFactory
from api.contract.regulamento_concorrencia.regulamento_builder import RegulamentoConcorrenciaBuilder
from api.contract.certificado_venda.certificado_builder import CertificadoVendaBuilder
from tests.common import PATH_CONTRACTS


class ContractFactoryTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super(ContractFactoryTestCase, self).__init__(*args, **kwargs)
        self.factory = ContractFactory()
        self.data = {"property_id": 1, "wallet_id": 1, "id_obj": 1}
        self.switch = {"certificado_venda": CertificadoVendaBuilder(data=self.data),
                       "regulamento_concorrencia": RegulamentoConcorrenciaBuilder(data=self.data)}

    def test_contract_factory_instace_by_folder(self):
        """
        Testando a seguinte regra:

        As pastas onde serão desenvolvidas as coisas relativas ao contrato (Builder, Facade...) deverá obrigatoriamente
        possuir o nome do contract_type. Exemplo: contract_type="regulamento_concorrencia -> nome da pasta
        então deverá ser: "regulamento_concorrencia" no path: app/api/contract/.
        """
        directorys = []

        for file in os.listdir(PATH_CONTRACTS):
            d = os.path.join(PATH_CONTRACTS, file)
            if os.path.isdir(d) and d.split('/')[-1] != "__pycache__":
                directorys.append(d.split('/')[-1])

        for contract_type in directorys:
            contract = self.factory.get_instance(
                contract_type=contract_type, data=self.data)
            self.assertEqual(contract.__class__,
                             self.switch.get(contract_type).__class__)


if __name__ == '__main__':
    unittest.main()
