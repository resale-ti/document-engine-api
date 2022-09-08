from api.contract.layers_base import HTMLBaseLayer


class RegulamentoDefaultLayer(HTMLBaseLayer):
    layer_base_path = "static/templates/regulamento_concorrencia"


class MLP002CapaLayer(RegulamentoDefaultLayer):
    current_layer = "MLP_002/capa.html"