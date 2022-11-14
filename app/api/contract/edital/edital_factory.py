from api.contract.regulamento_concorrencia.regulamento_layers import MLP002Capa, MLP002Miolo, MLP002Rodape

class EditalFactory:

    def get_instance(self, wallet_id, data):
        edital = data.get("edital")

        if edital == "DTBB001":
            return []
        elif edital == "DTBB002":
            return []
        elif edital == "DTBB003":
            return []
        elif edital == "DTBB004":
            return []

        return ""
