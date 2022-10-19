import os
from api.contract.contract_builder_interface import ContractFacadeInterface
from datetime import datetime

class CertificadoVendaFacade(ContractFacadeInterface):
    
    def __init__(self, wallet, schedule, property, regulamento, logs, sale_certificate_number):
        self.wallet = wallet
        self.schedule  = schedule
        self.property = property
        self.regulamento = regulamento
        self.logs = logs
        self.sale_certificate_number = sale_certificate_number
        
    def parse(self): 
        base_data = self.__get_base_data()
        logs = self.__get_logs()
        data = base_data | logs
        
        return data
    
    def __get_base_data(self):
        data_final = datetime.strftime(self.property.data_limite, "%d/%m/%Y")
        hora_final = datetime.strftime(self.property.data_limite, "%H:%M")
        
        return {
            'regulamento_url' : self.__get_regulamento_url(),
            'CEV' : self.sale_certificate_number,
            'MPR' : self.wallet.disputa_id,
            'CRONOGRAMA' : self.schedule.nome,
            'DATA_CONCORRENCIA' : data_final,
            'HORA_CONCORRENCIA' : hora_final
        }
    
    def __get_logs(self)->list:
        return {"LOGS" : list(map(self.parse_logs, self.logs))}
        
    
    @staticmethod
    def parse_logs(log: dict)->dict:
        
        data_modificacao = datetime.strftime(log.data_criacao, "%d/%m/%Y")
        hora_modificacao = datetime.strftime(log.data_criacao, "%H:%M")
        
        return{
            "DATA_MODIFICACAO" : data_modificacao,
            "HORA_MODIFICACAO" : hora_modificacao,
            "TEXTO_MODIFICADO" : log.descricao
        }
        
    def __get_regulamento_url(self):
        regulamento = self.regulamento
        
        base_url = os.environ.get("IMAGES_URL")
        
        if len(regulamento) != 0:
            return f'{base_url}/{regulamento.revisao_documento_id}'
            
        return ''