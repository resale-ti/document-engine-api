from api.common.repositories.document_repository import DocumentRepository
from api.common.repositories.manager_repository import ManagerRepository
from datetime import date, datetime
from utils.mail import Mail


class EditalLibrary:

    def inactive_documents_from_wallet_id(self, wallet_id, document_id):
        return

    def send_approved_document_email(self, wallet_id, document_id, doc_stream):
        return

    def _get_data_email(self, regulamento, doc_stream) -> dict:
        return
        
    @staticmethod
    def _get_tx_servico_min_max(imovel):
        is_cat_venda_tx_servico = (imovel.cat_venda_tx_servico_min and imovel.cat_venda_tx_servico_max)
        taxa_servico_minima = imovel.gestor_tx_servico_min if imovel.gestor_tx_servico_min else 0

        tx_servico_min = imovel.cat_venda_tx_servico_min if is_cat_venda_tx_servico else taxa_servico_minima
        tx_servico_max = imovel.cat_venda_tx_servico_max if is_cat_venda_tx_servico else 0

        return {
            "tx_servico_min": tx_servico_min,
            "tx_servico_max": tx_servico_max
        }
    
    @staticmethod
    def define_tx_servico_min_max(imovel_id):
        return EditalLibrary._get_tx_servico_min_max(ManagerRepository().get_taxa_servico(imovel_id))

