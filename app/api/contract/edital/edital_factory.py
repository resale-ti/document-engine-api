import api.contract.edital.edital_layers as layer

class EditalFactory:

    def get_instance(self, wallet_id, data):
        edital = data.get("edital")

        if edital == "DTBB001":
            return [layer.DTBB001Capa(wallet_id, data), layer.DTBB001Miolo(wallet_id, data), layer.DTBB001Rodape()]
        elif edital == "DTBB002":
            return [layer.DTBB001Capa(wallet_id, data), layer.DTBB001Miolo(wallet_id, data), layer.DTBB001Rodape(wallet_id, data)]
        elif edital == "DTBB003":
            return [layer.DTBB001Capa(wallet_id, data), layer.DTBB001Miolo(wallet_id, data), layer.DTBB001Rodape()]
        elif edital == "DTBB004":
            return [layer.DTBB001Capa(wallet_id, data), layer.DTBB001Miolo(wallet_id, data), layer.DTBB001Rodape()]
        elif edital == "DTBB005":
            return [layer.DTBB001Capa(wallet_id, data), layer.DTBB001Miolo(wallet_id, data), layer.DTBB001Rodape()]
        elif edital == "DTBB006":
            return [layer.DTBB001Capa(wallet_id, data), layer.DTBB001Miolo(wallet_id, data), layer.DTBB001Rodape()]

        return ""
