import api.contract.edital.edital_layers as layer


class EditalFactory:

    def get_instance(self, wallet_id, data):
        edital = data.get("EDITAL")

        if edital == "DTBB001":
            return [layer.DTBB001Capa(wallet_id, data), layer.DTBB001Miolo(wallet_id, data), layer.DTBB001Rodape(wallet_id, data)]
        elif edital == "DTBB002":
            return [layer.DTBB002Capa(wallet_id, data), layer.DTBB002Miolo(wallet_id, data), layer.DTBB002Rodape(wallet_id, data)]
        elif edital == "DTBB003":
            return [layer.DTBB003Capa(wallet_id, data), layer.DTBB003Miolo(wallet_id, data), layer.DTBB003Rodape(wallet_id, data)]
        elif edital == "DTBB004":
            return [layer.DTBB004Capa(wallet_id, data), layer.DTBB004Miolo(wallet_id, data), layer.DTBB004Rodape(wallet_id, data)]
        elif edital == "DTBB005":
            return [layer.DTBB005Capa(wallet_id, data), layer.DTBB005Rodape(wallet_id, data)]
        elif edital == "DTBB006":
            return [layer.DTBB006Capa(wallet_id, data), layer.DTBB006Miolo(wallet_id, data), layer.DTBB006Rodape(wallet_id, data)]
        elif edital == "DT003_002":
            return []
        elif edital == "DTBNC001_001":
            return []
        elif edital == "DTDV001_001":
            return []
        elif edital == "DTEM_001":
            return []
        elif edital == "DTEMG001":
            return []
        elif edital == "DTENF_NPL_001_004":
            return []
        elif edital == "DTITPV001_001":
            return []
        elif edital == "DTRD001_001":
            return []
        elif edital == "DTTRI001_001":
            return []
        
            

        return ""
