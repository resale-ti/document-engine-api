from api.common.rollback.regulamento_rollback import RegulamentoRollback

class RollbackFactory:

    def get_instance(self, contract_type, data):
        if contract_type == "regulamento_concorrencia":
            return RegulamentoRollback(task_payload=data)

        raise Exception(f"Nenhum Rollback está parametrizado para o contract_type: {contract_type}")
