from pydantic import BaseModel, validator
import datetime


class ContractBaseSchema(BaseModel):
    contract_type: str
    id_obj: str
    requester_id: str
    origin_application: str


class RegulamentoSchema(ContractBaseSchema):
    data_inicio: str

    @validator("data_inicio")
    @classmethod
    def check_data_inicio(cls, value):
        format = "%Y-%m-%d %H:%M:%S"
        try:
            return datetime.datetime.strptime(value, format)
        except ValueError:
            raise ValueError("A data_inicio deve conter a seguinte formatação: {%Y-%m-%d %H:%M:%S}")
