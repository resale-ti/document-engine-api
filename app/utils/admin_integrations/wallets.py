from .service import Service


class AdminAPIWallets:
    def __init__(self):
        self.service = Service()

    def post_create_wallet_related_document(self, wallet_id, body):
        return self.service.post(f"/carteira/{wallet_id}/documento/", body)
