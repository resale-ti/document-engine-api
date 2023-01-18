from core.database import Base

Base.prepare()

CeleryTask = Base.classes.tarefas_celery

Property, WalletProperty, Wallet = Base.classes.imovel, Base.classes.carteira_imovel, \
    Base.classes.carteira

WalletSchedule, Schedule = Base.classes.carteira_cronograma, Base.classes.cronograma

WalletManager, Manager = Base.classes.carteira_gestor, Base.classes.gestor

ResponsibleManager = Base.classes.gestor_responsavel

Contact, ContactEmail, Email = Base.classes.contato, Base.classes.contato_email, Base.classes.email

ScheduleSalesChannel, SalesChannel = Base.classes.cronograma_canal_venda, Base.classes.canal_venda

ManagerSalesCategory = Base.classes.gestor_categoria_venda
ManagerProperty = Base.classes.imovel_gestor

Management = Base.classes.gerenciador

DisputaWuzu = Base.classes.disputa_wuzu
Qualification = Base.classes.qualificacao

PaymentFormsWallet = Base.classes.carteira_formas_pagamento
PaymentConditionsWallet = Base.classes.carteira_condicoes_pagamento
PaymentInstallments = Base.classes.carteira_parcelas

Document, DocumentRevision, WalletDocument = Base.classes.documento, Base.classes.documento_revisao, Base.classes.carteira_documento

Usuario = Base.classes.usuario

CertificadoVendaLogs = Base.classes.certificados_venda_logs