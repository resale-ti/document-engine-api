from api.common.database_common import DBSessionContext
from api.common.models import PaymentFormsWallet, PaymentConditionsWallet, PaymentInstallments
from api.common.helpers import transform_dict


class SellerRepository(DBSessionContext):
    def get_payment_method(self, payment_form_id: str):
        with self.get_session_scope() as session:
            payment_methods = session.query(PaymentConditionsWallet.id,
                                            PaymentConditionsWallet.tipo_condicao,
                                            PaymentFormsWallet.vendedor_id,
                                            PaymentFormsWallet.status,
                                            PaymentConditionsWallet.porcentagem_sinal,
                                            PaymentConditionsWallet.porcentagem_ccv,
                                            PaymentConditionsWallet.porcentagem_escritura,
                                            PaymentConditionsWallet.a_vista_desconto) \
                .join(PaymentConditionsWallet, PaymentFormsWallet.id == PaymentConditionsWallet.id_method) \
                .filter(PaymentFormsWallet.status == 'ativo', PaymentFormsWallet.id == payment_form_id).all()

            return transform_dict(payment_methods)

    def get_payment_installments(self, payment_condition_id: str):
        with self.get_session_scope() as session:
            payment_installments = session.query(PaymentInstallments.qtd_fixa,
                                                 PaymentInstallments.qtd_maxima,
                                                 PaymentInstallments.porcentagem_entrada) \
                .filter(PaymentInstallments.id_condition == payment_condition_id).all()

            return transform_dict(payment_installments)
