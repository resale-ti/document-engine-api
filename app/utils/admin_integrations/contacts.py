from .service import Service


class AdminAPIContacts:
    def __init__(self):
        self.service = Service()

    def post_create_contact_related_document(self, contact_id, body):
        return self.service.post(f"/contato/{contact_id}/documento/", body)