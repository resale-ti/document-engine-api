from api.contract.regulamento_concorrencia.regulamento_layers import MLP002Capa, MLP002Miolo, MLP002Rodape

class RegulamentoDocumentsFactory:

    def get_instance(self, wallet_id, data):
        regulamento_type = data.get("regulamento")

        if regulamento_type == "MLP_002":
            return [MLP002Capa(wallet_id, data), MLP002Miolo(wallet_id, data), MLP002Rodape(wallet_id, data)]

        return ""
