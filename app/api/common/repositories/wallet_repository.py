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
        
        
    def get_properties_wallet(self, wallet_id: str):
        with self.get_session_scope() as session:
            properties = session.query(
                Property.lote,
                Property.id_no_banco,
                Property.descricao_legal_description,
                Property.consideracoes_importantes,
                Property.valor_proposto,
                Property.valor_minimo,
                (Property.valor_proposto * (Wallet.tx_servico / 100)).label('pgi_amount'),
                Property.imovel_origem,
                Property.data_limite,
                Property.data_primeiro_leilao_data,
                Property.data_segundo_leilao_data,
                Property.valor_primeiro_leilao_valor,
                Property.valor_segundo_leilao_valor,
                Property.id.label('imovel_id'),
                Property.nome,
                Property.idr_imovel,
                Manager.id.label('manager_id'),
                Manager.nome.label('manager_name'),
                Schedule.id.label('schedule_id'),
                DisputaWuzu.status,
                DisputaWuzu.wuzu_disputa_id.label('auction_id'),
                DisputaWuzu.wuzu_status,
                DisputaWuzu.data_inicio_disputa) \
                .select_from(Wallet) \
                .join(WalletProperty, Wallet.id == WalletProperty.carteira_id) \
                .join(Property, WalletProperty.imovel_id == Property.id) \
                .join(WalletManager, Wallet.id == WalletManager.carteira_id) \
                .join(Manager, WalletManager.gestor_id == Manager.id) \
                .join(WalletSchedule, Wallet.id == WalletSchedule.carteira_id) \
                .join(Schedule, WalletSchedule.cronograma_id == Schedule.id) \
                .join(DisputaWuzu, and_(DisputaWuzu.imovel_id == Property.id,
                                        Schedule.id == DisputaWuzu.cronograma_id,
                                        DisputaWuzu.wuzu_status != 'canceled'), isouter=True) \
                .filter(Wallet.id == wallet_id,
                        and_(Schedule.data_inicio <= func.current_date(), Schedule.data_final >= func.current_date()),
                        or_(DisputaWuzu.wuzu_status == None, DisputaWuzu.wuzu_status.not_in(['canceled', 'closed']))) \
                .group_by(Property.id) \
                .order_by(Property.lote).all()

            return properties