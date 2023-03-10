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
            return [layer.DT003_002Capa(wallet_id, data), layer.DT003_002Miolo(wallet_id, data), layer.DT003_002Rodape(wallet_id, data)]
        elif edital == "DTBNC001_001":
            return [layer.DTBNC001_001Capa(wallet_id, data), layer.DTBNC001_001Miolo(wallet_id, data), layer.DTBNC001_001Rodape(wallet_id, data)]
        elif edital == "DTDV001_001":
            return [layer.DTDV001_001Capa(wallet_id, data), layer.DTDV001_001Miolo(wallet_id, data), layer.DTDV001_001Rodape(wallet_id, data)]
        elif edital == "DTEM_001":
            return [layer.DTEM_001Capa(wallet_id, data), layer.DTEM_001Miolo(wallet_id, data), layer.DTEM_001Rodape(wallet_id, data)]
        elif edital == "DTEMG001":
            return [layer.DTEMG001Capa(wallet_id, data), layer.DTEMG001Miolo(wallet_id, data), layer.DTEMG001Rodape(wallet_id, data)]
        elif edital == "DTENF_NPL_001_004":
            return [layer.DTENF_NPL_001_004Capa(wallet_id, data), layer.DTENF_NPL_001_004Miolo(wallet_id, data), layer.DTENF_NPL_001_004Rodape(wallet_id, data)]
        elif edital == "DTPX001_001":
            return [layer.DTPX001_001Capa(wallet_id, data), layer.DTPX001_001Miolo(wallet_id, data), layer.DTPX001_001Rodape(wallet_id, data)]
        elif edital == "DTITPV001_001":
           return [layer.DTITPV001_001Capa(wallet_id, data), layer.DTITPV001_001Miolo(wallet_id, data), layer.DTITPV001_001Rodape(wallet_id, data)]
        elif edital == "DTRD001_001":
            return [layer.DTRD001_001Capa(wallet_id, data), layer.DTRD001_001Miolo(wallet_id, data), layer.DTRD001_001Rodape(wallet_id, data)]
        elif edital == "DTTRI001_001":
            return [layer.DTTRI001_001Capa(wallet_id, data), layer.DTTRI001_001Miolo(wallet_id, data), layer.DTTRI001_001Rodape(wallet_id, data)]
        elif edital == "DTCOMSPGI":
            return [layer.DTCOMSPGICapa(wallet_id, data), layer.DTCOMSPGIMiolo(wallet_id, data), layer.DTCOMSPGIRodape(wallet_id, data)]
        
        return Exception('Modelo de edital não encontrado!')
