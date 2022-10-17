import os
from tkinter import HORIZONTAL
from api.contract.contract_builder_interface import ContractFacadeInterface

class CertificadoVendaFacade(ContractFacadeInterface):
    
    def __init__(self, wallet, schedule, property, regulamento, logs, sale_certificate_number):
        self.wallet = wallet
        self.schedule  = schedule
        self.property = property
        self.regulamento = regulamento
        self.logs = logs
        self.sale_certificate_number = sale_certificate_number
        
    def parse(self)-> dict:
        base_data = self.__get_base_data()
        logs = self.__get_logs()
        data = base_data + logs
        
        return data
    
    def __get_base_data(self):
        data_final = "datafinal"
        hora_final = 'horafinal'
        
        return {
            'regulamento_url' : self.__get_regulamento_url(),
            'CEV' : self.sale_certificate_number,
            'MPR' : self.wallet.disputa_id,
            'CRONOGRAMA' : self.schedule.nome,
            'DATA_CONCORRENCIA' : data_final,
            'HORA_CONCORRENCIA' : hora_final
        }
    
    def __get_logs(self):
        return ''
    
    def __get_regulamento_url(self):
        regulamento = self.regulamento
        
        if len(regulamento) != 0:
            f'configitemurl{regulamento.revisao_documento_id}'
            
        return ''