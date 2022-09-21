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

    @validator("data_inicio")
    @classmethod
    def check_data_inicio(cls, value):
        format = "%d-%m-%Y %H:%M"
        try:
            return datetime.datetime.strptime(value, format)
        except ValueError:
            raise ValueError("A data_inicio deve conter a seguinte formatação: {%d-%m-%Y %H:%M}")
