from abc import abstractmethod
from api.engine.document_interfaces import HTMLLayerInterface


class HTMLBaseLayer(HTMLLayerInterface):
    content = None

    def __init__(self, data) -> None:
        layer_path = self._get_layer_path()
        
        with open(layer_path) as f:
            lines = f.readlines()
            self.content = "".join(lines)
            
        self._set_values(data)


    def _get_layer_path(self):
        return f"{self.layer_base_path}/{self.current_layer}"

    def get_layer_content(self):
        return "oi"
    
    def _set_values(self, data):
        pass