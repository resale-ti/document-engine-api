from core.database import Base

Base.prepare()

CeleryTask = Base.classes.tarefas_celery

Property, WalletProperty, Wallet = Base.classes.imovel, Base.classes.carteira_imovel, \
    Base.classes.carteira

PropertyAddress, Address = Base.classes.imovel_endereco, Base.classes.endereco
City = Base.classes.cidade

WalletSchedule, Schedule = Base.classes.carteira_cronograma, Base.classes.cronograma

WalletManager, Manager = Base.classes.carteira_gestor, Base.classes.gestor

DisputaWuzu = Base.classes.disputa_wuzu
Qualification = Base.classes.qualificacao

PaymentFormsWallet = Base.classes.carteira_formas_pagamento
PaymentConditionsWallet = Base.classes.carteira_condicoes_pagamento
PaymentInstallments = Base.classes.carteira_parcelas

Document, DocumentRevision, WalletDocument = Base.classes.documento, Base.classes.documento_revisao, Base.classes.carteira_documento

Usuario = Base.classes.usuario

CertificadoVendaLogs = Base.classes.certificados_venda_logs

PropertyHistory = Base.classes.imovel_history