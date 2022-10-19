from .service import Service


class AdminAPIProperty:
    def __init__(self):
        self.service = Service()
    
    def post_create_property_related_document(self, property_id, body):
        return self.service.post(f"/imovel/{property_id}/documento/", body)