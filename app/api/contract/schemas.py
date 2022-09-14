from pydantic import BaseModel


class ContractSchema(BaseModel):
    contract_type: str
    id_obj: str
    requester_id: str
    origin_application: str

