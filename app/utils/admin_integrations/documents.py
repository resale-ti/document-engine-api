from .service import Service


class AdminAPIDocuments:
    def __init__(self):
        self.service = Service()

    def post_create_document(self, data: dict):
        return self.service.post(f"/documento/", data)
