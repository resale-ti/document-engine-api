from api.contract.regulamento_concorrencia.regulamento_layers import MLP002Capa, MLP002Miolo, MLP002Rodape, MLPVA001Capa, MLPVA001Miolo, MLPVA001Rodape

class RegulamentoDocumentsFactory:

    def get_instance(self, wallet_id, data):
        regulamento_type = data.get("regulamento")

        if regulamento_type == "MLP_002":
            return [MLP002Capa(wallet_id, data), MLP002Miolo(wallet_id, data), MLP002Rodape(wallet_id, data)]
        elif regulamento_type == "MLPVA_001":
            return [MLPVA001Capa(wallet_id, data), MLPVA001Miolo(wallet_id, data), MLPVA001Rodape(wallet_id, data)]
        return ""
