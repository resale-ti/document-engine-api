import unittest
from api.contract.contract_enum import EnumContractType
from tests.common.mocks.enums_mock import ENUMS_MOCK


class ContractEnumTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs) -> None:
        super(ContractEnumTestCase, self).__init__(*args, **kwargs)
        self.enum_list = [ect for ect in EnumContractType]

    def test_contract_enum_match(self):
        for ect in self.enum_list:
            self.assertEqual(ect.value, ENUMS_MOCK.get(ect.name))


if __name__ == '__main__':
    unittest.main()
