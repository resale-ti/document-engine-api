import unittest
from api.contract.regulamento_concorrencia.regulamento_builder import RegulamentoConcorrenciaBuilder
from tests.regulamento_concorrencia.mocks.without_wallet_id_mock import WITHOUT_WALLET_ID_MOCK


class RegulamentoBuilderTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs) -> None:
        super(RegulamentoBuilderTestCase, self).__init__(*args, **kwargs)

    def test_regulamento_builder_exception(self):
        with self.assertRaises(Exception):
            RegulamentoConcorrenciaBuilder(data=WITHOUT_WALLET_ID_MOCK)


if __name__ == '__main__':
    unittest.main()
