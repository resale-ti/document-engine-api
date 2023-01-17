from api.contract.contract_builder_base import ContractBuilderBase
from api.common.repositories.wallet_repository import WalletRepository
from api.common.repositories.payment_repository import PaymentRepository
from api.common.repositories.property_repository import PropertyRepository
from api.common.repositories.qualification_repository import QualificationRepository
from api.common.repositories.property_auction_repository import PropertyAuctionRepository
from api.common.repositories.manager_repository import ManagerRepository
import api.contract.edital.edital_helpers as helper
from api.contract.edital.edital_facade import EditalFacade
from api.contract.edital.edital_factory import EditalFactory
from api.contract.edital.edital_library import EditalLibrary
from utils.admin_integrations.documents import AdminAPIDocuments
from utils.admin_integrations.wallets import AdminAPIWallets
from api.common.helpers import update_task_progress
import time
from datetime import date


class EditalBuilder(ContractBuilderBase):

    doc_name = "Edital"

    def __init__(self, data: dict) -> None:
        super().__init__()

        if "id_obj" in data:
            raise Exception("[ERROR]: Missing wallet_id")

        self.wallet_id = data.id_obj
        self.manager = ()
        self.requester_id = data.requester_id

    def build(self) -> None:
        #update_task_progress(current=1, total=5)
        data = self.__get_contract_data()
        documents_objects = self.__get_documents_objects_list(data)

        #update_task_progress(current=2, total=5)
        file_bytes_b64 = self._generate_documents(documents_objects)

        #update_task_progress(current=3, total=5)
        doc_data = self._handle_with_admin(file_bytes_b64=file_bytes_b64)
        document_id = doc_data.get("document_id")

        #update_task_progress(current=4, total=5)
        #RegulamentoConcorrenciaLibrary().inactive_documents_from_wallet_id(
        #    wallet_id=self.wallet_id, document_id=document_id)

        #RegulamentoConcorrenciaLibrary().send_approved_document_email(self.wallet_id, document_id, file_bytes_b64)
        #update_task_progress(current=5, total=5)


    def _handle_with_admin(self, file_bytes_b64):
        doc_data = self.mount_data_admin_document(
            file_bytes_b64=file_bytes_b64)

        response = AdminAPIDocuments().post_create_document(data=doc_data)

        document_id = response.get("id")

        AdminAPIWallets().post_create_wallet_related_document(
            wallet_id=self.wallet_id, body={"data": [document_id]})

        doc_data["document_id"] = document_id

        return doc_data

    def mount_data_admin_document(self, file_bytes_b64):
        doc_name = f"{self.doc_name} - {self.manager.nome} - {date.today().strftime('%Y%m%d')}"

        return {
            "nome_doc": doc_name,
            "documento_nome": doc_name + ".pdf",
            "categoria_id": "edital",
            "file_mime_type": "application/pdf",
            "file": file_bytes_b64.decode('utf-8'),
            "tipo_exibicao": "publico",
            "usuario_responsavel_id": self.requester_id,
            "documento_status": "approved"
        }

    def __get_documents_objects_list(self, data):
        edital_documents_factory = EditalFactory(
        ).get_instance(self.wallet_id, data)

        return edital_documents_factory

    def __get_contract_data(self):
        self.manager = ManagerRepository().get_manager_by_wallet_id(self.wallet_id)
        wallet = WalletRepository().get_wallet_details(self.wallet_id)
        
        wallet_schedule = WalletRepository().get_schedule_by_wallet(self.wallet_id)

        properties = PropertyRepository().get_properties_wallet_to_leilao(self.wallet_id)

        payment_methods = PaymentRepository().get_payment_method(
            payment_form_id=wallet.forma_pagamento_id)
        
        in_cash_payment_desc = ''
        for p in payment_methods:
            if (p.get('tipo_condicao') == 'parcelado'):
                cash_payment_text = f" {p.get('a_vista_complemento_texto')}" if p.get('a_vista_complemento_texto') else ''
                parceled_payment_text = f"  {p.get('parcelado_complemento_texto')}" if p.get('parcelado_complemento_texto') else ''
                financing_payment_text = f"  {p.get('financiamento_complemento_texto')}" if p.get('financiamento_complemento_texto') else ''

            if  p.get('tipo_condicao') == 'vista':
                condition_type_in_cash = 'X'

                if p.get('porcentagem_sinal', 0) > 0: 
                    in_cash_payment_desc = in_cash_payment_desc + helper.number_format(p.get('porcentagem_sinal', '0')) + \
                    r'% de entrada, '
                
                if  p.get('porcentagem_ccv', 0) > 0:
                    in_cash_payment_desc = in_cash_payment_desc + helper.number_format(p.get('porcentagem_ccv', '0')) + \
                    r'% do pagamento na emissão do CCV (Contrato de Compra e Venda)'
                
                if  p.get('porcentagem_escritura', 0) > 0:
                    in_cash_payment_desc = in_cash_payment_desc + ', ' + helper.number_format(p.get('porcentagem_escritura', '0')) + \
                        r'% na escritura'
                
                if  p.get('a_vista_desconto', 0) > 0:
                    in_cash_payment_desc = in_cash_payment_desc + ', c/ ' + helper.number_format(p.get('a_vista_desconto', '0')) + \
                        r'% de desconto sobre o valor do lance vencedor'

            if p.get('tipo_condicao') == 'financiado': 
                condition_type_financiado = 'X'

                if  p.get('porcentagem_entrada_financiamento', 0) > 0:
                    financing_payment_text = helper.number_format(p.get('porcentagem_entrada_financiamento')) + r'% de entrada'    
            

            if p.get('tipo_condicao') == 'parcelado': 
                condition_type_installments = 'X'
                payment_installments = PaymentRepository().get_payment_installments(payment_condition_id=p.get('id'))

                if payment_installments[0].get('qtd_fixa'):
                    sorted(payment_installments, key=lambda x: x.get('qtd_fixa'), reverse=True)
                else:
                    sorted(payment_installments, key=lambda x: x.get('qtd_maxima'), reverse=True)
                    
                payment_installments = payment_installments[0]

                entry_percent = payment_installments.get('porcentagem_entrada', '0')

                installments_payment_desc = helper.number_format(entry_percent) + r'% de entrada e '

                interest_period = payment_installments.get('periodo_juros') if payment_installments.get('periodo_juros') else 'a.m.'
                interest_rate = ((payment_installments.get('tx_juros') if payment_installments.get('tx_juros') else 0) * 100) / 100

                correction_period = payment_installments.get('periodo_correcao') if payment_installments.get('periodo_correcao') else 'a.m.'
                correction_rate = ((payment_installments.get('tx_correcao') if payment_installments.get('tx_correcao') else 0 ) * 100) / 100

                indexador = helper.normalize_payment_method(payment_installments.get('indexador'))

                if payment_installments.get('qtd_fixa') > 0:
                    installments_payment_desc = f"{installments_payment_desc}saldo em até {payment_installments.get('qtd_fixa')} " 
                    f"parcelas com juros de {helper.number_format(interest_rate)}% {interest_period}"
                else:
                    installments_payment_desc = f"{installments_payment_desc}saldo em até {payment_installments.get('qtd_maxima')} "  
                    f"parcelas com juros de {helper.number_format(interest_rate)}% {interest_period}"

                if correction_rate:
                    installments_payment_desc = installments_payment_desc + f" + correção de {helper.number_format(correction_rate)}% {correction_period}"
                
                if indexador:
                    installments_payment_desc = installments_payment_desc + f" + {indexador}"
        
        dict_tx_servico = EditalLibrary.define_tx_servico_min_max(properties[0].get('imovel_id'))
        taxa_minima = helper.number_format_money(dict_tx_servico.get("tx_servico_min"))
        taxa_maxima = helper.number_format_money(dict_tx_servico.get("tx_servico_max"))            
                    

        edital_facade = EditalFacade(
            wallet=wallet,
            payment_methods=payment_methods,
            properties=properties,
            cronograma=wallet_schedule)

        return edital_facade.parse()
