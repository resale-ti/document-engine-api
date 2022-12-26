from api.common.database_common import DBSessionContext
from api.common.models import Wallet, Property, Manager, Schedule, DisputaWuzu, WalletProperty, WalletSchedule, WalletManager
from sqlalchemy import func, and_, or_


class WalletRepository(DBSessionContext):
    def get_wallet_details(self, wallet_id: str):
        with self.get_session_scope() as session:
            wallet = session.query(
                Wallet.nome,
                Wallet.id,
                Wallet.aceita_valor_abaixo,
                Wallet.porcentagem_valor_abaixo,
                Wallet.honorarios_entrada,
                Wallet.forma_pagamento_id,
                Wallet.tx_comissao,
                Wallet.tipo_comissao,
                Wallet.quem_paga_comissao,
                Wallet.opcoes_call_to_action,
                Wallet.forma_pagamento_id,
                Wallet.display_places,
                Wallet.tipo_de_venda,
                Wallet.exibir_contrato_acordo,
                Wallet.formato_venda,
                Wallet.momento_pagamento_comissao,
                Wallet.quem_recebe_comissao,
                Wallet.status,
                Wallet.is_venda_condicional,
                Wallet.is_exclusiva,
                Wallet.tx_gerenciamento,
                Wallet.tx_servico,
                Wallet.tipo_valor_exibicao_portal,
                Wallet.tipo_valor_desagio,
                Wallet.exibir_comissao_portal,
                Wallet.tipo_valor_avaliacao,
                Wallet.quem_recebe_servico,
                Wallet.momento_pagamento_servico,
                Wallet.quem_paga_servico,
                Wallet.aceita_fgts,
                Wallet.tx_fgts,
                Wallet.origem_imoveis,
                Wallet.leiloeiro_gera_dados,
                Wallet.numero_leilao,
                Wallet.modelo_edital,
                Wallet.codigo,
                Wallet.campanha_exclusiva,
                Wallet.disputa_id,
                Wallet.is_disputa_concluida,
                Wallet.modelo_regulamento,
                Wallet.tx_servico,
                Wallet.tipo_concorrencia,
                Wallet.aceita_cupom,
                Wallet.cupom_nome,
                Wallet.cupom_desconto,
                Wallet.cupom_data_inicio,
                Wallet.cupom_data_final,
                Wallet.cupom_inativado,
                Wallet.data_inicio_campanha,
                Wallet.data_fim_campanha).filter(Wallet.id == wallet_id).one()

            return wallet

    def get_wallet_gestor_detail(self, wallet_id: str):
        with self.get_session_scope() as session:
            wallet = session.query(
                Wallet.codigo,
                Manager.nome.label('gestor_nome')
            ).select_from(Wallet) \
                .join(WalletManager, Wallet.id == WalletManager.carteira_id) \
                .join(Manager, WalletManager.gestor_id == Manager.id) \
                .filter(Wallet.id == wallet_id).one()

            return wallet
