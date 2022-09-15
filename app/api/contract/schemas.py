from pydantic import BaseModel


class ContractBaseSchema(BaseModel):
    contract_type: str
    id_obj: str
    requester_id: str
    origin_application: str
