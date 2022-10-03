from app.api.contract.schemas import ContractBaseSchema


class CertificadoVendaBuilder(ContractBaseSchema):
    
    def build(self) -> None:
        return self