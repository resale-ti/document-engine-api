from api.contract.contract_builder_base import ContractBuilderBase
from api.common.repositories.wallet_repository import WalletRepository
from api.common.repositories.payment_repository import PaymentRepository
from api.common.repositories.property_repository import PropertyRepository
from api.common.repositories.manager_repository import ManagerRepository
from api.common.repositories.contact_repository import ContactRepository
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
        self.contact_id = data.contact_id
        self.manager_change_id = data.manager_charge_id

    def build(self) -> None:
        #update_task_progress(current=1, total=5)
        data = self.__get_contract_data()
        documents_objects = self.__get_documents_objects_list(data)

        #update_task_progress(current=2, total=5)
        file_bytes_b64 = self._generate_documents(documents_objects)
        
        return self.mount_data_admin_document(file_bytes_b64)

        #update_task_progress(current=3, total=5)
        # doc_data = self._handle_with_admin(file_bytes_b64=file_bytes_b64)
        # document_id = doc_data.get("document_id")
        
        

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
        return EditalFactory().get_instance(self.wallet_id, data)

    def __get_contract_data(self):
        self.manager = ManagerRepository().get_manager_by_wallet_id(self.wallet_id)
        manager_responsible = ManagerRepository().get_responsible_manager(self.manager.id, self.manager_change_id)
        contact = ContactRepository().get_contact_detail(self.contact_id)
        wallet = WalletRepository().get_wallet_details(self.wallet_id)
        wallet_schedule = WalletRepository().get_schedule_by_wallet(self.wallet_id)
        properties = PropertyRepository().get_properties_wallet_to_leilao(self.wallet_id)
        payment_methods = PaymentRepository().get_payment_method(
            payment_form_id=wallet.forma_pagamento_id)
        dict_aux = {}
        
        for p in payment_methods:
            if (p.get('tipo_condicao') == 'parcelado'):
                dict_aux['cash_payment_text'] = f" {p.get('a_vista_complemento_texto')}" if p.get('a_vista_complemento_texto') else ''
                dict_aux['parceled_payment_text'] = f"  {p.get('parcelado_complemento_texto')}" if p.get('parcelado_complemento_texto') else ''
                dict_aux['financing_payment_text'] = f"  {p.get('financiamento_complemento_texto')}" if p.get('financiamento_complemento_texto') else ''

            if  p.get('tipo_condicao') == 'vista':
                dict_aux['condition_type_in_cash'] = 'X'

                if p.get('porcentagem_sinal', 0) > 0: 
                    dict_aux['in_cash_payment_desc'] = dict_aux.get('in_cash_payment_desc', '') + helper.number_format(p.get('porcentagem_sinal', '0')) + \
                    r'% de entrada, '
                
                if  p.get('porcentagem_ccv', 0) > 0:
                    dict_aux['in_cash_payment_desc'] = dict_aux.get('in_cash_payment_desc', '') + helper.number_format(p.get('porcentagem_ccv', '0')) + \
                    r'% do pagamento na emissão do CCV (Contrato de Compra e Venda)'
                
                if  p.get('porcentagem_escritura', 0) > 0:
                    dict_aux['in_cash_payment_desc'] = dict_aux.get('in_cash_payment_desc', '') + ', ' + helper.number_format(p.get('porcentagem_escritura', '0')) + \
                        r'% na escritura'
                
                if  p.get('a_vista_desconto', 0) > 0:
                    dict_aux['in_cash_payment_desc'] = dict_aux.get('in_cash_payment_desc', '') + ', c/ ' + helper.number_format(p.get('a_vista_desconto', '0')) + \
                        r'% de desconto sobre o valor do lance vencedor'

            if p.get('tipo_condicao') == 'financiado': 
                dict_aux['condition_type_financiado'] = 'X'

                if  p.get('porcentagem_entrada_financiamento', 0) > 0:
                    dict_aux['financing_payment_text'] = helper.number_format(p.get('porcentagem_entrada_financiamento')) + r'% de entrada'    
            
            if p.get('tipo_condicao') == 'parcelado': 
                dict_aux['condition_type_installments'] = 'X'
                payment_installments = PaymentRepository().get_payment_installments(payment_condition_id=p.get('id'))

                if payment_installments[0].get('qtd_fixa'):
                    sorted(payment_installments, key=lambda x: x.get('qtd_fixa'), reverse=True)
                else:
                    sorted(payment_installments, key=lambda x: x.get('qtd_maxima'), reverse=True)
                    
                payment_installments = payment_installments[0]

                dict_aux['entry_percent'] = payment_installments.get('porcentagem_entrada', '0')

                dict_aux['installments_payment_desc'] = helper.number_format(dict_aux.get('entry_percent')) + r'% de entrada e '

                dict_aux['interest_period'] = payment_installments.get('periodo_juros') if payment_installments.get('periodo_juros') else 'a.m.'
                dict_aux['interest_rate'] = ((payment_installments.get('tx_juros') if payment_installments.get('tx_juros') else 0) * 100) / 100

                dict_aux['correction_period'] = payment_installments.get('periodo_correcao') if payment_installments.get('periodo_correcao') else 'a.m.'
                dict_aux['correction_rate'] = ((payment_installments.get('tx_correcao') if payment_installments.get('tx_correcao') else 0 ) * 100) / 100

                dict_aux['indexador'] = helper.normalize_payment_method(payment_installments.get('indexador'))

                if payment_installments.get('qtd_fixa') > 0:
                    dict_aux['installments_payment_desc'] = f"{dict_aux.get('installments_payment_desc', '')}saldo em até {payment_installments.get('qtd_fixa')} " 
                    f"parcelas com juros de {helper.number_format(dict_aux.get('interest_rate', ''))}% {dict_aux.get('interest_period', '')}"
                else:
                    dict_aux['installments_payment_desc'] = f"{dict_aux.get('installments_payment_desc', '')}saldo em até {payment_installments.get('qtd_maxima')} "  
                    f"parcelas com juros de {helper.number_format(dict_aux.get('interest_rate', ''))}% {dict_aux.get('interest_period', '')}"

                if dict_aux.get('correction_rate'):
                    dict_aux['installments_payment_desc'] = dict_aux.get('installments_payment_desc', '') 
                    f" + correção de {helper.number_format(dict_aux.get('correction_rate', ''))}% {dict_aux.get('correction_period', '')}"
                
                if dict_aux.get('indexador'):
                    dict_aux['installments_payment_desc'] = dict_aux.get('installments_payment_desc', '') + f" + {dict_aux.get('indexador', '')}"
        
        dict_tx_servico = EditalLibrary.define_tx_servico_min_max(properties[0].get('imovel_id'))
        dict_aux['taxa_minima'] = helper.number_format_money(dict_tx_servico.get("tx_servico_min"))
        dict_aux['taxa_maxima'] = helper.number_format_money(dict_tx_servico.get("tx_servico_max"))
        
        edital_facade = EditalFacade(
            wallet=wallet,
            payment_methods=payment_methods,
            properties=properties,
            cronograma=wallet_schedule,
            aux=dict_aux,
            proponente=contact,
            manager_responsible=manager_responsible)

        return edital_facade.parse()
