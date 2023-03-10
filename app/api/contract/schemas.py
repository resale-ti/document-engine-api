from pydantic import BaseModel, validator
from typing import Optional
import datetime


class ContractBaseSchema(BaseModel):
    contract_type: str
    id_obj: str
    requester_id: str
    origin_application: str
    manager_id: Optional[str] = None
    
class RegulamentoSchema(ContractBaseSchema):
    data_inicio: str
    data_fim: str

    @validator("data_inicio", "data_fim")
    @classmethod
    def check_data_inicio(cls, field_value, values, field, config):
        format = "%d-%m-%Y %H:%M"
        try:
            return datetime.datetime.strptime(field_value, format)
        except ValueError:
            raise ValueError(f"A {field.name} deve conter a seguinte formatação: {format}")

class CertificadoVendaSchema(ContractBaseSchema):
    property_id: str
    
    
class EditalSchema(ContractBaseSchema):
    contact_id: str
    manager_charge_id: Optional[str] = '0'