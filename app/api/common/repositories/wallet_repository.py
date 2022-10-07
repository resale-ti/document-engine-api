from api.common.database_common import DBSessionContext
from api.common.models import Wallet, Property, Manager, Schedule, DisputaWuzu, WalletProperty, WalletSchedule, WalletManager, ScheduleSalesChannel, SalesChannel, Management
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

        
    def get_schedule_by_wallet(self, wallet_id: str):
        """
        

        Args:
            wallet_id (str): _description_

        Returns:
            _type_: _description_
        """
        with self.get_session_scope() as session:
                schedule_sales_channel_data = session.query(Wallet.nome.label('wallet_name'),
                                       Wallet.id.label('wallet_id'),
                                       Schedule.nome.label('cronograma_id'),
                                       SalesChannel.nome.label('canal_venda_id'),
                                       #Responsável Nome
                                       SalesChannel.responsavel_nome,
                                       SalesChannel.responsavel_cpf,
                                       SalesChannel.canal_responsavel_telefone,
                                       SalesChannel.uf_jucesp,
                                       SalesChannel.numero_jucesp,
                                       SalesChannel.site,
                                       # Endereço
                                       SalesChannel.endereco_cidade,
                                       SalesChannel.endereco_estado,
                                       SalesChannel.endereco_rua,
                                       SalesChannel.endereco_cep,
                                       SalesChannel.endereco_bairro,
                                       SalesChannel.endereco_numero,
                                       
                                       Management.nome
                                       )\
                                           .select_from(Wallet) \
                                           .join(WalletSchedule, Wallet.id == WalletSchedule.carteira_id) \
                                           .join(Schedule, WalletSchedule.cronograma_id  == Schedule.id) \
                                           .join(ScheduleSalesChannel, ScheduleSalesChannel.cronograma_id == Schedule.id,isouter=True)\
                                           .join(SalesChannel,ScheduleSalesChannel.canal_venda_id == SalesChannel.id,isouter=True )\
                                           .join(Management, Management.id == Schedule.gerenciador_id,isouter=True)\
                                           .filter(Wallet.id == wallet_id,
                                                    and_(Schedule.data_inicio <= func.current_date(), Schedule.data_final >= func.current_date())).one()
                print(f"retorno do banco {schedule_sales_channel_data}")
        return schedule_sales_channel_data
            
            
            
        