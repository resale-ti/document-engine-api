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
from utils.admin_integrations.contacts import AdminAPIContacts
from api.task_control.progressbar import TaskProgress
from datetime import date


class EditalBuilder(ContractBuilderBase):

    doc_name = "Edital Leilão"

    def __init__(self, data: dict) -> None:
        super().__init__()
        if "id_obj" not in data:
            raise Exception("[ERROR]: Missing wallet_id")

        self.wallet_id = data.get('id_obj', '0')
        self.manager = ()
        self.contacts = {}
        self.wallet = ()
        self.requester_id = data.get('requester_id', '0')
        self.contact_id = data.get('contact_id', '0')
        self.manager_change_id = data.get('manager_charge_id', '0')

    def build(self) -> None:
        TaskProgress.update_task_progress()
        data = self.__get_contract_data()

        TaskProgress.update_task_progress()
        documents_objects = self.__get_documents_objects_list(data)

        TaskProgress.update_task_progress()
        file_bytes_b64 = self._generate_documents(documents_objects)

        TaskProgress.update_task_progress()
        self._handle_with_admin(file_bytes_b64=file_bytes_b64)

        TaskProgress.update_task_progress()

    def _handle_with_admin(self, file_bytes_b64):
        doc_data = self.mount_data_admin_document(
            file_bytes_b64=file_bytes_b64)

        response = AdminAPIDocuments().post_create_document(data=doc_data)

        document_id = response.get("id")

        AdminAPIWallets().post_create_wallet_related_document(
            wallet_id=self.wallet_id, body={"data": [document_id]})

        if self.contacts:
            for contact in self.contacts:
                AdminAPIContacts().post_create_contact_related_document(
                    contact_id=contact.get('id'), body={"data": [document_id]})

        doc_data["document_id"] = document_id

        return doc_data

    def mount_data_admin_document(self, file_bytes_b64):
        doc_name = f"{self.doc_name} - {self.wallet.numero_leilao} - {self.manager.nome} - {date.today().strftime('%m%Y')}"

        return {
            "nome_doc": doc_name,
            "documento_nome": doc_name + ".pdf",
            "categoria_id": "edital",
            "file_mime_type": "application/pdf",
            "file": file_bytes_b64.decode('utf-8'),
            "usuario_responsavel_id": self.requester_id,
            "responsavel_gestor_id": self.manager_change_id,
            "tipo_exibicao": "publico"
        }

    def __get_documents_objects_list(self, data):
        return EditalFactory().get_instance(self.wallet_id, data)

    def __get_contract_data(self):
        self.manager = ManagerRepository().get_manager_by_wallet_id(self.wallet_id)
        manager_responsible = ManagerRepository().get_responsible_manager(
            self.manager.id, self.manager_change_id)
        self.contacts = ContactRepository().get_contact_detail(self.contact_id)
        self.wallet = WalletRepository().get_wallet_details(self.wallet_id)
        wallet_schedule = WalletRepository().get_schedule_by_wallet(self.wallet_id)
        properties = PropertyRepository().get_properties_wallet_to_leilao(self.wallet_id)
        payment_methods = PaymentRepository().get_payment_method(
            payment_form_id=self.wallet.forma_pagamento_id)
        dict_ = {}

        dict_tx_servico = EditalLibrary.define_tx_servico_min_max(
            properties[0].get('imovel_id'))
        dict_['taxa_minima'] = helper.number_format_money(
            dict_tx_servico.get("tx_servico_min"))
        dict_['taxa_maxima'] = helper.number_format_money(
            dict_tx_servico.get("tx_servico_max"))

        edital_facade = EditalFacade(
            wallet=self.wallet,
            payment_methods=payment_methods,
            properties=properties,
            cronograma=wallet_schedule,
            text_payments=self.mount_text_payments(payment_methods),
            proponente=self.contacts,
            manager_responsible=manager_responsible)

        return edital_facade.parse()

    def mount_text_payments(payment_methods):
        dict_ = {}
        for p in payment_methods:
            if p.get('tipo_condicao') == 'vista':
                dict_['condition_type_in_cash'] = 'X'

                if p.get('porcentagem_sinal', 0) > 0:
                    dict_['in_cash_payment_desc'] = dict_.get('in_cash_payment_desc', '') + helper.number_format(p.get('porcentagem_sinal', '0')) + \
                        r'% de entrada, '

                if p.get('porcentagem_ccv', 0) > 0:
                    dict_['in_cash_payment_desc'] = dict_.get('in_cash_payment_desc', '') + helper.number_format(p.get('porcentagem_ccv', '0')) + \
                        r'% do pagamento na emissão do CCV (Contrato de Compra e Venda)'

                if p.get('porcentagem_escritura', 0) > 0:
                    dict_['in_cash_payment_desc'] = dict_.get('in_cash_payment_desc', '') + ', ' + helper.number_format(p.get('porcentagem_escritura', '0')) + \
                        r'% na escritura'

                if p.get('a_vista_desconto', 0) > 0:
                    dict_['in_cash_payment_desc'] = dict_.get('in_cash_payment_desc', '') + ', c/ ' + helper.number_format(p.get('a_vista_desconto', '0')) + \
                        r'% de desconto sobre o valor do lance vencedor'

            if p.get('tipo_condicao') == 'financiado':
                dict_['condition_type_financiado'] = 'X'

                if p.get('porcentagem_entrada_financiamento', 0) > 0:
                    dict_['financing_payment_text'] = helper.number_format(
                        p.get('porcentagem_entrada_financiamento')) + r'% de entrada'

            if p.get('tipo_condicao') == 'parcelado':
                dict_['cash_payment_text'] = f" {p.get('a_vista_complemento_texto')}" if p.get(
                    'a_vista_complemento_texto') else ''
                dict_['parceled_payment_text'] = f"  {p.get('parcelado_complemento_texto')}" if p.get(
                    'parcelado_complemento_texto') else ''
                dict_['financing_payment_text'] = f"  {p.get('financiamento_complemento_texto')}" if p.get(
                    'financiamento_complemento_texto') else ''

                dict_['condition_type_installments'] = 'X'
                payment_installments = PaymentRepository().get_payment_installments(
                    payment_condition_id=p.get('id'))

                if payment_installments[0].get('qtd_fixa'):
                    sorted(payment_installments, key=lambda x: x.get(
                        'qtd_fixa'), reverse=True)
                else:
                    sorted(payment_installments, key=lambda x: x.get(
                        'qtd_maxima'), reverse=True)

                payment_installments = payment_installments[0]

                dict_['entry_percent'] = payment_installments.get(
                    'porcentagem_entrada', '0')

                dict_['installments_payment_desc'] = helper.number_format(
                    dict_.get('entry_percent')) + r'% de entrada e '

                dict_['interest_period'] = payment_installments.get(
                    'periodo_juros') if payment_installments.get('periodo_juros') else 'a.m.'
                dict_['interest_rate'] = ((payment_installments.get(
                    'tx_juros') if payment_installments.get('tx_juros') else 0) * 100) / 100

                dict_['correction_period'] = payment_installments.get(
                    'periodo_correcao') if payment_installments.get('periodo_correcao') else 'a.m.'
                dict_['correction_rate'] = ((payment_installments.get(
                    'tx_correcao') if payment_installments.get('tx_correcao') else 0) * 100) / 100

                dict_['indexador'] = helper.normalize_payment_method(
                    payment_installments.get('indexador'))

                if payment_installments.get('qtd_fixa') > 0:
                    dict_[
                        'installments_payment_desc'] = f"{dict_.get('installments_payment_desc', '')}saldo em até {payment_installments.get('qtd_fixa')} "
                    f"parcelas com juros de {helper.number_format(dict_.get('interest_rate', ''))}% {dict_.get('interest_period', '')}"
                else:
                    dict_[
                        'installments_payment_desc'] = f"{dict_.get('installments_payment_desc', '')}saldo em até {payment_installments.get('qtd_maxima')} "
                    f"parcelas com juros de {helper.number_format(dict_.get('interest_rate', ''))}% {dict_.get('interest_period', '')}"

                if dict_.get('correction_rate'):
                    dict_['installments_payment_desc'] = dict_.get(
                        'installments_payment_desc', '')
                    f" + correção de {helper.number_format(dict_.get('correction_rate', ''))}% {dict_.get('correction_period', '')}"

                if dict_.get('indexador'):
                    dict_['installments_payment_desc'] = dict_.get(
                        'installments_payment_desc', '') + f" + {dict_.get('indexador', '')}"

        return dict_
