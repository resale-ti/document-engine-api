from api.contract.contract_builder_base import ContractBuilderBase
from api.common.helpers import update_task_progress
from api.common.repositories.manager_repository import ManagerRepository
from api.common.repositories.wallet_repository import WalletRepository
from api.common.repositories.property_repository import PropertyRepository
from api.common.repositories.seller_repository import SellerRepository
from app.api.common.models import Wallet



class EditalBuilder(ContractBuilderBase):
    """Classe Responsável """
    
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.wallet_id = data.get("id_obj")
        self.manager = ()
        self.requester_id = data.get("requester_id")
        self.data_inicio_regulamento = data.get("data_inicio")
        
    # def build(self) -> None:
    #     soma = 1+1
    #     print(soma)
    #     return soma
    
    
    def build(self) -> None:
        # update_task_progress(current=1, total=5)
        data = self.__get_contract_data()
        # documents_objects = self.__get_documents_objects_list(data)

        # update_task_progress(current=2, total=5)
        # file_bytes_b64 = self._generate_documents(documents_objects)

        # update_task_progress(current=3, total=5)
        # doc_data = self._handle_with_admin(file_bytes_b64=file_bytes_b64)
        # document_id = doc_data.get("document_id")

        # update_task_progress(current=4, total=5)
        # RegulamentoConcorrenciaLibrary().inactive_documents_from_wallet_id(
        #     wallet_id=self.wallet_id, document_id=document_id)

        # RegulamentoConcorrenciaLibrary().send_approved_document_email(self.wallet_id, document_id, file_bytes_b64)
        # update_task_progress(current=5, total=5)
        
        
    def __get_contract_data(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        
        """
        Os dados que preciso para o facade
        
        Dados do  Gestor ok
        Dados da Carteira ok
        
        Dados Cronograma e Canal de Venda
        
        Dados do imovel
        Fazer queiry focada no edital
        Dados Forma pagamento ok
        
        Dados do proponente 
        Dados do Encarregado ?
        """
        
        # Busca o gestor do imóvel
        self.manager = ManagerRepository().get_manager_by_wallet_id(self.wallet_id)
        print(self.manager)
        print(f"**************************************************************************")
        
        # Busca os dados da carteira
        wallet = WalletRepository().get_wallet_details(self.wallet_id)
        print(f"carteira: {wallet}")
        print(f"**************************************************************************")
        print(wallet)
        
        # Buscar os dados da forma e metodo de pagamentos
        payment_methods = SellerRepository().get_payment_method(
            payment_form_id=wallet.forma_pagamento_id)
        
        print(f"metodos de pagamentos: {payment_methods}")
        print(f"**************************************************************************")
        
        
        # Busca Dados do cronograma
        wallet = WalletRepository().get_schedule_by_wallet(self.wallet_id)
        

        return None
        