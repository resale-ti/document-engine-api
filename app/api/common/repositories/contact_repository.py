from api.common.database_common import DBSessionContext
from api.common.models import Contact, Email, ContactEmail


class ContactRepository(DBSessionContext):
    def get_contact_detail(self, contact_id):
        with self.get_session_scope() as session:
            contact = session.query(
                Contact.id,
                Email.email.label('email_address')
            ).select_from(Contact) \
                .join(ContactEmail, ContactEmail.contato_id == Contact.id) \
                .join(Email, ContactEmail.email_id == Email.id) \
                .filter(Contact.id == contact_id).one()

            return contact