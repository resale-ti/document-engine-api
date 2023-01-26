from api.common.repositories.manager_repository import ManagerRepository


class EditalLibrary:
        
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

